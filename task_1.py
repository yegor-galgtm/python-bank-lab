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
