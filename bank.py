from client import Client
from account import Account

class Bank:

    def __init__(self):
        self.clientList = []
        self.client_account = {}

    def registration(self, name):
        a = Client(name)
        self.clientList.append(a)
        accountList = set()
        self.client_account[Client.ID] = accountList

    def openAccount(self, ownerID, currency):
        a = Account(ownerID, currency)
        accountList = self.client_account[ownerID]
        accountList.add(a.ID)

    def closeAccount(self, ownerID, accountID):
        accountList = self.client_account[ownerID]
        accountList.discard(accountID)

    # def transfer(self, ownerID1, accountID1, ownerID2, accountID2, quantity):
    #     account1 = self.client_account[ownerID1]
    #     account2 = self.client_account[ownerID2]
    #     account1.