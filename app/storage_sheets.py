from app.sheets import open_sheet


def load_data():
    """
    Loads transactions and budgets from Google Sheets.
    Returns a dict with keys: transactions, budgets
    """
    sheet = open_sheet()

    transactions_ws = sheet.worksheet("transactions")
    budgets_ws = sheet.worksheet("budgets")

    transactions = transactions_ws.get_all_records()
    budgets = budgets_ws.get_all_records()

    return {
        "transactions": transactions,
        "budgets": budgets,
    }


def append_transaction(transaction):
    # Appends one transaction row to the transactions worksheet.
    sheet = open_sheet()
    ws = sheet.worksheet("transactions")

    ws.append_row([
        transaction["id"],
        transaction["date"],
        transaction["type"],
        transaction["category"],
        transaction["amount"],
        transaction["note"],
    ])


def upsert_budget(budget):
    # Updates a budget if month+category exists, otherwise appends new row.
    sheet = open_sheet()
    ws = sheet.worksheet("budgets")

    records = ws.get_all_records()

    for idx, row in enumerate(records, start=2):
        same_month = str(row.get("month", "")).strip() == budget["month"]
        same_cat = (
            str(row.get("category", "")).strip().lower()
            == budget["category"].lower()
        )

        if same_month and same_cat:
            ws.update(f"C{idx}", [[budget["limit"]]])
            return

    ws.append_row([
        budget["month"],
        budget["category"],
        budget["limit"],
    ])
