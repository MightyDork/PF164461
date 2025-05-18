from src.accounts import Account

class TransactionManager:
    def __init__(self):
        self.transaction_history = []

    def transfer(self, sender, receiver, amount):
        if not isinstance(receiver, Account) or not isinstance(sender, Account):
            raise TypeError("Both sender and receiver must be Account instances.")
        if sender.is_locked() or receiver.is_locked():
            raise ValueError("Either sender or receiver account is locked.")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if sender.get_available_balance() < amount:
            raise ValueError("Insufficient available funds")

        sender.withdraw(amount)
        receiver.deposit(amount)

        self.transaction_history.append({
            "type": "transfer",
            "from": sender.account_id,
            "to": receiver.account_id,
            "amount": amount
        })

    def reserve_funds(self, account: Account, amount: float) -> None:
        # reserve part of the balance for future transfer
        if amount <= 0:
            raise ValueError("Reservation amount must be positive.")
        if account.is_locked():
            raise PermissionError("Account is locked.")
        if account.get_available_balance() < amount:
            raise ValueError("Insufficient available funds.")
        account.locked_amount += amount

    def complete_reserved_transfer(self, source: Account, target: Account, amount: float) -> None:
        # finalize reserved transfer
        if not isinstance(target, Account):
            raise TypeError("Target must be an Account.")
        if source.is_locked() or target.is_locked():
            raise PermissionError("locked account cannot transfer or receive.")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive.")
        if source.locked_amount != amount:
            raise ValueError("Transfer amount must match reserved funds exactly.")
        source.locked_amount -= amount
        source.balance -= amount
        target.deposit(amount)
        self.transaction_history.append({
            "type": "reserved_transfer",
            "from": source.account_id,
            "to": target.account_id,
            "amount": amount
        })

    def cancel_reservation(self, account: Account, amount: float) -> None:
        # cancel locked reservation and restore available funds
        if amount <= 0:
            raise ValueError("Cancel amount must be positive.")
        if amount > account.locked_amount:
            raise ValueError("Cancel amount exceeds reserved funds.")
        account.locked_amount -= amount

    def apply_interest(self, account, rate):
        if rate < 0:
            raise ValueError("Interest rate must be non-negative")

        interest = account.get_balance() * rate
        if interest <= 0:
            return

        account.deposit(interest)
        self.transaction_history.append({
            "type": "interest",
            "account": account.account_id,
            "rate": rate,
            "amount": interest
        })

    def get_history(self):
        return list(self.transaction_history)

    def clear_history(self):
        self.transaction_history.clear()
