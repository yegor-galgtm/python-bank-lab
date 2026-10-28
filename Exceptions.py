from decimal import Decimal


class InsufficientFundsError(Exception):
    def __init__(self, current_balance, requested_amount):
        cur = Decimal(str(current_balance))
        req = Decimal(str(requested_amount))
        deficit = req - cur
        message = (f"Недостаточно средств! На счете: {cur}, "
                   f"запрошено: {req} (не хватает: {deficit})")
        super().__init__(message)
        self.current_balance = cur
        self.requested_amount = req
        self.deficit = deficit


class AccountNotFoundError(Exception):
    def __init__(self, account, client, bank):
        find_client = client in bank.clients
        find_account = account in client.checks if account else False
        if not find_client:
            message = "Такого клиента нет в этом банке"
        elif not find_account:
            message = "У этого клиента нет такого счёта"
        else:
            message = "Клиент или счёт не найдены"
        super().__init__(message)


class CurrencyMismatchError(Exception):
    def __init__(self, currency: str, expected_currency: str):
        message = f"Ошибка валюты! Переданная валюта: {currency}, ожидалась: {expected_currency}"
        super().__init__(message)
        self.currency = currency
        self.expected_currency = expected_currency

class DuplicateCurrencyError(Exception):
    def __init__(self, client, account):
        message = f"Ошибка! У клиента уже есть открытый счёт в валюте {account.currency}"

        super().__init__(message)
        self.client = client
        self.account = account

class AccountNotEmptyError(Exception):
    def __init__(self, account, client):
        message = (f"Ошибка удаления! Нельзя закрыть счёт с ненулевым балансом. "
                   f"На счету осталось: {account.balance} {account.currency}")

        super().__init__(message)
        self.account = account
        self.client = client

