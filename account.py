from exceptions import InsufficientFundsError, NonPositiveSumError

class Account:

    nextID = 1

    def __init__(self, ownerID, currency):
        self.ownerID = ownerID
        self.currency = currency
        self.ID = Account.nextID
        Account.nextID += 1
        self.balance = 0

    def add(self, quantity): #пополнение счета
        if quantity <= 0:
            raise NonPositiveSumError("вы можете положить на баланс только положительную сумму денег")
        self.balance += quantity

    def withdraw(self, quantity): #снятие средств
        if quantity <= 0:
            raise NonPositiveSumError("вы можете снять с баланса только положительную сумму денег")
        if self.balance < quantity:
            raise InsufficientFundsError(f"недостаточно средств. ваш баланс: {self.balance}")
        self.balance -= quantity