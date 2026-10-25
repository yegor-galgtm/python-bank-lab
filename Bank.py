from decimal import Decimal
from Exceptions import *
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
        if client not in self.clients:
            raise AccountNotFoundError(account, client, self)
        existing_currencies = [existing_acc.currency for existing_acc in client.checks]
        if account.currency  in existing_currencies:
            raise DuplicateCurrencyError(client, account)
        self.accounts.append(account)
        client.checks.append(account)



    def close_account(self, client:Client, account:Account):
        if client not in self.clients or account not in client.checks:
            raise AccountNotFoundError(account, client, self)
        if account.balance!=0:
            raise AccountNotEmptyError(account, client)
        self.accounts.remove(account)
        client.checks.remove(account)


    def add_money(self, client:Client, account:Account, amount:float):
        if client not in self.clients or account not in client.checks:
            raise AccountNotFoundError(account, client, self)
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительным числом")
        account.balance += Decimal(str(amount))


    def withdraw_money(self, client: Client, account: Account, amount: float):
        if client not in self.clients or account not in client.checks:
            raise AccountNotFoundError(account, client, self)
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительным числом")
        if account.balance<Decimal(str(amount)):
            raise InsufficientFundsError(account.balance, Decimal(str(amount)))
        account.balance -= Decimal(str(amount))



    def transfer_money(self, client: Client, account: Account, amount: float, recipient:Client, res_acc:Account):
        if client not in self.clients or account not in client.checks:
            raise AccountNotFoundError(account, client, self)
        if recipient not in self.clients or res_acc not in recipient.checks:
            raise AccountNotFoundError(res_acc, recipient, self)
        if amount <= 0:
            raise ValueError("Сумма перевода должна быть положительным числом")
        if client == recipient:
            raise ValueError("Переводить деньги самому себе нельзя")
        if account.balance<Decimal(str(amount)):
            raise InsufficientFundsError(account.balance, Decimal(str(amount)))
        if account.currency != res_acc.currency:
            raise CurrencyMismatchError(account.currency, res_acc.currency)
        account.balance -= Decimal(str(amount))
        res_acc.balance += Decimal(str(amount))