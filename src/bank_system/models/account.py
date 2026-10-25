import itertools
from decimal import Decimal
from enum import Enum

from bank_system.exceptions import InsufficientFundsError, InvalidAmountError


class Currency(Enum):
    RUB = "RUB"
    USD = "USD"
    BYN = "BYN"
    EUR = "EUR"


class Account:

    _number = itertools.count(1)

    def __init__(self, owner_id: int, currency: Currency):
        self.number = next(Account._number)
        self.owner_id = owner_id
        self.currency = currency
        self._balance = Decimal("0")

    @property
    def balance(self) -> Decimal:
        return self._balance

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise InvalidAmountError(f"Сумма должна быть положительной")

        self._balance += amount
        

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise InvalidAmountError(f"Сумма должна быть положительной")
        elif self.balance - amount < 0:
            raise InsufficientFundsError(f"У вас недостаточно денег на балансе. Ваш баланс: {self._balance}.")
        
        self._balance -= amount