import csv
import os
from app.storage_sheets import load_data, append_transaction, append_budget
from datetime import datetime
from tabulate import tabulate


MIN_YEAR = 2000
MAX_YEAR = 3000
MAX_BUDGET_LIMIT = 500000


def pause():
    input("Press Enter to continue...\n")


def show_intro():
    # Displays the introductory text for the application.
    intro_text = (
        "Personal Budget Planner\n"
        "----------------------\n"
        "Purpose: Track your income and expenses, set monthly budgets,"
        " and\n"
        "view monthly reports.\n\n"
        "How to use:\n"
        "1) Transactions: add/view income and expenses\n"
        "2) Budgets: set a monthly limit per category\n"
        "3) Reports: view monthly totals\n"
        "4) Export: save transactions/reports to CSV\n\n"
        "Tip: You will see menu options next. Use 0 in menus to go\n"
        "back or exit.\n"
    )
    print(intro_text)
    input("Press Enter to continue...")


def display_main_menu():
    # Displays the main menu options to the user.
    menu_text = (
        "Personal Budget Planner\n"
        "-------------------------\n"
        "1. Transactions\n"
        "2. Budgets\n"
        "3. Reports\n"
        "4. Export\n"
        "0. Exit\n"
    )
    print(menu_text)


def confirm_action(message="Is this correct? (y/n): "):
    while True:
        answer = input(message).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def get_user_choice():
    # Gets the user's menu choice.
    return input("Please choose an option: ").strip()


def prompt_for_date():
    """
    Prompts user for a date in YYYY-MM-DD format and validates it.
    Checks if the year is within the allowed range.
    Returns the date string.
    """
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if date_obj.year < MIN_YEAR or date_obj.year > MAX_YEAR:
                print(f"Year must be between {MIN_YEAR} and {MAX_YEAR}.")
                continue
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def prompt_for_amount():
    """
    Prompts user for an amount and validates it as a positive number.
    Returns the amount as a float.
    """
    while True:
        amount_str = input("Enter amount (e.g. 12.50): ")
        amount_str = amount_str.strip().replace(",", ".")
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a number (e.g. 12.50).")


def prompt_for_type():
    """
    Prompts user for transaction type: income or expense.
    Returns 'income' or 'expense'.
    """
    while True:
        t_type = input("Type (income/expense): ").strip().lower()
        if t_type in ("income", "expense"):
            return t_type
        print("Invalid type. Please enter 'income' or 'expense'.")


def add_transaction(data):
    """
    Prompts the user for transaction details and saves it to Google Sheets
    after confirmation.
    """
    print("Add a Transaction \n")
    print("-" * 18)

    date_str = prompt_for_date()
    t_type = prompt_for_type()
    if t_type == "income":
        print("\nIncome category examples: Salary, Bonus, Gift")
    else:
        print("\nExpense category examples: Food, Transport, Rent")
    category = prompt_for_category()
    note = input("Note (optional): ").strip()
    amount = prompt_for_amount()

    next_id = 1
    if data["transactions"]:
        next_id = max(t["id"] for t in data["transactions"]) + 1

    transaction = {
        "id": next_id,
        "date": date_str,
        "type": t_type,
        "category": category,
        "amount": amount,
        "note": note
    }

    print("Please confirm your transaction:\n")
    print(f"Date: {date_str}")
    print(f"Type: {t_type}")
    print(f"Category: {category}")
    print(f"Amount: {amount:.2f}")
    print(f"Note: {note if note else '(none)'}")

    if not confirm_action():
        print("Transaction cancelled. Nothing was saved.\n")
        return

    append_transaction(transaction)
    data["transactions"].append(transaction)
    print("\nTransaction saved.\n")


def view_transactions(data):
    # Displays all transactions in a readable format.
    transactions = data["transactions"]

    if len(transactions) == 0:
        print("\nNo transactions yet.\n")
        pause()
        return

    rows = []
    for t in transactions:
        rows.append([
            t["id"],
            t["date"],
            t["type"],
            t["category"],
            f'{float(t["amount"]):.2f}',
            t["note"] or ""
        ])

    print("\nAll Transactions\n")
    headers = ["ID", "Date", "Type", "Category", "Amount", "Note"]
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    pause()


def monthly_report(data):
    # Displays income, expenses, and balance for a given month.
    date_str = prompt_for_date()
    month = date_str[:7]

    income_total = 0
    expense_total = 0
    matches = 0

    for transaction in data["transactions"]:
        if transaction["date"].startswith(month):
            matches += 1
            if transaction["type"] == "income":
                income_total += transaction["amount"]
            elif transaction["type"] == "expense":
                expense_total += transaction["amount"]

    if matches == 0:
        print(f"No transactions found for {month}.\n")
        return

    print("Monthly Report for", month)
    print("-" * 25)
    print("Total income:", income_total)
    print("Total expenses:", expense_total)
    print("Balance:", income_total - expense_total)


def transactions_flow(data):
    # Handles the transactions submenu loop.
    while True:
        display_transactions_menu()
        choice = get_user_choice()

        if choice == "1":
            add_transaction(data)
        elif choice == "2":
            view_transactions(data)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a number from the menu.\n")


def set_budget(data):
    """
    Adds or updates a monthly budget for a category.
    Check if the budget exists for the month and category.
    And then if not found, create new one.
    """
    print("Set Monthly Budget\n")
    print("-" * 18)

    month = prompt_for_month()
    category = prompt_for_category()
    limit = prompt_for_limit()

    for budget in data["budgets"]:
        if (
            budget["month"] == month
            and budget["category"].lower() == category.lower()
        ):
            budget["category"] = category
            budget["limit"] = limit

            budget_data = {
                "month": month,
                "category": category,
                "limit": limit
            }
            append_budget(budget_data)
            print(f"Updated budget for {category} in {month} to {limit:.2f}\n")
            return

    print("\n Please confirm your budget:")
    print(f"Month: {month}")
    print(f"Category: {category}")
    print(f"Limit: {limit:.2f}")

    if not confirm_action():
        print("Budget cancelled. Nothing was saved.\n")
        return

    new_budget = {
        "month": month,
        "category": category,
        "limit": limit
        }

    append_budget(new_budget)
    data["budgets"].append(new_budget)

    print(f"Saved budget for {category} in {month}: {limit:.2f}\n")

    pause()


def view_budget_status(data):
    """
    Shows budget usage for a given month by category.
    And calculate it by the month.
    """
    month = prompt_for_month()

    spending_by_category = {}

    for t in data["transactions"]:
        if t["date"].startswith(month) and t["type"] == "expense":
            cat = t["category"]
            spending_by_category[cat] = (
                spending_by_category.get(cat, 0) + t["amount"]
            )

    budgets_for_month = [b for b in data["budgets"] if b["month"] == month]

    print(f"\nBudget Status for {month}")
    print("-" * 22)

    if len(budgets_for_month) == 0:
        print("No budgets set for this month.")
        return

    for b in budgets_for_month:
        cat = b["category"]
        limit = b["limit"]
        spent = spending_by_category.get(cat, 0)
        remaining = limit - spent

        print(f"\nCategory: {cat}")
        print(f"Limit: {limit:.2f}")
        print(f"Spent: {spent:.2f}")

        if remaining >= 0:
            print(f"Remaining: {remaining:.2f}")
        else:
            print(f"Overspent by: {abs(remaining):.2f}")

    if len(data["budgets"]) == 0:
        print("No budgets have been created yet.\n")
        return


def budgets_flow(data):
    # Handles the budgets submenu loop.
    while True:
        display_budgets_menu()
        choice = get_user_choice()

        if choice == "1":
            set_budget(data)
        elif choice == "2":
            view_budget_status(data)
        elif choice == "0":
            break
        else:
            print("\nInvalid choice. Please enter a number from the menu.")


def display_budgets_menu():
    # Displays the budgets submenu options.
    print("Budgets\n")
    print("-" * 7)
    print("1. Set monthly budget")
    print("2. View budget status")
    print("0. Back to main menu")


def prompt_for_month():
    # Prompts user for a month in YYYY-MM format.
    while True:
        month = input("Enter month (YYYY-MM): ").strip()
        if len(month) == 7 and month[4] == "-":
            return month
        print("Invalid format. Please use YYYY-MM.")


def prompt_for_category():
    """
    Prompts user for a category name.
    Category cannot be empty.
    """
    while True:
        category = input("Enter category (e.g. Food): ").strip()
        if category:
            return category.strip().title()
        print("Category cannot be empty. Please enter a category.")


def prompt_for_limit():
    """
    Prompts user for a positive budget limit and
    the persons input here should be positive only.
    Returns float.
    """
    while True:
        limit_str = input("Enter budget limit (e.g. 250): ")
        limit_str = limit_str.strip().replace(",", ".")
        try:
            limit = float(limit_str)
            if limit <= 0:
                print("Limit must be greater than 0.")
                continue
            if limit > MAX_BUDGET_LIMIT:
                print(f"Limit must be {MAX_BUDGET_LIMIT} or less.")
                continue
            return limit
        except ValueError:
            print("Invalid number. Please enter a valid amount.")


def display_export_menu():
    # Displays export submenu options.
    print("\nExport")
    print("-" * 6)
    print("1. Export all transactions (CSV)")
    print("2. Export monthly summary report (CSV)")
    print("0. Back to main menu")


def export_flow(data):
    # Handles the export submenu loop.
    while True:
        display_export_menu()
        choice = get_user_choice()

        if choice == "1":
            export_transactions_csv(data)
        elif choice == "2":
            export_monthly_report_csv(data)
        elif choice == "0":
            break
        else:
            print("\nInvalid choice. Please enter a number from the menu.")


def export_monthly_report_csv(data):
    # Exports a monthly income/expense/balance report to a CSV file.
    month = prompt_for_month()

    income_total = 0
    expense_total = 0

    for t in data["transactions"]:
        if t["date"].startswith(month):
            if t["type"] == "income":
                income_total += t["amount"]
            elif t["type"] == "expense":
                expense_total += t["amount"]

    balance = income_total - expense_total

    os.makedirs("exports", exist_ok=True)
    file_path = os.path.join("exports", f"monthly_report_{month}.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["month", "total_income", "total_expenses", "balance"])
        writer.writerow([month, income_total, expense_total, balance])

    print(f"Exported monthly report to {file_path}\n")

    pause()


def export_transactions_csv(data):
    """
    Exports all transactions to
    a CSV file in the exports folder.
    """
    os.makedirs("exports", exist_ok=True)
    file_path = os.path.join("exports", "transactions.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "date", "type", "category", "amount", "note"])

        for t in data["transactions"]:
            writer.writerow([
                t["id"],
                t["date"],
                t["type"],
                t["category"],
                t["amount"],
                t["note"]
            ])

    print(f"Exported transactions to {file_path}\n")

    pause()


def display_transactions_menu():
    #  Displays the transactions submenu options.
    print("\nTransactions")
    print("-" * 12)
    print("1. Add transaction")
    print("2. View transactions")
    print("0. Back to main menu")


def main():
    # Main application loop.
    show_intro()
    data = load_data()

    while True:
        print(f"\nLoaded {len(data['transactions'])} transactions.")
        display_main_menu()
        choice = get_user_choice()

        if choice == "1":
            transactions_flow(data)
        elif choice == "2":
            budgets_flow(data)
        elif choice == "3":
            monthly_report(data)
        elif choice == "4":
            export_flow(data)
        elif choice == "0":
            print("Thank you for using Personal Budget Planner. Goodbye!\n")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.\n")


if __name__ == "__main__":
    main()
