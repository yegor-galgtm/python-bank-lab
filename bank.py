class BankException(Exception):
    "Базовая ошибка банковской системы."
    pass


class InsufficientFundsError(BankException):
    "Недостаточно средств для снятия или перевода."
    pass


class AccountNotFoundError(BankException):
    "Счёт или клиент не найден."
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


class Account():
    _next_id = 1
    def __init__(self, valute, id_owner):
        self.id_account = Account._next_id
        Account._next_id += 1
        self.id_owner = id_owner

        if valute not in ("EUR", "USD", "RUB"):
            raise ValueError(f"Недопустимая валюта: {valute}")
        self.valute = valute

        self.balance = 0

    def plus(self, sums):
        if sums <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance += sums

    def minus(self, sums):
        if sums <= 0:
            raise ValueError("Сумма снятия должна быть положительной")

        if sums > self.balance:
            raise InsufficientFundsError(
                f"Запрошено {sums}, доступно {self.balance}"
            )

        self.balance -= sums


class Client():
    _next_id = 1

    def __init__(self, full_name):
        self.id_client = Client._next_id
        Client._next_id += 1

        self.full_name = full_name
        self.accounts = []

class Bank():
    def __init__(self):
        self.clients = {}
        self.accounts = {}
    def create_client(self):
        print("--Создание нового клиента банка--")
        full_name = input("Введите ФИО нового клиента банка: ")
        if not full_name.strip():
            raise ValueError("ФИО не может быть пустым")

        client = Client(full_name)
        self.clients[client.id_client] = client

        print(f"Клиент успешно создан! ID: {client.id_client}")
        return client

    def create_accounts(self):
        print("--Создание счета для клиента--")
        client_id = int(input("Введите ID клиента: "))
        if client_id not in self.clients:
            raise AccountNotFoundError(f"Клиент с ID {client_id} не найден")
        client = self.clients[client_id]

        valute = input("Введите валюту счета (RUB/USD/EUR): ").strip().upper()

        for acc in client.accounts:
            if acc.valute == valute:
                raise DuplicateCurrencyError(
                    f"У клиента уже есть счёт в валюте {valute}"
                )

        account = Account(valute, client.id_client)
        client.accounts.append(account)
        self.accounts[account.id_account] = account
        print(
            f"Счёт {account.id_account} ({account.valute}) "
            f"открыт для клиента {client.full_name}"
        )
        return account