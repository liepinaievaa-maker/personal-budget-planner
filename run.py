from app.storage import load_data, save_data
from datetime import datetime


def display_main_menu():
    """
    Displays the main menu options to the user.
    """
    print("\nPersonal Budget Planner")
    print("-" * 25)
    print("1. Transactions")
    print("2. Budgets")
    print("3. Reports")
    print("0. Exit")


def get_user_choice():
    """
    Gets the user's menu choice.
    """
    return input("Please choose an option: ").strip()


def prompt_for_date():
    """
    Prompts user for a date in YYYY-MM-DD format and validates it.
    Returns the date string.
    """
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def prompt_for_amount():
    """
    Prompts user for an amount and validates it as a positive number.
    Returns the amount as a float.
    """
    while True:
        amount_str = input("Enter amount (e.g. 12.50): ").strip().replace(",", ".")
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
    Prompts the user for transaction details, appends a new transaction
    to the data dict, and saves it.
    """
    print("\nAdd a Transaction")
    print("-" * 18)

    date_str = prompt_for_date()
    t_type = prompt_for_type()
    category = input("Category (e.g. Food, Rent): ").strip()
    note = input("Note (optional): ").strip()
    amount = prompt_for_amount()

    next_id = 1
    if data["transactions"]:
        next_id = max(t["id"] for t in data["transactions"]) + 1

    transaction = {
        "id": next_id,
        "date": date_str,
        "type": t_type,
        "category": category if category else "Uncategorized",
        "amount": amount,
        "note": note
    }

    data["transactions"].append(transaction)
    save_data(data)

    print(f"\nSaved transaction #{next_id} ({t_type}) - {amount:.2f}")


def view_transactions(data):
    """
    Displays all transactions in a readable format.
    """
    transactions = data["transactions"]

    if len(transactions) == 0:
        print("No transactions yet.\n")
        return

    print("All Transactions\n")
    print("-" * 17)

    for transaction in transactions:
        print(
            "ID:", transaction["id"],
            "| Date:", transaction["date"],
            "| Type:", transaction["type"],
            "| Category:", transaction["category"],
            "| Amount:", transaction["amount"],
            "| Note:", transaction["note"]
        )


def monthly_report(data):
    """
    Displays income, expenses, and balance for a given month.
    """
    month = prompt_for_month()

    income_total = 0
    expense_total = 0

    for transaction in data["transactions"]:
        if transaction["date"].startswith(month):
            if transaction["type"] == "income":
                income_total += transaction["amount"]
            elif transaction["type"] == "expense":
                expense_total += transaction["amount"]

    print("\nMonthly Report for", month)
    print("-" * 25)
    print("Total income:", income_total)
    print("Total expenses:", expense_total)
    print("Balance:", income_total - expense_total)


def transactions_flow(data):
    """
    Handles the transactions submenu loop.
    """
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
        if (budget["month"] == month and
                budget["category"].lower() == category.lower()):
            budget["category"] = category
            budget["limit"] = limit
            save_data(data)
            print(f"Updated budget for {category} in {month} to {limit:.2f}\n")
            return
    
    data["budgets"].append({
        "month": month,
        "category": category,
        "limit": limit
    })
    save_data(data)
    print(f"Saved budget for {category} in {month}: {limit:.2f}\n")


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
            spending_by_category[cat] = spending_by_category.get(cat, 0) + t["amount"]

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


def budgets_flow(data):
    """
    Handles the budgets submenu loop.
    """
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
    """
    Displays the budgets submenu options.
    """
    print("Budgets\n")
    print("-" * 7)
    print("1. Set monthly budget")
    print("2. View budget status")
    print("0. Back to main menu")


def prompt_for_month():
    """
    Prompts user for a month in YYYY-MM format.
    """
    while True:
        month = input("Enter month (YYYY-MM): ").strip()
        if len(month) == 7 and month[4] == "-":
            return month
        print("Invalid format. Please use YYYY-MM.")


def prompt_for_category():
    """
    Prompts user for a category name.
    """
    category = input("Enter category (e.g. Food): ").strip()
    return category if category else "Uncategorized"


def prompt_for_limit():
    """
    Prompts user for a positive budget limit.
    Returns float.
    """
    while True:
        limit_str = input("Enter budget limit (e.g. 250): ").strip().replace(",", ".")
        try:
            limit = float(limit_str)
            if limit <= 0:
                print("Limit must be greater than 0.")
                continue
            return limit
        except ValueError:
            print("Invalid number. Please enter a valid amount.")


def display_transactions_menu():
    """
    Displays the transactions submenu options.
    """
    print("\nTransactions")
    print("-" * 12)
    print("1. Add transaction")
    print("2. View transactions")
    print("0. Back to main menu")


def main():
    """
    Main application loop
    """
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
        elif choice == "0":
            print("Thank you for using Personal Budget Planner. Goodbye!\n")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.\n")


if __name__ == "__main__":
    main()