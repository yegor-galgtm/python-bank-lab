from client import Client
from exceptions import CurrencyMismatchError, SameAccountError, AccountNotFoundError

class Bank:

    def __init__(self):
        self.clientList = {}
        self.accountList = {}

    def registration(self, name): #регистрация
        a = Client(name)
        self.clientList[a.ID] = a
        return a #типа вернуть клиента

    def openAccount(self, ownerID, currency): #открытие счета
        if ownerID not in self.clientList:
            raise AccountNotFoundError(f"клиента с ID {ownerID} не существует")
        a = self.clientList[ownerID]
        b = a.addAccount(currency)
        self.accountList[b.ID] = b
        return  b.ID

    def closeAccount(self, ownerID, accountID): #закрытие счета
        if ownerID not in self.clientList:
                raise AccountNotFoundError(f"клиента с ID {ownerID} не существует")
        a = self.clientList[ownerID]
        a.deleteAccount(accountID)
        del self.accountList[accountID]

    def transfer(self, accountID1, accountID2, quantity):
        if accountID1 not in self.accountList:
                    raise AccountNotFoundError(f"счета с ID {accountID1} не существует")
        if accountID2 not in self.accountList:
                    raise AccountNotFoundError(f"счета с ID {accountID2} не существует")
        if accountID1 == accountID2:
            raise SameAccountError("невозможно перевести деньги самому себе")
        a = self.accountList[accountID1]
        b = self.accountList[accountID2]
        if a.currency != b.currency:
            raise CurrencyMismatchError("перевод между счетами разных валют невозможен")
        a.withdraw(quantity)
        b.add(quantity)