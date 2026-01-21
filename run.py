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


def main():
    """
    Main application loop
    """
    while True:
        display_main_menu()
        choice = get_user_choice()

        if choice == "0":
            print("Thank you for using Personal Budget Planner. Goodbye!\n")
            break
        else:
            print(f"You selected: {choice}\n")


if __name__ == "__main__":
    main()