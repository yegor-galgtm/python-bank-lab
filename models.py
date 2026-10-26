from exceptions import (
    DuplicateCurrencyError,
    InsufficientFundsError,
    InvalidAmountError,
)
class Account:
    _next_number: int = 100001
    def __init__(self, owner_id: str, currency: str, balance: float = 0.0):
        self.account_number: str = str(Account._next_number)
        Account._next_number += 1
        self.owner_id: str = str(owner_id).strip()
        self.currency: str = currency.strip().upper()
        self.balance: float = round(float(balance), 2)
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("Сумма пополнения должна быть больше нуля.")
        self.balance = round(self.balance + amount, 2)
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("Сумма снятия должна быть больше нуля.")
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Недостаточно средств. Доступный баланс: {self.balance:.2f} {self.currency}."
            )
        self.balance = round(self.balance - amount, 2)
    def __str__(self) -> str:
        return f"Счет №{self.account_number} | Валюта: {self.currency} | Баланс: {self.balance:.2f}"
class Client:
    def __init__(self, client_id: str, full_name: str):
        self.client_id: str = str(client_id).strip()
        self.full_name: str = full_name.strip()
        self.accounts: list[Account] = []
    def has_currency(self, currency: str) -> bool:
        currency = currency.strip().upper()
        return any(acc.currency == currency for acc in self.accounts)
    def add_account(self, account: Account) -> None:
        if self.has_currency(account.currency):
            raise DuplicateCurrencyError(
                f"У клиента уже открыт счет в валюте {account.currency}."
            )
        self.accounts.append(account)
    def remove_account(self, account: Account) -> None:
        if account in self.accounts:
            self.accounts.remove(account)
    def __str__(self) -> str:
        return f"Клиент [{self.client_id}]: {self.full_name} (счетов: {len(self.accounts)})"