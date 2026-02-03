from app.sheets import open_sheet

sheet = open_sheet()
print("OK: opened spreadsheet:", sheet.title)

tx = sheet.worksheet("transactions").get_all_records()
bd = sheet.worksheet("budgets").get_all_records()

print("Transactions:", tx)
print("Budgets:", bd)