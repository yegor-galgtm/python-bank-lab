class BankError(Exception):
    pass

class InsufficientFundsError(BankError):
    pass

class AccountNotFoundError(BankError):
    pass

class CurrencyMismatchError(BankError):
    pass

class DuplicateCurrencyError(BankError):
    pass

class AccountNotEmptyErrorr(BankError):
    pass