from bank_system.bank import Bank
from bank_system.cli.input_utils import (
    read_amount,
    read_currency,
    read_int,
    read_non_empty,
    read_yes_no,
)
from bank_system.exceptions import AccountNotFoundError, BankException
from bank_system.models.account import Account
from bank_system.models.client import Client
from bank_system.statement import generate_statement


class BankCLI:

    def __init__(self, bank: Bank) -> None:
        self.bank = bank
        self.client: Client | None = None
        self._actions = {
            "1": self._show_accounts,
            "2": self._deposit,
            "3": self._withdraw,
            "4": self._transfer,
            "5": self._statement,
            "6": self._open_account,
            "7": self._close_account,
        }

    def run(self) -> None:
        self.client = self._login()
        print(f"\nДобро пожаловать, {self.client.name}!")
        self._main_menu()

    def _login(self) -> Client:
        while True:
            client_id = read_int("Введите ID клиента: ")
            try:
                return self.bank.get_client(client_id)
            except AccountNotFoundError as e:
                print(f"Ошибка: {e}")
                if read_yes_no("Создать нового клиента?"):
                    name = read_non_empty("Введите ФИО: ")
                    client = self.bank.register_client(name)
                    print(f"Готово! Ваш ID: {client.client_id}. Запомните его.")
                    return client

    def _main_menu(self) -> None:
        while True:
            print(
                "\n1. Мои счета\n2. Пополнить счёт\n3. Снять деньги\n"
                "4. Перевод\n5. Выписка\n6. Открыть счёт\n7. Закрыть счёт\n"
                "0. Выход"
            )
            choice = input("Выбор: ").strip()
            if choice == "0":
                print("До свидания!")
                break
            action = self._actions.get(choice)
            if action is None:
                print("Нет такого пункта меню.")
                continue
            try:
                action()
            except BankException as e:
                print(f"Ошибка: {e}")
            except OSError as e:
                print(f"Не удалось сохранить файл: {e}")

    def _get_own_account(self, number: int) -> Account:
        """Счёт по номеру, но только если он принадлежит вошедшему клиенту."""
        account = self.bank.get_account(number)
        if account.owner_id != self.client.client_id:
            raise AccountNotFoundError(f"Счёт №{number} вам не принадлежит")
        return account

    def _show_accounts(self) -> None:
        accounts = self.bank.get_client_accounts(self.client.client_id)
        if not accounts:
            print("У вас пока нет счетов. Откройте счёт (пункт 6).")
            return
        for account in accounts:
            print(f"№{account.number} | {account.currency.value} | {account.balance}")

    def _deposit(self) -> None:
        number = read_int("Номер вашего счёта: ")
        self._get_own_account(number)
        amount = read_amount("Сумма пополнения: ")
        self.bank.deposit(number, amount)
        print("Счёт пополнен.")

    def _withdraw(self) -> None:
        number = read_int("Номер вашего счёта: ")
        self._get_own_account(number)
        amount = read_amount("Сумма снятия: ")
        self.bank.withdraw(number, amount)
        print("Деньги сняты.")

    def _transfer(self) -> None:
        from_number = read_int("С вашего счёта №: ")
        self._get_own_account(from_number)
        to_number = read_int("На счёт №: ")
        amount = read_amount("Сумма перевода: ")
        self.bank.transfer(from_number, to_number, amount)
        print("Перевод выполнен.")

    def _statement(self) -> None:
        path = generate_statement(self.client)
        print(f"Выписка сохранена: {path}")

    def _open_account(self) -> None:
        currency = read_currency("Валюта нового счёта: ")
        account = self.bank.open_account(self.client.client_id, currency)
        print(f"Счёт открыт. Номер: {account.number}")

    def _close_account(self) -> None:
        number = read_int("Номер счёта для закрытия: ")
        self.bank.close_account(self.client.client_id, number)
        print("Счёт закрыт.")