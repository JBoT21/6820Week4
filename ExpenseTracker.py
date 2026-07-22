import csv
import os
from datetime import datetime
from collections import defaultdict

FILENAME = "expenses.csv"

FIELDS = ["Date", "Category", "Description", "Amount"]


def initialize_file():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDS)


def load_expenses():
    expenses = []

    with open(FILENAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["Amount"] = float(row["Amount"])
            expenses.append(row)

    return expenses


def save_expense(expense):
    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            expense["Date"],
            expense["Category"],
            expense["Description"],
            expense["Amount"]
        ])


def add_expense():
    print("\nAdd New Expense")

    category = input("Category: ").strip()
    description = input("Description: ").strip()

    while True:
        try:
            amount = float(input("Amount: $"))
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            print("Enter a positive number.")

    date = input("Date (YYYY-MM-DD) [today]: ").strip()

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    expense = {
        "Date": date,
        "Category": category,
        "Description": description,
        "Amount": amount
    }

    save_expense(expense)
    print("Expense saved.")


def view_expenses():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses recorded.")
        return

    print("\nExpenses")
    print("-" * 70)

    total = 0

    for item in expenses:
        print(
            f"{item['Date']:12}"
            f"{item['Category']:15}"
            f"{item['Description']:25}"
            f"${item['Amount']:8.2f}"
        )
        total += item["Amount"]

    print("-" * 70)
    print(f"Total: ${total:.2f}")


def search_category():
    category = input("\nCategory to search: ").strip().lower()

    expenses = load_expenses()

    found = False
    total = 0

    for item in expenses:
        if item["Category"].lower() == category:
            found = True
            print(
                f"{item['Date']} | "
                f"{item['Description']} | "
                f"${item['Amount']:.2f}"
            )
            total += item["Amount"]

    if found:
        print(f"Category Total: ${total:.2f}")
    else:
        print("No matching expenses found.")


def monthly_summary():
    expenses = load_expenses()

    summary = defaultdict(float)

    for item in expenses:
        month = item["Date"][:7]
        summary[month] += item["Amount"]

    if not summary:
        print("No expense data.")
        return

    print("\nMonthly Summary")

    for month in sorted(summary):
        print(f"{month}: ${summary[month]:.2f}")


def highest_expense():
    expenses = load_expenses()

    if not expenses:
        print("No expenses available.")
        return

    highest = max(expenses, key=lambda x: x["Amount"])

    print("\nLargest Expense")
    print(f"Date: {highest['Date']}")
    print(f"Category: {highest['Category']}")
    print(f"Description: {highest['Description']}")
    print(f"Amount: ${highest['Amount']:.2f}")


def export_report():
    expenses = load_expenses()

    report_name = "expense_report.txt"

    with open(report_name, "w") as report:
        report.write("Expense Report\n")
        report.write("=" * 40 + "\n\n")

        total = 0

        category_totals = defaultdict(float)

        for item in expenses:
            report.write(
                f"{item['Date']} | "
                f"{item['Category']} | "
                f"{item['Description']} | "
                f"${item['Amount']:.2f}\n"
            )

            total += item["Amount"]
            category_totals[item["Category"]] += item["Amount"]

        report.write("\n")
        report.write("=" * 40 + "\n")
        report.write(f"Overall Total: ${total:.2f}\n\n")

        report.write("Totals by Category\n")
        report.write("-" * 20 + "\n")

        for category in sorted(category_totals):
            report.write(
                f"{category}: ${category_totals[category]:.2f}\n"
            )

    print(f"Report exported to '{report_name}'.")


def menu():
    initialize_file()

    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search by Category")
        print("4. Monthly Summary")
        print("5. Highest Expense")
        print("6. Export Report")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            search_category()

        elif choice == "4":
            monthly_summary()

        elif choice == "5":
            highest_expense()

        elif choice == "6":
            export_report()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid selection.")


if __name__ == "__main__":
    menu()
