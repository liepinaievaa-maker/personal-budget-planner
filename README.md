![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

# Personal Budget Planner

## Project Overview

- Personal Budget Planner is a command-line Python application that helps users track income and expenses, set monthly budgets by category, view monthly financial reports, and export data to CSV files. The application is designed for users who want a simple, text-based tool to manage their personal finances without relying on spreadsheets or external services.

- The project is built using the Code Institute Python Essentials Template and is deployed to Heroku using a mock terminal interface.

## Target Audience

This application is intended for individuals who want a simple, text-based tool to track their personal finances. It is suitable for users who prefer a command-line interface and want to manage budgets without using spreadsheets or external financial applications.


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

-JSON was chosen for data storage because it is lightweight, human-readable, and well-suited for small to medium datasets used in command-line applications.

- Data is stored locally in a JSON file with the following structure:
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

- Manual testing was carried out during development to ensure the application behaves as expected.

## Bugs and Fixes

### Bug: Program would not run from root folder

- **Issue**: Running `python run.py` from the outer project folder caused a file not found error.
- **Fix**: Ensured the application is run from the inner project directory where `run.py` is located.

### Bug: Invalid menu input caused unexpected behaviour

- **Issue**: Users could enter non-numeric values at menus.
- **Fix**: Added input validation and defensive checks in all menu handlers.

## Libraries and Technologies Used

### Python Standard Library

- [json](https://docs.python.org/3/library/json.html)
   - Used for persistent storage of transactions and budgets.
- [csv](https://docs.python.org/3/library/csv.html) 
    - Used to export transaction data and reports.
- [datetime](https://docs.python.org/3/library/datetime.html)
   -  Used to validate date input.
- [os](https://docs.python.org/3/library/os.html)
   -  Used for file and folder handling.

### External Libraries

This project is based on the Code Institute Python Essentials Template, which includes:
- [gspread](https://pypi.org/project/gspread/)
- [google-auth](https://pypi.org/project/google-auth/)

These libraries were retained for template compatibility but are not directly used in this project.

## Deployment

The project is deployed to Heroku using the Code Institute Python Essentials Template.

Deployment steps:

1. Create a new Heroku app

2. Set the buildpacks to Python and Node.js

3. Connect the Heroku app to the GitHub repository

4. Deploy the main branch

## Credits

- Code Institute Python Essentials Template

- Python documentation

## Acknowledgements

This project was developed as Portfolio Project 3 for the Diploma in Full Stack Software Development at Code Institute.

## 

---
