from datetime import datetime

class BankException(Exception):
    "Базовая ошибка банковской системы."
    pass

class InsufficientFundsError(BankException):
    "Недостаточно средств для снятия или перевода."
    pass

class AccountNotFoundError(BankException):
    "Счёт, или клиент не найден."
    pass

class CurrencyMismatchError(BankException):
    "Попытка перевода между счетами разных валют."
    pass

class DuplicateCurrencyError(BankException):
    "Попытка открыть второй счёт в той же валюте."
    pass

class AccountNotEmptyError(BankException):
    "Попытка закрыть счёт с ненулевым балансом."
    pass

class InvalidAmountError(BankException):
    "Некорректная сумма операции."
    pass

class InvalidCurrencyError(BankException):
    "Недопустимая валюта."
    pass
