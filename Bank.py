from decimal import Decimal
import Account
import Client


class Bank:
    def __init__(self, clients:list=None, accounts:list=None):
        self.clients = clients if clients is not None else []
        self.accounts = accounts if accounts is not None else []
    def add_client(self, client:Client):
        if client not in self.clients:
            self.clients.append(client)

    def add_account(self, account:Account, client:Client):
        existing_currencies = [existing_acc.currency for existing_acc in client.checks]
        if account.currency not in existing_currencies:
            client.checks.append(account)
            self.accounts.append(account)
        else:
            print(f"Ошибка: у клиента уже есть счет в валюте {account.currency}")
    def close_account(self, client:Client, account:Account):
        if account in client.checks:
            if account.balance == 0:
                client.checks.remove(account)
                self.accounts.remove(account)
            else:
                print("Ошибка, у клиента на счету есть деньги, счёт не подлежит удалению")
        else:
            print("Ошибка! У данного клиента нет такого аккаунта")
    def add_money(self, client:Client, account:Account, amount:float):
        if account in client.checks:
            if amount > 0:
                account.balance += Decimal(str(amount))
                print(f"Баланс пополнен на: {amount}")
            else:
                print("Ошибка! Сумма пополнения должна быть положительным числом")
        else:
            print("Ошибка! У данного клиента нет такого аккаунта")