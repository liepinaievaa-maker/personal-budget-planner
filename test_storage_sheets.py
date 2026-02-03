from app.storage_sheets import load_data

data = load_data()
print("Transactions loaded:", len(data["transactions"]))
print("Budgets loaded:", len(data["budgets"]))
