library(lpSolve)

# Define the coefficients for the objective function:
# These represent the "scores" or "values" assigned to each player type
# The goal is to maximize the total score of the squad
objective_coeffs <- c(90, 26, 51, 80)  # Coefficients for batsmen, spin bowlers, fast bowlers, allrounders

# Define the constraints matrix:
# Each row corresponds to a linear constraint on the decision variables
# Columns correspond to variables: bats, spin, fast, allrounder
constraints <- matrix(c(
  1, 0, 0, 0,  # Batsmen lower bound constraint coefficient
  1, 0, 0, 0,  # Batsmen upper bound constraint coefficient
  0, 1, 0, 0,  # Spin bowlers lower bound constraint coefficient
  0, 1, 0, 0,  # Spin bowlers upper bound constraint coefficient
  0, 0, 1, 0,  # Fast bowlers lower bound constraint coefficient
  0, 0, 1, 0,  # Fast bowlers upper bound constraint coefficient
  0, 0, 0, 1,  # Allrounders lower bound constraint coefficient
  0, 0, 0, 1,  # Allrounders upper bound constraint coefficient
  1, 1, 1, 1   # Total players constraint (sum of all players)
), nrow = 9, byrow = TRUE)

# Define the direction of each constraint:
# ">=" for lower bounds, "<=" for upper bounds, "==" for equality constraint
direction <- c(">=", "<=", ">=", "<=", ">=", "<=", ">=", "<=", "==")

# Define the right-hand side values for each constraint:
# These specify the bounds and total number of players
rhs <- c(4, 8, 2, 6, 2, 6, 5, 9, 23)

# Solve the integer linear programming problem:
# "max" specifies maximization of the objective function
# all.int = TRUE enforces integer solutions for all variables
result <- lp("max", objective_coeffs, constraints, direction, rhs, all.int = TRUE)

# Check if an optimal solution was found (status == 0 means success)
if (result$status == 0) {
  # Extract the integer values of the decision variables from the solution
  bats_val <- result$solution[1]      # Number of batsmen
  spin_val <- result$solution[2]      # Number of spin bowlers
  fast_val <- result$solution[3]      # Number of fast bowlers
  all_val <- result$solution[4]       # Number of allrounders
  
  # Calculate the total score based on the solution
  total_score <- 90 * bats_val + 26 * spin_val + 51 * fast_val + 80 * all_val
  
  # Prints the optimal squad composition and total score
  cat("Optimal Squad Composition:\n")
  cat(sprintf("Batsmen: %d, Spin Bowlers: %d, Fast Bowlers: %d, Allrounders: %d\n", bats_val, spin_val, fast_val, all_val))
  cat(sprintf("Total Score: %d\n", total_score))
  
  # Function to distribute players into sub-categories proportionally by given weights
  # This is a post-processing step to allocate players into finer groups
  distribute_counts <- function(total, weights) {
    total_weight <- sum(weights)
    # Calculate raw fractional counts based on weights
    raw_counts <- total * weights / total_weight
    # Convert to integer counts by truncation (floor)
    int_counts <- floor(raw_counts)
    # Calculate remainder to distribute due to truncation
    remainder <- total - sum(int_counts)
    # Calculate fractional parts to decide where to add remainder
    fractional_parts <- raw_counts - int_counts
    # Distribute remainder to sub-categories with largest fractional parts
    for (i in seq_len(remainder)) {
      idx <- which.max(fractional_parts)
      int_counts[idx] <- int_counts[idx] + 1
      fractional_parts[idx] <- 0
    }
    return(int_counts)
  }
  
  # Distribute batsmen into sub-categories: IDB, IIN, OIN based on given weights
  bats_subcategories <- distribute_counts(bats_val, c(8, 13, 11))
  IDB <- bats_subcategories[1]
  IIN <- bats_subcategories[2]
  OIN <- bats_subcategories[3]
  
  # Distribute spin bowlers into sub-categories: IDSB, IISB, OISB
  spin_subcategories <- distribute_counts(spin_val, c(6, 11, 9))
  IDSB <- spin_subcategories[1]
  IISB <- spin_subcategories[2]
  OISB <- spin_subcategories[3]
  
  # Distribute fast bowlers into sub-categories: IDFB, IIFB, OIFB
  fast_subcategories <- distribute_counts(fast_val, c(7, 12, 10))
  IDFB <- fast_subcategories[1]
  IIFB <- fast_subcategories[2]
  OIFB <- fast_subcategories[3]
  
  # Distribute allrounders into sub-categories: IDA, IIA, OIA
  all_subcategories <- distribute_counts(all_val , c(9, 14, 12))
  IDA <- all_subcategories[1]
  IIA <- all_subcategories[2]
  OIA <- all_subcategories[3]
  
  # Print detailed squad composition by sub-categories
  cat("\nDetailed Squad Composition:\n")
  cat(sprintf("IDB = %d, IIN = %d, OIN = %d\n", IDB, IIN, OIN))
  cat(sprintf("IDSB = %d, IISB = %d, OISB = %d\n", IDSB, IISB, OISB))
  cat(sprintf("IDFB = %d, IIFB = %d, OIFB = %d\n", IDFB, IIFB, OIFB))
  cat(sprintf("IDA = %d, IIA = %d, OIA = %d\n", IDA, IIA, OIA))
  
} else {
  # No optimal solution found for the given constraints
  cat("No optimal solution found.\n")
}
