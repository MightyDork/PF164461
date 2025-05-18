import unittest
import tempfile
import os
import json
from src.accounts import Account
from src.storage import save_accounts_to_file, load_accounts_from_file, save_transaction_history, load_transaction_history


class TestStorage(unittest.TestCase):

    def setUp(self):
        # create sample accounts and history
        self.account1 = Account("A001", "Alice", 100.0)
        self.account2 = Account("A002", "Bob", 200.0)
        self.accounts = [self.account1, self.account2]

        self.history = [
            {"type": "deposit", "account": "A001", "amount": 100.0},
            {"type": "withdraw", "account": "A002", "amount": 50.0}
        ]

    def test_save_and_load_accounts(self):
        # save accounts to file and read back
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            save_accounts_to_file(self.accounts, tmp.name)
            tmp_path = tmp.name

        try:
            loaded_accounts = load_accounts_from_file(tmp_path)
            self.assertEqual(len(loaded_accounts), 2)
            self.assertEqual(loaded_accounts[0].owner, "Alice")
            self.assertEqual(loaded_accounts[1].balance, 200.0)
        finally:
            os.remove(tmp_path)

    def test_load_accounts_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_accounts_from_file("nonexistent.json")

    def test_load_accounts_invalid_json(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            tmp.write("invalid json")
            tmp_path = tmp.name

        try:
            with self.assertRaises(ValueError):
                load_accounts_from_file(tmp_path)
        finally:
            os.remove(tmp_path)

    def test_save_and_load_transaction_history(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            save_transaction_history(self.history, tmp.name)
            tmp_path = tmp.name

        try:
            loaded_history = load_transaction_history(tmp_path)
            self.assertEqual(len(loaded_history), 2)
            self.assertEqual(loaded_history[0]["type"], "deposit")
        finally:
            os.remove(tmp_path)

    def test_load_transaction_history_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_transaction_history("no_history.json")

    # 5 testów

    def test_load_transaction_history_invalid_data(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            tmp.write("not valid json at all")
            tmp_path = tmp.name

        try:
            with self.assertRaises(ValueError):
                load_transaction_history(tmp_path)
        finally:
            os.remove(tmp_path)
