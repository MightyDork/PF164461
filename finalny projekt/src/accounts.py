from datetime import date


class Account:
    def __init__(self, account_id: str, owner: str, balance: float = 0.0,
                 creation_date: date = None, daily_limit: int = 5):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.unlock()
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
        self.locked = False
        self.daily_withdraw_limit = 1000.0
        self.withdrawn_today = 0.0
        self.last_withdraw_date = date.today()
        self.creation_date = creation_date if creation_date else date.today()
        self.daily_limit = daily_limit
        self.operation_log = []
        self.locked_amount = 0.0

    def deposit(self, amount: float) -> None:
        self._check_daily_limit()
        if self.locked:
            raise ValueError("Account is locked.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self._record_operation()

    def withdraw(self, amount: float) -> None:
        self._check_daily_limit()
        if self.locked:
            raise ValueError("Account is locked.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.get_available_balance():
            raise ValueError("Insufficient available  funds.")

        today = date.today()
        if today != self.last_withdraw_date:
            self.withdrawn_today = 0.0
            self.last_withdraw_date = today

        if self.withdrawn_today + amount > self.daily_withdraw_limit:
            raise ValueError("Daily withdrawal limit exceeded.")

        self.balance -= amount
        self.withdrawn_today += amount
        self._record_operation()

    def get_balance(self) -> float:
        return self.balance

    def is_overdrawn(self) -> bool:
        # check if balance is below zero
        return self.balance < 0

    def lock(self) -> None:
        self.locked = True

    def unlock(self) -> None:
        self.locked = False

    def is_locked(self) -> bool:
        return self.locked

    def set_daily_limit(self, new_limit: float) -> None:
        if new_limit <= 0:
            raise ValueError("Limit must be positive.")
        self.daily_withdraw_limit = new_limit

    def reset_daily_withdrawn(self) -> None:
        # for testing
        self.withdrawn_today = 0.0
        self.last_withdraw_date = date.today()

    def rename_owner(self, new_name: str) -> None:
        # change the account owner name
        if not new_name:
            raise ValueError("Owner name cannot be empty.")
        self.owner = new_name

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "owner": self.owner,
            "balance": self.balance,
            "creation_date": self.creation_date.isoformat() if hasattr(self, 'creation_date') else None
        }

    def _record_operation(self):
        # add today's date to the operation log
        self.operation_log.append(date.today())

    def _check_daily_limit(self):
        # count how many operations today
        today = date.today()
        today_ops = [d for d in self.operation_log if d == today]
        if len(today_ops) >= self.daily_limit:
            raise ValueError("Daily operation limit exceeded.")

    def get_available_balance(self) -> float:
        # only available for withdrawal
        return self.balance - self.locked_amount

    def freeze_amount(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount to freeze must be positive.")
        if amount > self.get_available_balance():
            raise ValueError("Not enough available funds to freeze.")
        self.locked_amount += amount

    def unfreeze_amount(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount to unfreeze must be positive.")
        if amount > self.locked_amount:
            raise ValueError("Cannot unfreeze more than is locked.")
        self.locked_amount -= amount

