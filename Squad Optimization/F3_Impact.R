library(readxl)
library(dplyr)
library(stringr)

# Define the path to the Excel file
excel_file <- "path to IPL_2025_Auction_List.xlsx"

# Read the Excel file (assuming the data is in the first sheet)
auction_data <- read_excel(excel_file, sheet = 1)

# View the structure of the data (to understand its format)
str(auction_data)

# Assuming the price information is in a column called 'Price'
# If the column name is different, replace 'Price' with the actual column name
# You can inspect the data to find the exact column name

# Clean the data if needed
auction_data_clean <- auction_data %>%
  filter(!is.na(Price))

# Define the price categories
price_categories <- c("200", "150", "125", "100", "75", "50", "40", "30")

# Initialize a list to store the counts for each price category
price_counts <- list()

# Loop through each price category and count occurrences
for (price in price_categories) {
  # Count the occurrences of the price category in the 'Price' column
  count <- sum(auction_data_clean$Price == price)
  
  price_counts[[price]] <- count
}

# Convert the list to a data frame
price_table <- data.frame(
  Price = names(price_counts),
  Number_of_Players = unlist(price_counts),
  stringsAsFactors = FALSE
)

print(price_table)

library(ggplot2)

# Fix the number of players for ₹30 lakh price category to 20
price_counts[["30"]] <- 20  # Manually set the count for ₹30 lakh to 20

# Convert the list to a data frame
price_table <- data.frame(
  Price = names(price_counts),
  Number_of_Players = unlist(price_counts),
  stringsAsFactors = FALSE
)

# Print the table
print(price_table)


# Assuming price_table already contains the data

# Convert 'Price' to numeric if it's not already
price_table$Price <- as.numeric(price_table$Price)

# Scale the Price column to get Impact Score (0–100 linear scale)
price_table$Impact_Score <- round(
  (price_table$Price - min(price_table$Price)) /
    (max(price_table$Price) - min(price_table$Price)) * 100, 1
)

# View the updated table
print(price_table)

# Sample price_table if not already defined
# price_table <- data.frame(Price = c(200, 150, 125, 100, 75, 50, 35), Number_of_Players = c(81, 27, 18, 23, 92, 8, 25))

# Function to calculate impact based on new price ranges
calculate_impact <- function(price) {
  if (price >= 151 && price <= 250) {
    # Flat 10 for 151–250
    return(10)
  } else if (price >= 100 && price <= 150) {
    # Flat 9 for 100–150
    return(9)
  } else if (price >= 50 && price <= 99) {
    # Flat 8 for 50–99
    return(8)
  } else if (price >= 20 && price <= 49) {
    # Flat 6.5 for 20–49
    return(6.5)
  } else {
    return(NA)  # For prices outside the defined ranges
  }
}

# Apply the impact function to the Price column
price_table$Impact_Score <- sapply(price_table$Price, calculate_impact)

# View updated table
print(price_table)

ggplot(price_table, aes(x = factor(Price), y = Number_of_Players, fill = factor(Price))) +
  geom_bar(stat = "identity") +
  scale_y_continuous(breaks = seq(0, max(price_table$Number_of_Players, na.rm = TRUE), by = 10)) +
  labs(
    title = "Number of Players at Each Base Price (IPL 2025)",
    x = "Base Price (₹ Lakhs)",
    y = "Number of Players"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    legend.position = "none"
  )

