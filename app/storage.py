import json
import os

DATA_FILE_PATH = os.path.join("data", "budget_data.json")


def load_data():
    """
    Loads budget data from a JSON file.
    Returns a dictionary with keys: 'transactions' and 'budgets'.
    If the file is missing or invalid, returns safe defaults.
    """
    default_data = {"transactions": [], "budgets": []}

    if not os.path.exists(DATA_FILE_PATH):
        return default_data

    try:
        with open(DATA_FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return default_data

        data.setdefault("transactions", [])
        data.setdefault("budgets", [])
        return data

    except (json.JSONDecodeError, OSError):
        return default_data


def save_data(data):
    """
    Saves budget data to a JSON file.
    """
    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)