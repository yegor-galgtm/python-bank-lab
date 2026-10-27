from decimal import Decimal

from bank_system.exceptions import (
    AccountNotEmptyError,
    AccountNotFoundError,
    CurrencyMismatchError,
    DuplicateCurrencyError,
    SelfTransferError,
)
from bank_system.models.account import Account, Currency
from bank_system.models.client import Client


class Bank:

    def __init__(self) -> None:
        self._clients: dict[int, Client] = {}
        self._accounts: dict[int, Account] = {}
        self._next_client_id = 1

    def register_client(self, name: str) -> Client:
        client = Client(self._next_client_id, name)
        self._clients[client.client_id] = client
        self._next_client_id += 1
        return client

    def get_client(self, client_id: int) -> Client:
        if client_id not in self._clients:
            raise AccountNotFoundError(f"Клиент с ID {client_id} не найден")
        return self._clients[client_id]

    def get_account(self, number: int) -> Account:
        if number not in self._accounts:
            raise AccountNotFoundError(f"Счёт №{number} не найден")
        return self._accounts[number]

    def get_client_accounts(self, client_id: int) -> list[Account]:
        client = self.get_client(client_id)
        return client.get_accounts()

    def open_account(self, client_id: int, currency: Currency) -> Account:
        client = self.get_client(client_id)
        if client.has_currency(currency):
            raise DuplicateCurrencyError(
                f"У клиента уже есть счёт в валюте {currency.value}"
            )
        account = Account(client_id, currency)
        client.add_account(account)
        self._accounts[account.number] = account
        return account

    def close_account(self, client_id: int, number: int) -> None:
        client = self.get_client(client_id)
        account = self.get_account(number)
        if account.owner_id != client_id:
            raise AccountNotFoundError(f"Счёт №{number} вам не принадлежит")
        if account.balance != 0:
            raise AccountNotEmptyError(
                f"На счёте №{number} остались деньги: {account.balance}"
            )
        client.remove_account(account.currency)
        self._accounts.pop(number)

    def deposit(self, number: int, amount: Decimal) -> None:
        account = self.get_account(number)
        account.deposit(amount)

    def withdraw(self, number: int, amount: Decimal) -> None:
        account = self.get_account(number)
        account.withdraw(amount)

    def transfer(self, from_number: int, to_number: int,
                 amount: Decimal) -> None:
        source = self.get_account(from_number)
        target = self.get_account(to_number)
        if from_number == to_number:
            raise SelfTransferError("Нельзя перевести деньги на тот же счёт")
        if source.currency != target.currency:
            raise CurrencyMismatchError(
                f"Валюты счетов различаются: "
                f"{source.currency.value} и {target.currency.value}"
            )

        source.withdraw(amount)
        target.deposit(amount)