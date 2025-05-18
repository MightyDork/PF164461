import json
import os
from src.accounts import Account
from datetime import date


def save_accounts_to_file(accounts: list[Account], filename: str) -> None:
    with open(filename, 'w') as f:
        json.dump([account.to_dict() for account in accounts], f)

def load_accounts_from_file(filename: str) -> list[Account]:
    with open(filename, 'r') as f:
        data = json.load(f)
        accounts = []
        for item in data:
            if 'creation_date' in item and item['creation_date'] is not None:
                item['creation_date'] = date.fromisoformat(item['creation_date'])
            else:
                item['creation_date'] = date.today()
            accounts.append(Account(**item))
        return accounts

def save_transaction_history(history: list[dict], filename: str) -> None:
    # save transaction history to json file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(history, f)

def load_transaction_history(filename: str) -> list[dict]:
    # load transaction history from json file
    if not os.path.exists(filename):
        raise FileNotFoundError(f"file '{filename}' does not exist")

    with open(filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError("invalid transaction history format") from e
