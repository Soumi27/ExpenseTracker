import csv
import datetime

FILENAME = "expenses.csv"

# Function to add an expense
def add_expense():
    date = datetime.date.today()
    category = input("Enter category (Food, Travel, Bills, etc.): ")
    description = input("Enter description : ")
    amount = float(input("Enter amount: "))

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])
    print("✅ Expense added successfully!\n")

# Function to view all expenses
def view_expenses():
    try:
        with open(FILENAME, "r") as file:
            reader = csv.reader(file)
            print("\nDate       | Category   | Description       | Amount")
            print("-"*55)
            for row in reader:
                print(f"{row[0]} | {row[1]:10} | {row[2]:15} | ₹{row[3]}")
    except FileNotFoundError:
        print("⚠️ No expenses found! Add some first.\n")

# Function to view summary by category
def expense_summary():
    summary = {}
    try:
        with open(FILENAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                category, amount = row[1], float(row[3])
                summary[category] = summary.get(category, 0) + amount

        print("\nExpense Summary by Category:")
        print("-"*30)
        for cat, total in summary.items():
            print(f"{cat}: ₹{total}")
    except FileNotFoundError:
        print("⚠️ No expenses found! Add some first.\n")

# Main menu
def main():
    while True:
        print("\n==== Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Summary")
        print("4. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            expense_summary()
        elif choice == "4":
            print("👋 Exiting... Have a great day!")
            break
        else:
            print("❌ Invalid choice, try again!\n")

if __name__ == "__main__":
    main()
