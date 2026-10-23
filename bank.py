class BankException(Exception):
    "Базова ошибка банка."
    pass

class InsufficientFundsError(BankException):
    " недостаточно средств для снятия/перевода."
    pass

class AccountNotFoundError(BankException):
    "счет или клиент не найден"
    pass

class CurrencyMismatchError(BankException):
    " попытка перевести средства между счетами разных валют."
    pass

class DuplicateCurrencyError(BankExecption):
    "попытка открыть второй счет в той же валюте."
    pass

class AccountNotEmptyError(BankException):
    "попытка закрыть счет с ненулевым балансом."
    pass

class Account():
    _next_id = 1
    id_owner = 0
    id_account = 0
    valute = ""
    balance = 0

    def __init__(self, valute, balance, id_owner):
        self.id_account = Account._next_id
        Account._next_id += 1

        self.id_owner = id_owner
        match valute:
            case "RUB":
                self.valute = valute
            case "USD":
                self.valute = valute
            case "EUR":
                self.valute = valute
            case _:
                print("Ошибка: Валюта введена некорректна!")
        self.balance = balance

    def plus(self, sums):
        if sums < 0:
            print("Ошибка: Сумма пополнения некорректна!")
        else:
             self.balance += sums

    def minus(self, sums):
        if sums > self.balance:
            print(f"Ошибка: средств на балансе меньше, чем сумма снятия")
        else:
            self.balance -= sums


class Client():
    _next_id = 1
    id_client = 0
    full_name = ""

    def __init__(self, full_name):
        self.id_client = Client._next_id
        Client._next_id += 1

        self.full_name = full_name
        self.accounts = []

class Bank():
    clients = {}
    accounts = {}
    def __init__(self):
        self.clients = {}
        self.accounts = {}

    def create_client(self):
      print("--Создание нового клиента банка--")
      print("Введите ФИО нового клиента банка: ")
      name, last_name, first_name = input(), input(), input()
      Member = Client(name, last_name, first_name)
      print("Клиент успешно создан!")
      self.clients[Member.id_client] = Member
      print("Клиент добавлен в список клиентов")

    def create_accounts(self):
        print("--Создание счета для клиента--")




