from datetime import datetime

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

class InvalidAmountError(BankException):
    "Некорректная сумма операции."
    pass

class InvalidCurrencyError(BankException):
    "Недопустимая валюта."
    pass


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")

def read_positive_money(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")
            continue
        if value <= 0:
            print("Ошибка: сумма должна быть положительной.")
            continue
        return value

def read_currency(prompt):
    allowed = ("RUB", "USD", "EUR")
    while True:
        value = input(prompt).strip().upper()
        if value in allowed:
            return value
        print(f"Ошибка: допустимые валюты: {', '.join(allowed)}.")

def read_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: строка не может быть пустой.")

class Account():
    _next_id = 1

    def __init__(self, valute, id_owner):
        self.id_account = Account._next_id
        Account._next_id += 1
        self.id_owner = id_owner

        if valute not in ("EUR", "USD", "RUB"):
            raise InvalidCurrencyError(f"Недопустимая валюта: {valute}")
        self.valute = valute

        self.balance = 0

    def plus(self, sums):
        if sums <= 0:
            raise InvalidAmountError("Сумма пополнения должна быть положительной")
        self.balance += sums

    def minus(self, sums):
        if sums <= 0:
            raise InvalidAmountError("Сумма снятия должна быть положительной")

        if sums > self.balance:
            raise InsufficientFundsError(
                f"Запрошено {sums}, доступно {self.balance}"
            )
        self.balance -= sums

    def close(self):
        if self.balance != 0:
            raise AccountNotEmptyError(
                f"Нельзя закрыть счёт {self.id_account}: "
                f"на нём {self.balance} {self.valute}"
            )

class Client():
    _next_id = 1

    def __init__(self, full_name):
        self.id_client = Client._next_id
        Client._next_id += 1

        self.full_name = full_name
        self.accounts = []

    def add_account(self, account):
        for acc in self.accounts:
            if acc.valute == account.valute:
                raise DuplicateCurrencyError(
                    f"У клиента уже есть счёт в валюте {account.valute}"
                )
        self.accounts.append(account)

    def get_account(self, account_id):
        for acc in self.accounts:
            if acc.id_account == account_id:
                return acc
        raise AccountNotFoundError(
            f"Счёт {account_id} не найден у клиента {self.id_client}"
        )

    def remove_account(self, account_id):
        account = self.get_account(account_id)
        self.accounts.remove(account)
        return account


class Bank():
    def __init__(self):
        self.clients = {}
        self.accounts = {}

    def get_client(self, client_id):
        if client_id not in self.clients:
            raise AccountNotFoundError(f"Клиент с ID {client_id} не найден")
        return self.clients[client_id]

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Счёт {account_id} не найден")
        return self.accounts[account_id]

    def create_client(self):
        print("--Создание нового клиента банка--")
        full_name = read_nonempty("Введите ФИО нового клиента банка: ")

        client = Client(full_name)
        self.clients[client.id_client] = client

        print(f"Клиент успешно создан! ID: {client.id_client}")
        return client

    def create_accounts(self, client_id=None):
        print("--Создание счёта для клиента--")
        if client_id is None:
            client_id = read_int("Введите ID клиента: ")
        client = self.get_client(client_id)

        valute = read_currency("Введите валюту счёта (RUB/USD/EUR): ")

        account = Account(valute, client.id_client)
        client.add_account(account)

        self.accounts[account.id_account] = account
        print(
            f"Счёт {account.id_account} ({account.valute}) "
            f"открыт для клиента {client.full_name}"
        )
        return account

    def delete_accounts(self, client_id=None):
        id_account = read_int("Введите номер счёта для закрытия: ")
        account = self.get_account(id_account)

        if client_id is not None and account.id_owner != client_id:
            raise BankException("Это не ваш счёт")

        account.close()

        del self.accounts[id_account]
        self.get_client(account.id_owner).remove_account(id_account)

        print(f"Счёт {id_account} успешно закрыт!")

    def trade(self, client_id=None):
        start_id = read_int("Введите id счета с которого переводим деньги: ")
        start_acc = self.get_account(start_id)

        if client_id is not None and start_acc.id_owner != client_id:
            raise BankException("Это не ваш счёт")

        end_id = read_int("Введите id счета получателя: ")
        end_acc = self.get_account(end_id)

        if start_id == end_id:
            raise BankException("Попытка перевести деньги самому себе")

        if start_acc.valute != end_acc.valute:
            raise CurrencyMismatchError(
                f"Нельзя перевести {start_acc.valute} в {end_acc.valute}"
            )

        money = read_positive_money("Сумма: ")
        start_acc.minus(money)
        end_acc.plus(money)

    def statement(self, client_id=None):
        if client_id is None:
            client_id = read_int("Введите id клиента для получения выписки: ")
        client = self.get_client(client_id)

        result = {}
        for acc in client.accounts:
            result[acc.valute] = result.get(acc.valute, 0) + acc.balance

        time_gener = datetime.now()
        path = f"statement_{client_id}.txt"

        with open(path, "w", encoding="utf-8") as file:
            file.write(f"Выписка по клиенту: {client.full_name} (ID {client_id})\n")
            file.write(f"Сгенерировано: {time_gener:%Y-%m-%d %H:%M:%S}\n")
            file.write("\nСчета:\n")

            if not client.accounts:
                file.write("  Счетов нет\n")
            else:
                for acc in client.accounts:
                    file.write(f"  Счёт {acc.id_account}: {acc.valute} — {acc.balance}\n")

            file.write("\nИтоги по валютам:\n")
            if not result:
                file.write("  Нет данных\n")
            else:
                for valute, total in result.items():
                    file.write(f"  {valute}: {total}\n")

        print(f"Выписка была успешно сохранена в {path}")
        return path

bank = Bank()
client = None
running = True

while running and client == None:
    client_id = read_int("Введите ID клиента (0 — выход): ")
    if client_id == 0:
        print("До свидания!")
        running = False
        continue

    try:
        client = bank.get_client(client_id)
        print(f"Добро пожаловать, {client.full_name}!")
    except AccountNotFoundError:
        print(f"Клиент с ID {client_id} не найден.")
        answer = input("Создать нового клиента? (да/нет): ").strip().lower()
        if answer in ("да", "yes", "y", "д"):
            client = bank.create_client()
            print(f"Вход выполнен под ID {client.id_client}")

if running and client != None:
    while True:
        print("----Меню Bank----")
        print("1. Мои счета")
        print("2. Пополнить счёт")
        print("3. Снять средства")
        print("4. Перевод")
        print("5. Выписка")
        print("6. Создать счет")
        print("7. Удалить счет")
        print("0. Выход")

        choice = read_int("Выбор: ")

        try:
            if choice == 1:
                if not client.accounts:
                    print("У вас нет счетов.")
                else:
                    print("Ваши счета:")
                    for acc in client.accounts:
                        print(f"  Счёт {acc.id_account}: {acc.valute} — {acc.balance}")

            elif choice == 2:
                acc_id = read_int("ID счёта: ")
                acc = client.get_account(acc_id)
                amount = read_positive_money("Сумма пополнения: ")
                acc.plus(amount)
                print(f"Счёт {acc_id} пополнен на {amount} {acc.valute}")

            elif choice == 3:
                acc_id = read_int("ID счёта: ")
                acc = client.get_account(acc_id)
                amount = read_positive_money("Сумма снятия: ")
                acc.minus(amount)
                print(f"Со счёта {acc_id} снято {amount} {acc.valute}")

            elif choice == 4:
                bank.trade(client.id_client)

            elif choice == 5:
                bank.statement(client.id_client)

            elif choice == 6:
                bank.create_accounts(client.id_client)

            elif choice == 7:
                bank.delete_accounts(client.id_client)

            elif choice == 0:
                print("До свидания!")
                break

            else:
                print("Нет такого пункта меню.")

        except BankException as e:
            print(f"Ошибка: {e}")