class BankException(Exception):
    """обозначение продуманной мною ошибки ниже для ловли именно наших ошибок"""

class InsufficientFundsError(BankException):
    """недостаточно средств для снятия/перевода."""

class AccountNotFoundError(BankException):
    """счет или клиент не найден"""

class CurrencyMismatchError(BankException):
    """попытка перевести средства между счетами разных валют."""

class DuplicateCurrencyError(BankException):
    """попытка открыть второй счет в той же валюте."""

class AccountNotEmptyError(BankException):
    """попытка закрыть счет с ненулевым балансом."""

class InvalidAmountError(BankException):
    """сумма должна быть положительной."""


class SelfTransferError(BankException):
    """нельзя переводить деньги на тот же счёт."""