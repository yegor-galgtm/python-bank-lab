class Account:
    def __init__(self, owner="Клиент", account_number="0000", initial_balance=0.0):
        self.owner = str(owner)
        self.account_number = str(account_number)
        try:
            self.balance = float(initial_balance)
        except (ValueError, TypeError):
            self.balance = 0.0

    def deposit(self, amount):
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            print("Ошибка: сумма должна быть числом.")
            return False

        if amount > 0:
            self.balance += amount
            print(f"Счет {self.account_number} пополнен на {amount}. Баланс: {self.balance}")
            return True
        else:
            print("Ошибка: сумма пополнения должна быть больше нуля.")
            return False

    def withdraw(self, amount):
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            print("Ошибка: сумма должна быть числом.")
            return False

        if amount <= 0:
            print("Ошибка: сумма снятия должна быть больше нуля.")
            return False
        
        if amount > self.balance:
            print(f"Ошибка: недостаточно средств на счете {self.account_number}.")
            return False
        
        self.balance -= amount
        print(f"Со счета {self.account_number} снято {amount}. Остаток: {self.balance}")
        return True

    def get_balance(self):
        return self.balance

class Bank:
    def __init__(self, name="Центральный Банк"):
        self.name = str(name)
        self.accounts = {}

    def add_account(self, account):
        if not isinstance(account, Account):
            print("Ошибка: можно добавлять только объекты класса Account.")
            return False

        if account.account_number in self.accounts:
            print(f"Счет с номером {account.account_number} уже существует!")
            return False
        else:
            self.accounts[account.account_number] = account
            print(f"Счет {account.account_number} успешно зарегистрирован в банке {self.name}.")
            return True

    def find_account(self, account_number):
        account_number = str(account_number)
        if account_number in self.accounts:
            return self.accounts[account_number]
        else:
            print(f"Счет {account_number} не найден.")
            return None

    def transfer(self, from_acc_num, to_acc_num, amount):
        print(f"\nВыполняется перевод {amount} со счета {from_acc_num} на счет {to_acc_num}...")
        
        from_account = self.find_account(from_acc_num)
        to_account = self.find_account(to_acc_num)

        if from_account is None or to_account is None:
            print("Ошибка перевода: один из счетов не существует.")
            return False

        if from_account.withdraw(amount):
            to_account.deposit(amount)
            print("Перевод успешно выполнен!")
            return True
        else:
            print("Перевод отменен из-за ошибки списания.")
            return False