import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Configure matplotlib backend for better compatibility
plt.switch_backend('Agg')  # Use non-interactive backend

# Ensure all rows are displayed in the output
pd.set_option('display.max_rows', None)

def add_expense():
    """
    Prompts the user to add a new expense and saves it to the CSV.
    """
    print("\n--- Add New Expense ---")
    try:
        date = input("Enter date (YYYY-MM-DD): ")
        # Validate date format
        datetime.strptime(date, '%Y-%m-%d')

        category = input("Enter category: ")
        amount = float(input("Enter amount: "))
        description = input("Enter description: ")

        new_expense = pd.DataFrame([[date, category, amount, description]], columns=['Date', 'Category', 'Amount', 'Description'])
        
        # Check if file exists to determine if we need headers
        file_exists = os.path.exists('expenses.csv')
        new_expense.to_csv('expenses.csv', mode='a', header=not file_exists, index=False)
        print("Expense added successfully!")

    except ValueError:
        print("Invalid input. Please check date format (YYYY-MM-DD) or amount.")
    except Exception as e:
        print(f"An error occurred: {e}")

def expense_analysis():
    """
    Reads expense data from a CSV file and performs a basic analysis.
    """
    try:
        # Check if file exists
        if not os.path.exists('expenses.csv'):
            print("Error: 'expenses.csv' not found. Please add some expenses first.")
            return
            
        # Read the data from expenses.csv
        df = pd.read_csv('expenses.csv')
        
        # Check if DataFrame is empty
        if df.empty:
            print("No expenses found in the CSV file.")
            return
        df['Date'] = pd.to_datetime(df['Date']) # Convert Date column to datetime objects

        # --- Bonus: Filter by Date ---
        filter_choice = input("Do you want to filter expenses by date? (yes/no): ").lower()
        if filter_choice == 'yes':
            start_date_str = input("Enter start date (YYYY-MM-DD): ")
            end_date_str = input("Enter end date (YYYY-MM-DD): ")
            try:
                start_date = pd.to_datetime(start_date_str)
                end_date = pd.to_datetime(end_date_str)
                df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
            except ValueError:
                print("Invalid date format. Skipping filter.")

        # --- 1. Total Spending Overview ---
        print("--- Spending Overview ---")

        # Calculate the total amount spent
        total_spent = np.sum(df['Amount'])
        if total_spent == 0:
            print("No expenses found in the selected range.")
            return

        print(f"Total Amount Spent: ${total_spent:,.2f}")

        # Find the highest expense (with safety check)
        if not df.empty:
            highest_expense = df.loc[df['Amount'].idxmax()]
            print("\nHighest Expense:")
            print(highest_expense)

            # Find the lowest expense (with safety check)
            lowest_expense = df.loc[df['Amount'].idxmin()]
            print("\nLowest Expense:")
            print(lowest_expense)

        # --- 2. Category-wise Analysis ---
        print("\n--- Starting Category-wise Analysis ---")
        # Group by category and calculate sum and count
        category_analysis = df.groupby('Category')['Amount'].agg(TotalAmount='sum', Transactions='count').reset_index()
        print("\n--- DataFrame after Grouping and Aggregation ---")
        print(category_analysis)

        # Calculate the percentage of total spending for each category
        category_analysis['Percentage'] = (category_analysis['TotalAmount'] / total_spent * 100).round(2)
        print("\n--- DataFrame after Calculating Percentages ---")
        print(category_analysis)

        # --- Bonus: Export Summary Report ---
        try:
            category_analysis.to_csv('summary_report.csv', index=False)
            print("\nSummary report 'summary_report.csv' generated successfully.")
        except Exception as e:
            print(f"\nError exporting summary report: {e}")

        print("\n--- Final Output Loop ---")
        # Print each row of the category analysis
        for index, row in category_analysis.iterrows():
            print(f"\nProcessing row {index}:")
            print(row)
            print(f"\nCategory: {row['Category']}")
            print(f"  Total Amount: ${row['TotalAmount']:,.2f}")
            print(f"  Transactions: {row['Transactions']}")
            print(f"  Percentage: {row['Percentage']}%")

        # --- 3. Optional Visual (Bonus) ---
        print("\n--- Generating Pie Chart ---")
        try:
            plt.figure(figsize=(10, 7))
            plt.pie(category_analysis['TotalAmount'], labels=category_analysis['Category'], autopct='%1.1f%%', startangle=140)
            plt.title('Expense Distribution by Category')
            plt.ylabel('') # Hide the y-label
            
            # Save the plot instead of showing it (more reliable)
            plt.savefig('expense_pie_chart.png', dpi=300, bbox_inches='tight')
            print("Pie chart saved as 'expense_pie_chart.png'")
            plt.close()  # Close the figure to free memory
        except Exception as e:
            print(f"Error generating pie chart: {e}")

    except FileNotFoundError:
        print("Error: 'expenses.csv' not found. Please make sure the file exists in the same directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Ask user if they want to add an expense
    add_choice = input("Do you want to add a new expense? (yes/no): ").lower()
    if add_choice == 'yes':
        add_expense()
        
    expense_analysis()
