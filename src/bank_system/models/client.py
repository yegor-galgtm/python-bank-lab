from bank_system.models.account import Account, Currency


class Client:

    def __init__(self, client_id: int, name: str):
        self.client_id = client_id
        self.name = name
        self.accounts: dict[Currency, Account] = {}

    def add_account(self, account: Account) -> None:
        self.accounts[account.currency] = account

    def remove_account(self, currency: Currency) -> None:
        self.accounts.pop(currency)

    def has_currency(self, currency: Currency) -> bool:
        return currency in self.accounts

    def get_accounts(self) -> list[Account]:
        result = []
        for account in self.accounts.values():
            result.append(account)
        return result