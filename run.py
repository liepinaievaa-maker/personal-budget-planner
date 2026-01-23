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
            print("Budgets feature coming soon.\n")
        elif choice == "3":
            print("Reports feature coming soon.\n")
        elif choice == "0":
            print("Thank you for using Personal Budget Planner. Goodbye!\n")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.\n")


if __name__ == "__main__":
    main()