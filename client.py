from account import Account
from exceptions import DuplicateCurrencyError, AccountNotEmptyError, AccountNotFoundError

class Client:

    nextID = 1

    def __init__(self, name):
        self.name = name
        self.ID = Client.nextID
        Client.nextID += 1
        self.accountList = {}

    def addAccount(self, currency):
        for acc in self.accountList.values():
            if acc.currency == currency:
                raise DuplicateCurrencyError(f"счет в этой валюте уже существует: {acc.ID}")
        newAcc = Account(self.ID, currency)
        self.accountList[newAcc.ID] = newAcc
        return newAcc

    def deleteAccount(self, accountID):
        if accountID not in self.accountList:
            raise AccountNotFoundError(f"счета с ID {accountID} не существует")
        if self.accountList[accountID].balance != 0:
            raise AccountNotEmptyError(f"баланс ненулевой. он равен: {self.accountList[accountID].balance}")
        del self.accountList[accountID]

