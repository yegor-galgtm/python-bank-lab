from locale import currency

import Account
import Client


class Bank:
    def __init__(self, clients:list=None, accounts:list=None):
        self.clients = clients if clients is not None else []
        self.accounts = accounts if accounts is not None else []
    def add_client(self, client:Client):
        self.clients.append(client)
    def add_account(self, account:Account, client:Client):
        existing_currencies = [existing_acc.currency for existing_acc in client.checks]
        if account.currency not in existing_currencies:
            client.checks.append(account)
            self.accounts.append(account)
        else:
            print(f"Ошибка: у клиента уже есть счет в валюте {account.currency}")