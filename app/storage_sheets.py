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


def upsert_budget(month: str, category: str, limit: float) -> bool:
    """
    Update budget if (month, category) exists, otherwise append.
    Returns True if updated, False if appended.
    """
    sheet = open_sheet()
    ws = sheet.worksheet("budgets")

    month = month.strip()
    category_norm = category.strip().lower()

    rows = ws.get_all_values()

    if not rows:
        ws.append_row(["month", "category", "limit"])
        ws.append_row([month, category.strip(), str(limit)])
        return False

    for i, row in enumerate(rows[1:], start=2):
        row_month = (row[0].strip() if len(row) > 0 else "")
        row_cat = (row[1].strip().lower() if len(row) > 1 else "")

        if row_month == month and row_cat == category_norm:
            ws.update_cell(i, 3, str(limit))
            return True

    ws.append_row([month, category.strip(), str(limit)])
    return False


def append_budget(budget):
    """
    Appends one budget row to the 'budgets' worksheet.
    Expected columns: month, category, limit
    """
    sheet = open_sheet()
    worksheet = sheet.worksheet("budgets")

    worksheet.append_row([
        budget["month"],
        budget["category"],
        budget["limit"],
    ])
