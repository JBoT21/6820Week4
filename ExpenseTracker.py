import csv
import os
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

FILENAME = "expenses.csv"

FIELDS = ["Date", "Category", "Description", "Amount"]


def get_non_empty_string(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("Input cannot be empty.")


def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))

            if value <= 0:
                print("Amount must be greater than zero.")
            else:
                return value

        except ValueError:
            print("Please enter a valid number.")

def get_valid_date(prompt):
    while True:
        value = input(prompt).strip()

        if value == "":
            return datetime.today().strftime("%Y-%m-%d")

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value

        except ValueError:
            print("Please enter the date as YYYY-MM-DD.")

def get_menu_choice(minimum, maximum):
    while True:
        choice = input("Choose an option: ").strip()

        if choice.isdigit():
            choice = int(choice)

            if minimum <= choice <= maximum:
                return choice

        print(f"Please enter a number from {minimum} to {maximum}.")

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

    category = get_non_empty_string("Category: ")
    description = get_non_empty_string("Description: ")
    amount = get_positive_float("Amount: $")
    date = get_valid_date("Date (YYYY-MM-DD) [Press Enter for today]: ")

    expense = {
        "Date": date,
        "Category": category,
        "Description": description,
        "Amount": amount
    }

    save_expense(expense)
    print("\nExpense saved successfully!")


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
    category = get_non_empty_string(
        "\nCategory to search: "
    ).lower()

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
        print(f"\nCategory Total: ${total:.2f}")
    else:
        print("\nNo matching expenses found.")


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


def monthly_spending_graph():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses to graph.")
        return

    monthly_totals = defaultdict(float)

    for expense in expenses:
        date = datetime.strptime(
            expense["Date"],
            "%Y-%m-%d"
        )

        month = date.strftime("%Y-%m")
        monthly_totals[month] += expense["Amount"]

    months = sorted(monthly_totals.keys())
    totals = [monthly_totals[m] for m in months]

    plt.figure(figsize=(10, 5))

    plt.plot(
        months,
        totals,
        marker="o",
        linewidth=2
    )

    plt.fill_between(months, totals, alpha=0.25)

    for month, total in zip(months, totals):
        plt.text(
            month,
            total,
            f"${total:.0f}",
            ha="center",
            va="bottom"
        )

    plt.title("Monthly Spending")
    plt.xlabel("Month")
    plt.ylabel("Total Spent ($)")
    plt.grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


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
        print("7. Monthly Spending Graph")
        print("8. Exit")

        choice = get_menu_choice(1, 8)

        if choice == 1:
            add_expense()

        elif choice == 2:
            view_expenses()

        elif choice == 3:
            search_category()

        elif choice == 4:
            monthly_summary()

        elif choice == 5:
            highest_expense()

        elif choice == 6:
            export_report()

        elif choice == 7:
            monthly_spending_graph()

        elif choice == 8:
            print("\nExiting Expense Tracker. Goodbye!")
            break


if __name__ == "__main__":
    menu()
