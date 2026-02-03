import json
import os

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]


def get_client():
    creds_json = os.environ.get("CREDS")
    if not creds_json:
        raise ValueError("Missing CREDS environment variable.")

    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
    return gspread.authorize(creds)


def open_sheet():
    sheet_name = os.environ.get("SHEET_NAME")
    if not sheet_name:
        raise ValueError("Missing SHEET_NAME environment variable.")

    client = get_client()
    return client.open(sheet_name)


def get_transactions():
    sheet = open_sheet()
    ws = sheet.worksheet("transactions")
    return ws.get_all_records()


def get_budgets():
    sheet = open_sheet()
    ws = sheet.worksheet("budgets")
    return ws.get_all_records()