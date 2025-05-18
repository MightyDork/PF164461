import unittest
from src.accounts import Account
from src.transactions import TransactionManager


class TestTransactionManager(unittest.TestCase):

    def setUp(self):
        # initialize test accounts and manager
        self.manager = TransactionManager()
        self.sender = Account("S001", "Sender", 500.0)
        self.receiver = Account("R001", "Receiver", 200.0)

    def test_successful_transfer(self):
        # test a successful transfer between accounts
        self.manager.transfer(self.sender, self.receiver, 100.0)
        self.assertEqual(self.sender.get_balance(), 400.0)
        self.assertEqual(self.receiver.get_balance(), 300.0)

    def test_transfer_insufficient_funds(self):
        # test transfer raises error if sender has insufficient funds
        with self.assertRaises(ValueError):
            self.manager.transfer(self.sender, self.receiver, 1000.0)

    def test_transfer_zero_amount(self):
        # test transfer with zero amount raises error
        with self.assertRaises(ValueError):
            self.manager.transfer(self.sender, self.receiver, 0.0)

    def test_transfer_negative_amount(self):
        # test transfer with negative amount raises error
        with self.assertRaises(ValueError):
            self.manager.transfer(self.sender, self.receiver, -50.0)

    def test_transfer_to_self(self):
        # Test transfer to self still changes balance correctly
        self.manager.transfer(self.sender, self.sender, 100.0)
        self.assertEqual(self.sender.get_balance(), 500.0)  # No change

    def test_interest_positive_rate(self):
        # Test that interest is added correctly
        acc = Account("A001", "Interest", 1000.0)
        self.manager.apply_interest(acc, 0.05)
        self.assertAlmostEqual(acc.get_balance(), 1050.0)

    def test_interest_zero_rate(self):
        # Test that zero interest rate leaves balance unchanged
        acc = Account("A002", "ZeroRate", 800.0)
        self.manager.apply_interest(acc, 0.0)
        self.assertEqual(acc.get_balance(), 800.0)

    def test_interest_negative_rate(self):
        # test that negative interest rate raises ValueError
        acc = Account("A003", "NegativeRate", 700.0)
        with self.assertRaises(ValueError):
            self.manager.apply_interest(acc, -0.01)

    def test_multiple_transfers(self):
        # test multiple transfers in sequence
        self.manager.transfer(self.sender, self.receiver, 50)
        self.manager.transfer(self.sender, self.receiver, 25)
        self.assertEqual(self.sender.get_balance(), 425.0)
        self.assertEqual(self.receiver.get_balance(), 275.0)

    def test_interest_applied_to_zero_balance(self):
        # test that interest on zero balance has no effect
        acc = Account("A004", "Zero", 0.0)
        self.manager.apply_interest(acc, 0.10)
        self.assertEqual(acc.get_balance(), 0.0)

    # 10 testów

    def test_transaction_history_records_transfer(self):
        # perform transfer
        self.manager.transfer(self.sender, self.receiver, 50)
        history = self.manager.get_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["type"], "transfer")
        self.assertEqual(history[0]["from"], "S001")
        self.assertEqual(history[0]["to"], "R001")
        self.assertEqual(history[0]["amount"], 50)

    def test_transaction_history_records_interest(self):
        acc = Account("X001", "X", 100)
        self.manager.apply_interest(acc, 0.1)
        history = self.manager.get_history()

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["type"], "interest")
        self.assertEqual(history[0]["account"], "X001")
        self.assertEqual(history[0]["rate"], 0.1)
        self.assertAlmostEqual(history[0]["amount"], 10)

    def test_transaction_history_multiple_operations(self):
        acc = Account("X002", "X", 100)
        self.manager.apply_interest(acc, 0.05)
        self.manager.transfer(self.sender, self.receiver, 75)

        history = self.manager.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["type"], "interest")
        self.assertEqual(history[1]["type"], "transfer")

    def test_transaction_history_isolated_copy(self):
        # make sure history is returned as a copy
        self.manager.transfer(self.sender, self.receiver, 20)
        history = self.manager.get_history()
        history.append("fake")

        self.assertEqual(len(self.manager.get_history()), 1)

    def test_clear_history(self):
        # add one transaction and clear
        self.manager.transfer(self.sender, self.receiver, 10)
        self.manager.clear_history()
        self.assertEqual(len(self.manager.get_history()), 0)

    # 15 testów

    def test_transfer_success(self):
        acc1 = Account("008", "Hubert", 100)
        acc2 = Account("009", "Iga", 50)
        self.manager.transfer(acc1, acc2, 30)
        self.assertEqual(acc1.get_balance(), 70)
        self.assertEqual(acc2.get_balance(), 80)

    def test_transfer_invalid_target(self):
        acc = Account("010", "Jan", 100)
        with self.assertRaises(TypeError):
            self.manager.transfer(acc, "not an account", 50)

    def test_reserve_and_complete_transfer(self):
        acc1 = Account("300", "A", 100)
        acc2 = Account("301", "B", 50)
        self.manager.reserve_funds(acc1, 60)
        self.assertEqual(acc1.locked_amount, 60)
        self.manager.complete_reserved_transfer(acc1, acc2, 60)
        self.assertEqual(acc1.get_balance(), 40)
        self.assertEqual(acc1.locked_amount, 0)
        self.assertEqual(acc2.get_balance(), 110)

    def test_cancel_reservation(self):
        acc = Account("302", "C", 100)
        self.manager.reserve_funds(acc, 70)
        self.manager.cancel_reservation(acc, 70)
        self.assertEqual(acc.locked_amount, 0)
        self.assertEqual(acc.get_balance(), 100)

    def test_reserved_transfer_without_reservation(self):
        acc1 = Account("303", "X", 100)
        acc2 = Account("304", "Y", 50)
        with self.assertRaises(ValueError):
            self.manager.complete_reserved_transfer(acc1, acc2, 30)

    def test_reserve_more_than_available(self):
        acc = Account("305", "Z", 100)
        with self.assertRaises(ValueError):
            self.manager.reserve_funds(acc, 150)

    def test_cancel_more_than_reserved(self):
        acc = Account("306", "M", 100)
        self.manager.reserve_funds(acc, 40)
        with self.assertRaises(ValueError):
            self.manager.cancel_reservation(acc, 50)

    def test_double_reservation(self):
        acc = Account("307", "N", 200)
        self.manager.reserve_funds(acc, 50)
        self.manager.reserve_funds(acc, 50)
        self.assertEqual(acc.locked_amount, 100)
        self.assertEqual(acc.get_available_balance(), 100)

    def test_reserved_transfer_wrong_types(self):
        acc1 = Account("308", "P", 100)
        acc2 = "not an account"
        self.manager.reserve_funds(acc1, 30)
        with self.assertRaises(TypeError):
            self.manager.complete_reserved_transfer(acc1, acc2, 30)

    def test_cancel_reservation_wrong_type(self):
        with self.assertRaises(AttributeError):
            self.manager.cancel_reservation("not an account", 50)

    def test_reserve_funds_on_locked_account(self):
        acc = Account("309", "Q", 100)
        acc.lock()
        with self.assertRaises(PermissionError):
            self.manager.reserve_funds(acc, 50)

    def test_complete_transfer_on_locked_account(self):
        acc1 = Account("310", "R", 100)
        acc2 = Account("311", "S", 0)
        self.manager.reserve_funds(acc1, 60)
        acc1.lock()
        with self.assertRaises(PermissionError):
            self.manager.complete_reserved_transfer(acc1, acc2, 60)

    def test_complete_transfer_to_locked_account(self):
        acc1 = Account("312", "T", 100)
        acc2 = Account("313", "U", 0)
        acc2.lock()
        self.manager.reserve_funds(acc1, 30)
        with self.assertRaises(PermissionError):
            self.manager.complete_reserved_transfer(acc1, acc2, 30)

    def test_reserve_negative_amount(self):
        acc = Account("314", "V", 100)
        with self.assertRaises(ValueError):
            self.manager.reserve_funds(acc, -10)

    def test_complete_transfer_amount_mismatch(self):
        acc1 = Account("315", "W", 100)
        acc2 = Account("316", "X", 0)
        self.manager.reserve_funds(acc1, 40)
        with self.assertRaises(ValueError):
            self.manager.complete_reserved_transfer(acc1, acc2, 30)

    def test_reserve_zero_amount(self):
        acc = Account("317", "Y", 100)
        with self.assertRaises(ValueError):
            self.manager.reserve_funds(acc, 0)

    def test_cancel_zero_amount(self):
        acc = Account("318", "Z", 100)
        self.manager.reserve_funds(acc, 40)
        with self.assertRaises(ValueError):
            self.manager.cancel_reservation(acc, 0)

    def test_transfer_then_try_to_cancel_same_amount(self):
        acc1 = Account("319", "AA", 100)
        acc2 = Account("320", "BB", 50)
        self.manager.reserve_funds(acc1, 30)
        self.manager.complete_reserved_transfer(acc1, acc2, 30)
        with self.assertRaises(ValueError):
            self.manager.cancel_reservation(acc1, 30)

    def test_reservation_does_not_affect_total_balance(self):
        acc = Account("321", "CC", 200)
        self.manager.reserve_funds(acc, 150)
        self.assertEqual(acc.get_balance(), 200)
        self.assertEqual(acc.get_available_balance(), 50)

    def test_cancel_all_locked_then_reserve_again(self):
        acc = Account("322", "DD", 300)
        self.manager.reserve_funds(acc, 100)
        self.manager.cancel_reservation(acc, 100)
        self.manager.reserve_funds(acc, 200)
        self.assertEqual(acc.locked_amount, 200)
        self.assertEqual(acc.get_available_balance(), 100)

    def test_reserved_transfer_logged(self):
        acc1 = Account("401", "Y", 100)
        acc2 = Account("402", "Z", 0)

        self.manager.reserve_funds(acc1, 40)
        self.manager.complete_reserved_transfer(acc1, acc2, 40)

        history = self.manager.get_history()
        self.assertTrue(any(
            entry["type"] == "reserved_transfer" and
            entry["from"] == "401" and
            entry["to"] == "402" and
            entry["amount"] == 40
            for entry in history
        ))

    def test_transfer_locked_account(self):
        acc1 = Account("501", "Sender", 100)
        acc2 = Account("502", "Receiver", 50)

        acc1.lock()

        with self.assertRaises(ValueError):
            self.manager.transfer(acc1, acc2, 30)

    def test_complete_reserved_transfer_negative_amount(self):
        acc1 = Account("601", "From", 100)
        acc2 = Account("602", "To", 50)

        self.manager.reserve_funds(acc1, 30)

        with self.assertRaises(ValueError):
            self.manager.complete_reserved_transfer(acc1, acc2, -10)
