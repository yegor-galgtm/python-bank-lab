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

    def save_statement(self, client_id):
        client = self.get_client(client_id)
        file_name = f"statement_{client_id}.txt"
        now = datetime.datetime.now()
        totals = {}

        with open(file_name, "w", encoding="utf-8") as fh:
            fh.write(f"Банк: {self._name}\n")
            fh.write(f"Клиент: {client.get_full_name()} (ID {client_id})\n")
            fh.write("Дата и время: " + now.strftime("%d.%m.%Y %H:%M:%S") + "\n")
            fh.write("\nСчета:\n")

            if len(client.get_accounts()) == 0:
                fh.write("  Счетов нет\n")

            for account in client.get_accounts():
                currency = account.get_currency()
                balance = account.get_balance()
                fh.write(f"  Счет {account.get_number()} | {currency} | {balance:.2f}\n")
                totals[currency] = round(totals.get(currency, 0.0) + balance, 2)

            fh.write("\nИтого по валютам:\n")
            for currency in totals:
                fh.write(f"  {currency}: {totals[currency]:.2f}\n")

        return file_name

def read_amount(prompt):
    while True:
        text = input(prompt).strip().replace(",", ".")
        try:
            amount = float(text)
        except ValueError:
            print("Нужно ввести число, например 100 или 25.5. Попробуйте еще раз.")
            continue
        if not (0 < amount < 1000000000):
            print("Сумма должна быть больше нуля и не слишком большой.")
            continue
        if round(amount, 2) <= 0:
            print("Минимальная сумма - 0.01.")
            continue
        return amount


def print_menu():
    print("\n=== Меню ===")
    print("1. Мои счета")
    print("2. Открыть счет")
    print("3. Закрыть счет")
    print("4. Пополнить счет")
    print("5. Снять деньги")
    print("6. Перевод")
    print("7. Сформировать выписку")
    print("0. Выйти из аккаунта")


def show_accounts(client):
    accounts = client.get_accounts()
    if len(accounts) == 0:
        print("У вас пока нет счетов.")
        return
    print("Ваши счета:")
    for account in accounts:
        print(f"  {account.get_number()} | {account.get_currency()} | {account.get_balance():.2f}")


def get_own_account(bank, client, account_number):
    account = bank.get_account(account_number)
    if account.get_owner_id() != client.get_id():
        raise AccountNotFoundError(f"У вас нет счета {account_number}.")
    return account


def login(bank):
    while True:
        text = input("\nВведите ID клиента (q - выход из программы): ").strip()
        if text.lower() == "q":
            return None
        try:
            client_id = int(text)
        except ValueError:
            print("ID должен быть целым числом.")
            continue
        if client_id < 0:
            print("ID не может быть отрицательным.")
            continue

        client = bank.find_client(client_id)
        if client is not None:
            print(f"Добро пожаловать, {client.get_full_name()}!")
            return client

        answer = input("Клиент не найден. Создать нового? (y/n): ").strip().lower()
        if answer == "y":
            name = input("Введите ФИО: ")
            try:
                client = bank.register_client(client_id, name)
            except BankError as e:
                print("Ошибка:", e)
                continue
            except ValueError as e:
                print("Ошибка:", e)
                continue
            print(f"Клиент {client.get_full_name()} зарегистрирован.")
            return client


def client_session(bank, client):
    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()

        try:
            if choice == "1":
                show_accounts(client)

            elif choice == "2":
                currency = input("Валюта (" + "/".join(CURRENCIES) + "): ")
                account = bank.open_account(client.get_id(), currency)
                print(f"Счет открыт. Номер: {account.get_number()}, валюта: {account.get_currency()}")

            elif choice == "3":
                number = input("Номер счета для закрытия: ")
                account = get_own_account(bank, client, number)
                bank.close_account(account.get_number())
                print("Счет закрыт.")

            elif choice == "4":
                number = input("Номер счета: ")
                account = get_own_account(bank, client, number)
                amount = read_amount("Сумма пополнения: ")
                bank.deposit(account.get_number(), amount)
                print(f"Готово. Баланс: {account.get_balance():.2f} {account.get_currency()}")

            elif choice == "5":
                number = input("Номер счета: ")
                account = get_own_account(bank, client, number)
                amount = read_amount("Сумма снятия: ")
                bank.withdraw(account.get_number(), amount)
                print(f"Готово. Баланс: {account.get_balance():.2f} {account.get_currency()}")

            elif choice == "6":
                from_number = input("Номер вашего счета (откуда): ")
                from_account = get_own_account(bank, client, from_number)
                to_number = input("Номер счета получателя: ")
                amount = read_amount("Сумма перевода: ")
                bank.transfer(from_account.get_number(), to_number, amount)
                print(f"Перевод выполнен. Баланс: {from_account.get_balance():.2f} {from_account.get_currency()}")

            elif choice == "7":
                file_name = bank.save_statement(client.get_id())
                print("Выписка сохранена в файл", file_name)

            elif choice == "0":
                print("Выход из аккаунта.")
                break

            else:
                print("Нет такого пункта меню, введите число от 0 до 7.")

        except BankError as e:
            print("Ошибка:", e)
        except ValueError as e:
            print("Ошибка:", e)
        except OSError as e:
            print("Не удалось записать файл:", e)


def main():
    bank = Bank("Лабораторный банк")
    print("=== Банковская система ===")

    while True:
        client = login(bank)
        if client is None:
            break
        client_session(bank, client)

    print("До свидания!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма завершена.")