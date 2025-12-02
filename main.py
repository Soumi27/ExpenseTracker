import csv
import datetime
import os

FILENAME = "expenses.csv"

# Simple ANSI color codes for decoration (they work in most terminals)
class Color:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def clear_screen():
    """Clear terminal screen for better UI (optional)."""
    os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    print(Color.CYAN + Color.BOLD + "=" * 50 + Color.RESET)
    print(Color.CYAN + Color.BOLD + "           💰 PERSONAL EXPENSE TRACKER          " + Color.RESET)
    print(Color.CYAN + Color.BOLD + "=" * 50 + Color.RESET)

def read_expenses():
    """Read all expenses from CSV and return as a list of rows."""
    expenses = []
    try:
        with open(FILENAME, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 4:
                    continue
                expenses.append(row)
    except FileNotFoundError:
        pass
    return expenses

def write_expenses(expenses):
    """Overwrite CSV with the given list of rows."""
    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(expenses)

def add_expense():
    clear_screen()
    print_banner()
    print(Color.BOLD + "➕ Add New Expense\n" + Color.RESET)

    # Date: allow custom date, default to today
    today = datetime.date.today()
    print(f"Press Enter for today's date ({today}) or enter a date as YYYY-MM-DD.")
    date_str = input("Date: ").strip()

    if date_str == "":
        date = today
    else:
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(Color.RED + "❌ Invalid date format! Using today's date instead.\n" + Color.RESET)
            date = today

    category = input("Enter category (Food, Travel, Bills, etc.): ").strip() or "Other"
    description = input("Enter description: ").strip() or "-"

    # Validate amount
    while True:
        amount_str = input("Enter amount: ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            print(Color.RED + "❌ Please enter a valid positive number for amount." + Color.RESET)

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])

    print(Color.GREEN + "\n✅ Expense added successfully!\n" + Color.RESET)
    input("Press Enter to return to menu...")

def view_expenses():
    clear_screen()
    print_banner()
    print(Color.BOLD + "📜 All Expenses\n" + Color.RESET)

    expenses = read_expenses()
    if not expenses:
        print(Color.YELLOW + "⚠️ No expenses found! Add some first.\n" + Color.RESET)
        input("Press Enter to return to menu...")
        return

    print(f"{'No.':<4} {'Date':<12} {'Category':<12} {'Description':<20} {'Amount (₹)':>10}")
    print("-" * 65)
    total = 0
    for idx, row in enumerate(expenses, start=1):
        date, category, description, amount = row
        try:
            amount_val = float(amount)
        except ValueError:
            amount_val = 0
        total += amount_val
        print(f"{idx:<4} {date:<12} {category:<12} {description:<20} {amount_val:>10.2f}")

    print("-" * 65)
    print(Color.GREEN + f"💡 Total spent: ₹{total:.2f}" + Color.RESET)
    print()
    input("Press Enter to return to menu...")

def expense_summary():
    clear_screen()
    print_banner()
    print(Color.BOLD + "📊 Expense Summary by Category\n" + Color.RESET)

    expenses = read_expenses()
    if not expenses:
        print(Color.YELLOW + "⚠️ No expenses found! Add some first.\n" + Color.RESET)
        input("Press Enter to return to menu...")
        return

    summary = {}
    for row in expenses:
        category, amount_str = row[1], row[3]
        try:
            amount = float(amount_str)
        except ValueError:
            continue
        summary[category] = summary.get(category, 0) + amount

    if not summary:
        print(Color.YELLOW + "⚠️ No valid amounts found in the file.\n" + Color.RESET)
        input("Press Enter to return to menu...")
        return

    print(f"{'Category':<15} {'Total (₹)':>12}")
    print("-" * 30)

    grand_total = 0
    top_category = None
    top_amount = 0

    for cat, total in summary.items():
        print(f"{cat:<15} {total:>12.2f}")
        grand_total += total
        if total > top_amount:
            top_amount = total
            top_category = cat

    print("-" * 30)
    print(Color.GREEN + f"Overall total: ₹{grand_total:.2f}" + Color.RESET)
    if top_category:
        print(Color.BLUE + f"⭐ Highest spending in: {top_category} (₹{top_amount:.2f})" + Color.RESET)
    print()
    input("Press Enter to return to menu...")

def delete_expense():
    clear_screen()
    print_banner()
    print(Color.BOLD + "🗑️ Delete an Expense\n" + Color.RESET)

    expenses = read_expenses()
    if not expenses:
        print(Color.YELLOW + "⚠️ No expenses to delete.\n" + Color.RESET)
        input("Press Enter to return to menu...")
        return

    # Show expenses with numbers
    print(f"{'No.':<4} {'Date':<12} {'Category':<12} {'Description':<20} {'Amount (₹)':>10}")
    print("-" * 65)
    for idx, row in enumerate(expenses, start=1):
        date, category, description, amount = row
        try:
            amount_val = float(amount)
        except ValueError:
            amount_val = 0
        print(f"{idx:<4} {date:<12} {category:<12} {description:<20} {amount_val:>10.2f}")
    print("-" * 65)

    while True:
        choice = input("Enter the expense number to delete (or 0 to cancel): ").strip()
        try:
            num = int(choice)
            if num == 0:
                print(Color.YELLOW + "↩️ Deletion cancelled." + Color.RESET)
                break
            if 1 <= num <= len(expenses):
                removed = expenses.pop(num - 1)
                write_expenses(expenses)
                print(Color.GREEN + f"✅ Deleted expense: {removed[0]} | {removed[1]} | {removed[2]} | ₹{removed[3]}" + Color.RESET)
                break
            else:
                print(Color.RED + "❌ Invalid number. Try again." + Color.RESET)
        except ValueError:
            print(Color.RED + "❌ Please enter a valid number." + Color.RESET)

    print()
    input("Press Enter to return to menu...")

def main():
    while True:
        clear_screen()
        print_banner()
        print("Please choose an option:\n")
        print("  1️⃣  Add Expense")
        print("  2️⃣  View All Expenses")
        print("  3️⃣  View Summary by Category")
        print("  4️⃣  Delete an Expense")
        print("  5️⃣  Exit\n")

        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            expense_summary()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            clear_screen()
            print_banner()
            print(Color.GREEN + "👋 Exiting... Have a great day!\n" + Color.RESET)
            break
        else:
            print(Color.RED + "❌ Invalid choice, press Enter and try again!" + Color.RESET)
            input()

if __name__ == "__main__":
    main()
