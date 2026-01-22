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
        
        if choice == "1":
            print("Transactions feature coming soon.\n")
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