class BankError(Exception):
    pass
class InsufficientFundsError(BankError):
    def __init__(self, message: str = "Недостаточно средств на счете."):
        super().__init__(message)
class AccountNotFoundError(BankError):
    def __init__(self, message: str = "Указанный счет или клиент не найден."):
        super().__init__(message)
class CurrencyMismatchError(BankError):
    def __init__(self, message: str = "Перевод возможен только между счетами в одной валюте."):
        super().__init__(message)
class DuplicateCurrencyError(BankError):
    def __init__(self, message: str = "У клиента уже открыт счет в данной валюте."):
        super().__init__(message)
class AccountNotEmptyError(BankError):
    def __init__(self, message: str = "Невозможно закрыть счет с ненулевым балансом."):
        super().__init__(message)
class InvalidAmountError(BankError):
    def __init__(self, message: str = "Сумма операции должна быть строго больше нуля."):
        super().__init__(message)
class SelfTransferError(BankError):
    def __init__(self, message: str = "Перевод самому себе запрещен."):
        super().__init__(message)