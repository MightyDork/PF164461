class Account:
    def __init__(self, account_id: str, owner: str, balance: float = 0.0):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.account_id = account_id
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self) -> float:
        return self.balance



    def transfer_to(self, target: 'Account', amount: float) -> None:
        # transfer money to another account
        if not isinstance(target, Account):
            raise TypeError("Target must be an Account.")
        self.withdraw(amount)
        target.deposit(amount)

    def is_overdrawn(self) -> bool:
        # TODO check if balance is below zero
        return self.balance < 0