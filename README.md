# Expense Tracker

This is a command-line based Expense Tracker built with Python, using the pandas and numpy libraries for data manipulation and analysis.

## What the program does

The program reads expense data from a `expenses.csv` file, performs an analysis, and provides the following insights:
- A total spending overview, including the highest and lowest expenses.
- A detailed category-wise analysis showing total spend, number of transactions, and percentage of total spend per category.
- An optional pie chart visualization of the expense distribution.

It also includes bonus features such as:
- Filtering expenses by a specified date range.
- Dynamically adding new expenses to the dataset.
- Exporting the summary analysis to a `summary_report.csv` file.

## How to run it

1.  **Clone the repository or download the files.**
2.  **Install the required libraries:**
    ```bash
    pip install pandas numpy matplotlib
    ```
3.  **Run the script from your terminal:**
    ```bash
    python expense_tracker.py
    ```
4.  **Follow the on-screen prompts** to add new expenses or filter the analysis by date.

## Features Implemented

-   **Data Reading**: Reads expenses from a CSV file (`expenses.csv`).
-   **Spending Overview**: Calculates and displays total spending, highest expense, and lowest expense.
-   **Category Analysis**: Groups expenses by category and calculates total spend, transaction count, and percentage of total spend for each.
-   **Pie Chart Visualization**: Generates a pie chart to visualize the distribution of expenses across categories.
-   **Date Filtering (Bonus)**: Allows users to filter the expense analysis for a specific date range.
-   **Dynamic Expense Entry (Bonus)**: Allows users to add new expense records, which are saved to the CSV file.
-   **Report Export (Bonus)**: Saves the category-wise summary analysis to `summary_report.csv`.

## Sample Input (`expenses.csv`)

```csv
Date,Category,Amount,Description
2025-06-10,Food,150,Pizza at Dominos
2025-06-11,Transport,50,Rickshaw fare
2025-06-12,Rent,5000,June Rent
2025-06-12,Utilities,200,Electricity Bill
```

## Sample Output

```
--- Spending Overview ---
Total Amount Spent: 5,400.00

Highest Expense:
Date           2025-06-12
Category             Rent
Amount               5000
Description     June Rent
Name: 2, dtype: object

Lowest Expense:
Date              2025-06-11
Category           Transport
Amount                    50
Description    Rickshaw fare
Name: 1, dtype: object

--- Category-wise Analysis ---

Category: Food
  Total Amount: 150.00
  Transactions: 1
  Percentage: 2.78%

Category: Rent
  Total Amount: 5,000.00
  Transactions: 1
  Percentage: 92.59%

Category: Transport
  Total Amount: 50.00
  Transactions: 1
  Percentage: 0.93%

Category: Utilities
  Total Amount: 200.00
  Transactions: 1
  Percentage: 3.7%

--- Generating Pie Chart ---
(A window opens with the pie chart)
```

### Screenshot of Pie Chart

*(You can add a screenshot of the generated pie chart here.)*
![Pie Chart](https://i.imgur.com/example.png) <!--- Placeholder for a real screenshot -->
