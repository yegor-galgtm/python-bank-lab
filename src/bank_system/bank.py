from bank_system.exceptions import AccountNotFoundError
from bank_system.models.account import Account, Currency
from bank_system.models.client import Client

class Bank:

    def __init__(self):
        self._clients: dict[int, Client] = {}
        self._accounts: dict[int, Account] = {}
        self._next_id_client = 1

    def register_client(self, name: str) -> Client:
        client = Client(self._next_id_client, name)
        self._clients[client.client_id] = client
        self._next_id_client += 1
        return client

    def get_client(self, client_id: int) -> Client:
        if client_id not in self._clients:
            raise AccountNotFoundError(...)
        return self._clients[client_id]