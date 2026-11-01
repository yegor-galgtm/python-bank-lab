import datetime

CURRENCIES = ["RUB", "USD", "EUR"]

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


class AccountNotEmptyError(BankError):
    pass


class ClientAlreadyExistsError(BankError):
    pass

class Account:
    _next_number = 100001

    def __init__(self, owner_id, currency):
        self._number = str(Account._next_number)
        Account._next_number += 1
        self._owner_id = owner_id
        self._currency = currency
        self._balance = 0.0

    def get_number(self):
        return self._number

    def get_owner_id(self):
        return self._owner_id

    def get_currency(self):
        return self._currency

    def get_balance(self):
        return self._balance

    def deposit(self, amount):
        amount = round(amount, 2)
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля.")
        self._balance = round(self._balance + amount, 2)

    def withdraw(self, amount):
        amount = round(amount, 2)
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля.")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Недостаточно средств на счете {self._number}: "
                f"на счете {self._balance} {self._currency}, а нужно {amount}."
            )
        self._balance = round(self._balance - amount, 2)


class Client:
    def __init__(self, client_id, full_name):
        self._id = client_id
        self._full_name = full_name
        self._accounts = []

    def get_id(self):
        return self._id

    def get_full_name(self):
        return self._full_name

    def get_accounts(self):
        return self._accounts

    def add_account(self, account):
        self._accounts.append(account)

    def remove_account(self, account):
        self._accounts.remove(account)

    def find_account_by_currency(self, currency):
        for account in self._accounts:
            if account.get_currency() == currency:
                return account
        return None


class Bank:
    def __init__(self, name):
        self._name = name
        self._clients = {}
        self._accounts = {}

    def get_name(self):
        return self._name

    def register_client(self, client_id, full_name):
        if client_id in self._clients:
            raise ClientAlreadyExistsError(f"Клиент с ID {client_id} уже существует.")
        full_name = full_name.strip()
        if full_name == "":
            raise ValueError("ФИО не может быть пустым.")
        client = Client(client_id, full_name)
        self._clients[client_id] = client
        return client

    def find_client(self, client_id):
        return self._clients.get(client_id)

    def get_client(self, client_id):
        client = self.find_client(client_id)
        if client is None:
            raise AccountNotFoundError(f"Клиент с ID {client_id} не найден.")
        return client

    def get_account(self, account_number):
        account_number = str(account_number).strip()
        if account_number not in self._accounts:
            raise AccountNotFoundError(f"Счет {account_number} не найден.")
        return self._accounts[account_number]

    def open_account(self, client_id, currency):
        client = self.get_client(client_id)
        currency = currency.strip().upper()
        if currency not in CURRENCIES:
            raise ValueError("Неизвестная валюта. Доступно: " + ", ".join(CURRENCIES))
        if client.find_account_by_currency(currency) is not None:
            raise DuplicateCurrencyError(f"У клиента уже есть счет в валюте {currency}.")
        account = Account(client_id, currency)
        client.add_account(account)
        self._accounts[account.get_number()] = account
        return account

    def close_account(self, account_number):
        account = self.get_account(account_number)
        if account.get_balance() != 0:
            raise AccountNotEmptyError(
                f"Нельзя закрыть счет {account.get_number()}: баланс {account.get_balance()} "
                f"{account.get_currency()}, он должен быть равен нулю."
            )
        client = self.get_client(account.get_owner_id())
        client.remove_account(account)
        del self._accounts[account.get_number()]

    def deposit(self, account_number, amount):
        account = self.get_account(account_number)
        account.deposit(amount)

    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)
        account.withdraw(amount)

    def transfer(self, from_number, to_number, amount):
        from_account = self.get_account(from_number)
        to_account = self.get_account(to_number)

        if from_account is to_account:
            raise ValueError("Нельзя переводить деньги на тот же самый счет.")
        if from_account.get_currency() != to_account.get_currency():
            raise CurrencyMismatchError(
                f"Валюты счетов не совпадают: {from_account.get_currency()} и "
                f"{to_account.get_currency()}."
            )

        from_account.withdraw(amount)
        to_account.deposit(amount)


if __name__ == "__main__":
    bank = Bank("Лабораторный банк")
    ivan = bank.register_client(1, "Иванов Иван")
    anna = bank.register_client(2, "Петрова Анна")

    acc1 = bank.open_account(1, "RUB")
    acc2 = bank.open_account(2, "RUB")
    bank.deposit(acc1.get_number(), 500)

    try:
        bank.open_account(1, "RUB")
    except DuplicateCurrencyError as e:
        print("Ошибка:", e)

    try:
        bank.withdraw(acc1.get_number(), 5000)
    except InsufficientFundsError as e:
        print("Ошибка:", e)

    bank.transfer(acc1.get_number(), acc2.get_number(), 100)
    print(acc1.get_balance(), acc2.get_balance())

    try:
        bank.close_account(acc1.get_number())
    except AccountNotEmptyError as e:
        print("Ошибка:", e)