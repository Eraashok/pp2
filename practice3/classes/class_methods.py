class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= self.balance:
            self.balance -= amount

    def show_balance(self) -> None:
        print(self.balance)

if __name__ == "__main__":
    acc = BankAccount("Dana", 1000)
    acc.deposit(500)
    acc.withdraw(300)
    acc.show_balance()
