import unittest
from src.accounts import Account
from datetime import date

class TestAccount(unittest.TestCase):
    def test_deposit(self):
        acc = Account("001", "Anna", 100)
        acc.deposit(50)
        self.assertEqual(acc.get_balance(), 150)

    def test_withdraw_success(self):
        acc = Account("002", "Bartek", 200)
        acc.withdraw(100)
        self.assertEqual(acc.get_balance(), 100)

    def test_withdraw_insufficient_funds(self):
        acc = Account("003", "Czarek", 50)
        with self.assertRaises(ValueError):
            acc.withdraw(100)

    def test_negative_initial_balance(self):
        with self.assertRaises(ValueError):
            Account("004", "Damian", -10)

    def test_invalid_deposit(self):
        acc = Account("005", "Emilia", 0)
        with self.assertRaises(ValueError):
            acc.deposit(0)

    def test_owner_change_success(self):
        acc = Account("006", "Filip", 100)
        acc.rename_owner("Filip Nowak")
        self.assertEqual(acc.owner, "Filip Nowak")

    def test_owner_change_empty_name(self):
        acc = Account("007", "Gosia", 100)
        with self.assertRaises(ValueError):
            acc.rename_owner("")

    def test_zero_balance_not_overdrawn(self):
        acc = Account("013", "Marek", 0)
        self.assertFalse(acc.is_overdrawn())

    def test_is_overdrawn_false(self):
        acc = Account("014", "Natalia", 100)
        self.assertFalse(acc.is_overdrawn())

    def test_lock_and_unlock_account(self):
        acc = Account("011", "Kasia", 100)
        self.assertFalse(acc.is_locked())
        acc.lock()
        self.assertTrue(acc.is_locked())
        acc.unlock()
        self.assertFalse(acc.is_locked())

    def test_locked_account_cannot_deposit_or_withdraw(self):
        acc = Account("012", "Lena", 100)
        acc.lock()
        with self.assertRaises(ValueError):
            acc.deposit(50)
        with self.assertRaises(ValueError):
            acc.withdraw(10)

    def test_set_valid_daily_limit(self):
        acc = Account("013", "Marek", 500)
        acc.set_daily_limit(200)
        acc.withdraw(150)
        self.assertEqual(acc.get_balance(), 350)

    def test_set_invalid_daily_limit(self):
        acc = Account("014", "Natalia", 300)
        with self.assertRaises(ValueError):
            acc.set_daily_limit(0)

    def test_daily_withdraw_limit_exceeded(self):
        acc = Account("015", "Olga", 1000)
        acc.set_daily_limit(300)
        acc.withdraw(200)
        with self.assertRaises(ValueError):
            acc.withdraw(150)

    def test_daily_limit_resets(self):
        acc = Account("016", "Patryk", 1000)
        acc.set_daily_limit(400)
        acc.withdraw(300)

        # simulate new day
        acc.last_withdraw_date = date(2000, 1, 1)
        acc.withdraw(200)  # should succeed
        self.assertEqual(acc.get_balance(), 500)

    def test_operation_limit_reached(self):
        acc = Account("101", "LimitTest", 500, daily_limit=3)
        acc.deposit(10)
        acc.deposit(10)
        acc.deposit(10)
        with self.assertRaises(ValueError):
            acc.deposit(10)

    def test_operation_limit_shared_between_deposit_and_withdraw(self):
        acc = Account("102", "MixedOps", 500, daily_limit=3)
        acc.deposit(50)
        acc.withdraw(20)
        acc.deposit(30)
        with self.assertRaises(ValueError):
            acc.withdraw(10)

    def test_operation_log_records_correct_dates(self):
        acc = Account("103", "Logger", 100, daily_limit=2)
        acc.deposit(10)
        acc.withdraw(5)
        self.assertEqual(len(acc.operation_log), 2)
        self.assertTrue(all(op == date.today() for op in acc.operation_log))

    def test_freeze_and_unfreeze_amount(self):
        acc = Account("201", "lockedMan", 200)
        acc.freeze_amount(50)
        self.assertEqual(acc.get_available_balance(), 150)
        acc.unfreeze_amount(30)
        self.assertEqual(acc.get_available_balance(), 180)
        self.assertEqual(acc.locked_amount, 20)

    def test_freeze_more_than_available(self):
        acc = Account("202", "Blocker", 100)
        with self.assertRaises(ValueError):
            acc.freeze_amount(150)

    # 20 testów

    def test_unfreeze_more_than_locked(self):
        acc = Account("203", "TooMuch", 100)
        acc.freeze_amount(20)
        with self.assertRaises(ValueError):
            acc.unfreeze_amount(50)

    def test_withdraw_respects_locked_funds(self):
        acc = Account("204", "Careful", 100)
        acc.freeze_amount(80)
        with self.assertRaises(ValueError):
            acc.withdraw(30)  # only 20 available

    def test_get_balance_includes_locked(self):
        acc = Account("205", "Check", 300)
        acc.freeze_amount(100)
        self.assertEqual(acc.get_balance(), 300)
        self.assertEqual(acc.get_available_balance(), 200)

    def test_withdraw_nonpositive_amount(self):
        acc = Account("700", "Tester", 100)

        with self.assertRaises(ValueError):
            acc.withdraw(0)

        with self.assertRaises(ValueError):
            acc.withdraw(-50)

    def test_freeze_nonpositive_amount(self):
        acc = Account("700", "Tester", 100)

        with self.assertRaises(ValueError):
            acc.freeze_amount(0)

        with self.assertRaises(ValueError):
            acc.freeze_amount(-50)

    def test_unfreeze_nonpositive_amount(self):
        acc = Account("700", "Tester", 100)
        acc.freeze_amount(50)  # Need some frozen amount first

        with self.assertRaises(ValueError):
            acc.unfreeze_amount(0)

        with self.assertRaises(ValueError):
            acc.unfreeze_amount(-30)