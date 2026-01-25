![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Personal Budget Planner

## Project Overview

- Personal Budget Planner is a command-line Python application that helps users track income and expenses, set monthly budgets by category, view monthly financial reports, and export data to CSV files. The application is designed for users who want a simple, text-based tool to manage their personal finances without relying on spreadsheets or external services.

- The project is built using the Code Institute Python Essentials Template and is deployed to Heroku using a mock terminal interface.

## User Goals

- Record income and expense transactions

- View a list of all transactions

- See monthly summaries of income, expenses, and balance

- Set monthly budgets for spending categories

- Compare budgets against actual spending

- Export transactions and reports to CSV files

## Site Owner Goals

- Provide a clear, easy-to-use command-line interface

- Ensure all user input is validated to prevent errors

- Store data persistently between sessions

- Demonstrate clean, well-structured Python code


## Application Features

### Main Menu

The main menu allows the user to navigate between:

- Transactions

- Budgets

- Reports

- CSV Export

- Exit

The application runs in a loop until the user chooses to exit.

### Transactions

- Add a transaction with date, type (income/expense), category, amount, and optional note

- View all saved transactions

- Transactions are stored persistently in a JSON file

### Monthly Reports

- Generate a monthly report by entering a month in YYYY-MM format

- Displays total income, total expenses, and balance for the selected month

### Budgets

- Set or update a monthly budget for a specific category

- View budget status for a selected month

- Shows spending, remaining budget, or overspend amount

### CSV Export

- Export all transactions to transactions.csv

- Export a monthly summary report to monthly_report_YYYY-MM.csv

## Data Model

Data is stored locally in a JSON file with the following structure:
{
  "transactions": [
    {
      "id": 1,
      "date": "2026-01-20",
      "type": "income",
      "category": "food",
      "amount": 45.8,
      "note": "no"
    },
    {
      "id": 2,
      "date": "2026-01-29",
      "type": "expense",
      "category": "rent",
      "amount": 790.0,
      "note": ""
    }
  ],
  "budgets": [
    {
      "month": "2026-01",
      "category": "rent",
      "limit": 800.0
    }
  ]
}

## Program Flow

- The application starts in run.py

- Data is loaded from the JSON file on startup

- User input is handled through dedicated prompt functions

- Feature-specific logic is separated into reusable functions

- Data is saved back to the JSON file after changes

## Input Validation and Error Handling

- All numeric inputs are validated to ensure correct format and range

- Date and month inputs are validated to prevent invalid values

- Menus handle invalid selections gracefully without crashing

## Testing

## Libraries and Technologies Used

## Deployment

## Credits

## Acknowledgements

## 

---

Happy coding!
