from datetime import datetime
from exceptions import (
    AccountNotEmptyError,
    AccountNotFoundError,
    BankError,
    CurrencyMismatchError,
    SelfTransferError,
)
from models import Account, Client
class Bank:
    SUPPORTED_CURRENCIES = ("RUB", "USD", "EUR", "BYN")
    def __init__(self):
        self.clients: dict[str, Client] = {}
        self.accounts: dict[str, Account] = {}
    def register_client(self, client_id: str, full_name: str) -> Client:
        client_id = str(client_id).strip()
        full_name = full_name.strip()
        if not client_id or not full_name:
            raise BankError("ID клиента и ФИО не могут быть пустыми.")
        if client_id in self.clients:
            raise BankError(f"Клиент с ID '{client_id}' уже зарегистрирован.")
        client = Client(client_id=client_id, full_name=full_name)
        self.clients[client_id] = client
        return client
    def get_client(self, client_id: str) -> Client:
        client_id = str(client_id).strip()
        if client_id not in self.clients:
            raise AccountNotFoundError(f"Клиент с ID '{client_id}' не найден.")
        return self.clients[client_id]
    def get_account(self, account_number: str) -> Account:
        account_number = str(account_number).strip()
        if account_number not in self.accounts:
            raise AccountNotFoundError(f"Счет №{account_number} не найден.")
        return self.accounts[account_number]
    def open_account(self, client_id: str, currency: str) -> Account:
        client = self.get_client(client_id)
        currency = currency.strip().upper()
        if not currency.isalpha() or len(currency) != 3:
            raise BankError("Код валюты должен состоять из 3 латинских букв (например, RUB, USD, EUR).")
        account = Account(owner_id=client.client_id, currency=currency)
        client.add_account(account)
        self.accounts[account.account_number] = account
        return account
    def close_account(self, client_id: str, account_number: str) -> None:
        client = self.get_client(client_id)
        account = self.get_account(account_number)
        if account.owner_id != client.client_id:
            raise AccountNotFoundError("Указанный счет не принадлежит данному клиенту.")
        if account.balance != 0:
            raise AccountNotEmptyError(
                f"Невозможно закрыть счет №{account.account_number}: "
                f"текущий баланс составляет {account.balance:.2f} {account.currency}."
            )
        client.remove_account(account)
        del self.accounts[account.account_number]
    def deposit(self, account_number: str, amount: float) -> None:
        account = self.get_account(account_number)
        account.deposit(amount)
    def withdraw(self, account_number: str, amount: float) -> None:
        account = self.get_account(account_number)
        account.withdraw(amount)
    def transfer(self, from_account_num: str, to_account_num: str, amount: float) -> None:
        from_acc = self.get_account(from_account_num)
        to_acc = self.get_account(to_account_num)
        self.get_client(from_acc.owner_id)
        self.get_client(to_acc.owner_id)
        if from_acc.account_number == to_acc.account_number or from_acc.owner_id == to_acc.owner_id:
            raise SelfTransferError("Перевод самому себе или на тот же счет запрещен.")
        if from_acc.currency != to_acc.currency:
            raise CurrencyMismatchError(
                f"Несовпадение валют: счет списания ({from_acc.currency}), "
                f"счет зачисления ({to_acc.currency})."
            )
        from_acc.withdraw(amount)
        to_acc.deposit(amount)
    def generate_statement(self, client_id: str) -> str:
        client = self.get_client(client_id)
        filename = f"statement_{client.client_id}.txt"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        totals_by_currency: dict[str, float] = {}
        for acc in client.accounts:
            totals_by_currency[acc.currency] = round(
                totals_by_currency.get(acc.currency, 0.0) + acc.balance, 2
            )
        lines = [
            "=" * 50,
            "ВЫПИСКА ПО СЧЕТАМ КЛИЕНТА",
            "=" * 50,
            f"Дата и время формирования: {now_str}",
            f"ID клиента: {client.client_id}",
            f"ФИО клиента: {client.full_name}",
            "-" * 50,
            "Список счетов:",
        ]
        if not client.accounts:
            lines.append("  У клиента нет открытых счетов.")
        else:
            for acc in client.accounts:
                lines.append(
                    f"  • Счет №{acc.account_number} | Валюта: {acc.currency} | Баланс: {acc.balance:.2f}"
                )
        lines.append("-" * 50)
        lines.append("Итоговый баланс по каждой валюте:")
        if not totals_by_currency:
            lines.append("  0.00")
        else:
            for currency, total in totals_by_currency.items():
                lines.append(f"  • {currency}: {total:.2f}")
        lines.append("=" * 50)
        with open(filename, mode="w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")
        return filename