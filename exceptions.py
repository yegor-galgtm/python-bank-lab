class BankError(Exception):
    pass

class InsufficientFundsError(BankError): #недостаточно средств
    pass

class AccountNotFoundError(BankError): #счет или клиент не найден
    pass

class CurrencyMismatchError(BankError): #разные валюты перевода
    pass

class DuplicateCurrencyError(BankError): #счет в той же валюте
    pass

class AccountNotEmptyError(BankError): #попытка закрыть счет с ненулевым балансом
    pass

class SameAccountError(BankError): #попытка перевести на тот же счет
    pass

class NonPositiveSumError(BankError):
    pass