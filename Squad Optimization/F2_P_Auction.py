import cvxpy as cp

# Define decision variables (integer variables representing counts of players in each category)
# Integer constraints make this an Integer Linear Programming (ILP) problem
bats = cp.Variable(integer=True)       # Number of batsmen
spin = cp.Variable(integer=True)       # Number of spin bowlers
fast = cp.Variable(integer=True)       # Number of fast bowlers
allrounder = cp.Variable(integer=True) # Number of allrounders

# Define constraints on decision variables:
# These are linear inequalities and equalities, which keep the problem convex
constraints = [
    bats >= 4, bats <= 8,                # Batsmen between 4 and 8
    spin >= 2, spin <= 6,                # Spin bowlers between 2 and 6
    fast >= 2, fast <= 6,                # Fast bowlers between 2 and 6
    allrounder >= 5, allrounder <= 9,   # Allrounders between 5 and 9
    bats + spin + fast + allrounder == 23  # Total squad size fixed at 23 players
]

# Define the linear objective function to maximize:
# Total score is a weighted sum of the number of players in each category
score = 90 * bats + 26 * spin + 51 * fast + 80 * allrounder

# Define the optimization objective: maximize the total score
objective = cp.Maximize(score)

# Define the convex optimization problem with linear constraints and objective
problem = cp.Problem(objective, constraints)

# Solve the problem using a suitable solver that supports integer variables
problem.solve()

# Check if an optimal solution was found
if problem.status == cp.OPTIMAL:
    # Extract the integer values of the decision variables by rounding
    bats_val = int(round(bats.value.item()))
    spin_val = int(round(spin.value.item()))
    fast_val = int(round(fast.value.item()))
    all_val = int(round(allrounder.value.item()))

    # Calculate the total score based on the solution
    total_score = 90 * bats_val + 26 * spin_val + 51 * fast_val + 80 * all_val

    # Print the optimal squad composition and total score
    print("Optimal Squad Composition:")
    print(f"Batsmen: {bats_val}, Spin Bowlers: {spin_val}, Fast Bowlers: {fast_val}, Allrounders: {all_val}")
    print(f"Total Score: {total_score}")

    # Function to distribute players into sub-categories proportionally by given weights
    def distribute_counts(total, weights):
        total_weight = sum(weights)
        # Calculate raw fractional counts based on weights
        raw_counts = [total * w / total_weight for w in weights]
        # Convert to integer counts by truncation
        int_counts = [int(x) for x in raw_counts]
        # Calculate remainder to distribute due to truncation
        remainder = total - sum(int_counts)
        # Calculate fractional parts to decide where to add remainder
        fractional_parts = [x - int(x) for x in raw_counts]
        # Distribute remainder to sub-categories with largest fractional parts
        for _ in range(remainder):
            idx = fractional_parts.index(max(fractional_parts))
            int_counts[idx] += 1
            fractional_parts[idx] = 0
        return int_counts

    # Distribute batsmen into sub-categories: IDB, IIN, OIN based on given weights
    IDB, IIN, OIN = distribute_counts(bats_val, [8, 13, 11])
    # Distribute spin bowlers into sub-categories: IDSB, IISB, OISB
    IDSB, IISB, OISB = distribute_counts(spin_val, [6, 11, 9])
    # Distribute fast bowlers into sub-categories: IDFB, IIFB, OIFB
    IDFB, IIFB, OIFB = distribute_counts(fast_val, [7, 12, 10])
    # Distribute allrounders into sub-categories: IDA, IIA, OIA
    IDA, IIA, OIA = distribute_counts(all_val, [9, 14, 12])

    # Print detailed squad composition by sub-categories
    print("\nDetailed Squad Composition:")
    print(f"IDB = {IDB}, IIN = {IIN}, OIN = {OIN}")
    print(f"IDSB = {IDSB}, IISB = {IISB}, OISB = {OISB}")
    print(f"IDFB = {IDFB}, IIFB = {IIFB}, OIFB = {OIFB}")
    print(f"IDA = {IDA}, IIA = {IIA}, OIA = {OIA}")

else:
    # No optimal solution found for the given constraints
    print("No optimal solution found.")
