class Account:

    nextID = 1
    balance = 0

    def __init__(self, ownerID, currency):
        self.ownerID = ownerID
        self.currency = currency
        self.ID = Account.nextID
        Account.nextID += 1

    def add(self, quantity):
        self.balance += quantity

    def withdraw(self, quantity):
        self.balance -= quantity