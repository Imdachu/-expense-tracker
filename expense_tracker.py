import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Setting up matplotlib to avoid display issues (especially on systems without GUIs)
plt.switch_backend('Agg')  # Use non-interactive backend

# Making sure we can see all rows in DataFrame outputs
pd.set_option('display.max_rows', None)

def add_expense():
    """
    Prompts the user to add a new expense and saves it to the CSV.
    """
    print("\n--- Add New Expense ---")
    try:
        date = input("Enter date (YYYY-MM-DD): ")
        # Just double-checking if the user entered the date in the correct format
        datetime.strptime(date, '%Y-%m-%d')

        category = input("Enter category: ")
        amount = float(input("Enter amount: "))
        description = input("Enter description: ")

        new_expense = pd.DataFrame([[date, category, amount, description]], columns=['Date', 'Category', 'Amount', 'Description'])
        
        # If the file already exists, we won't add the header again
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
        # Converting date strings into actual datetime objects
        df['Date'] = pd.to_datetime(df['Date'])

        # Giving users the option to focus on specific dates
        filter_choice = input("Do you want to filter expenses by date? (yes/no): ").lower()
        if filter_choice == 'yes':
            start_date_str = input("Enter start date (YYYY-MM-DD): ")
            end_date_str = input("Enter end date (YYYY-MM-DD): ")
            try:
                start_date = pd.to_datetime(start_date_str)
                end_date = pd.to_datetime(end_date_str)
                df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
            except ValueError:
                print("Hmm... that date format doesn't look right. Skipping date filter.")

        # Let's give you an overview of your total spending
        print("--- Spending Overview ---")

        # Calculate the total amount spent
        total_spent = np.sum(df['Amount'])
        if total_spent == 0:
            print("No expenses found in the selected range.")
            return

        print(f"Total Amount Spent: ${total_spent:,.2f}")

        # Let's show you the highest and lowest expenses
        if not df.empty:
            highest_expense = df.loc[df['Amount'].idxmax()]
            print("\nHighest Expense:")
            print(highest_expense)

            # Find the lowest expense (with safety check)
            lowest_expense = df.loc[df['Amount'].idxmin()]
            print("\nLowest Expense:")
            print(lowest_expense)

        # Now let's dive into how much you've spent in each category
        print("\n--- Starting Category-wise Analysis ---")
        # Group by category and calculate sum and count
        category_analysis = df.groupby('Category')['Amount'].agg(TotalAmount='sum', Transactions='count').reset_index()
        print("\n--- DataFrame after Grouping and Aggregation ---")
        print(category_analysis)

        # Let's see what share each category holds in your total expenses
        category_analysis['Percentage'] = (category_analysis['TotalAmount'] / total_spent * 100).round(2)
        print("\n--- DataFrame after Calculating Percentages ---")
        print(category_analysis)

        # Let's also give you a CSV summary report to keep for records
        try:
            category_analysis.to_csv('summary_report.csv', index=False)
            print("\nSummary report 'summary_report.csv' generated successfully.")
        except Exception as e:
            print(f"\nError exporting summary report: {e}")

        print("\n--- Final Output Loop ---")
        # Giving you a friendly breakdown for each category
        for index, row in category_analysis.iterrows():
            print(f"\nProcessing row {index}:")
            print(row)
            print(f"\nCategory: {row['Category']}")
            print(f"  Total Amount: ${row['TotalAmount']:,.2f}")
            print(f"  Transactions: {row['Transactions']}")
            print(f"  Percentage: {row['Percentage']}%")

        # Time for a visual – a pie chart to help you see the distribution at a glance
        print("\n--- Generating Pie Chart ---")
        try:
            plt.figure(figsize=(10, 7))
            plt.pie(category_analysis['TotalAmount'], labels=category_analysis['Category'], autopct='%1.1f%%', startangle=140)
            plt.title('Expense Distribution by Category')
            # No need for a y-label here
            plt.ylabel('') 
            
            # Save the chart as an image file for easy viewing later
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
    # Asking the user if they'd like to log a new expense first
    add_choice = input("Do you want to add a new expense? (yes/no): ").lower()
    if add_choice == 'yes':
        add_expense()
        
    # Either way, we'll run the analysis after that
    expense_analysis()
