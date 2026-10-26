import os
from datetime import datetime

class InsufficientFundsError(Exception):#недостаточно средств для снятия/перевода.
    pass
class AccountNotFoundError(Exception):#счет или клиент не найден.
    pass
class CurrencyMismatchError(Exception):#попытка перевести средства между счетами разных валют.
    pass
class DuplicateCurrencyError(Exception):#попытка открыть второй счет в той же валюте.
    pass
class AccountNotEmptyError(Exception):#попытка закрыть счет с ненулевым балансом.
    pass

class Currency:
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    
class Account:
    _counter = 0
    def __init__(self, owner_id:str, currency:str, balance:float = 0.0):
        Account._counter +=1
        self.number = f"ACC{Account._counter:06d}"
        self.owner_id = owner_id
        self.currency = currency
        self.balance = balance

class Client:
    _counter = 0
    def __init__(self,full_name:str):
        if not full_name or not full_name.strip():
            raise ValueError("ФИО клиента не может быть пустым")
        Client._counter+=1
        self.full_name = full_name
        self.id = str(Client._counter)
        self.accounts: list[Account] = []      
        
class Bank:
    def __init__(self):
        self.clients: dict[str,Client] = {}
        self.accounts: dict[str,Account] = {}
        
    def register_client(self, full_name:str):
        client = Client(full_name)
        self.clients[client.id] = client
        return client
        
    def open_account(self, client_id:str, currency:str):
        client = self.clients.get(client_id)
        if not client:
            raise AccountNotFoundError(f"Клиент с {client_id} не найден!")
        if currency not in (Currency.RUB,Currency.USD,Currency.EUR):
            raise ValueError("Неизвестная валюта!")
        if any(acc.currency == currency for acc in client.accounts):
            raise DuplicateCurrencyError(f"У клиента есть счет в валюте {currency}!")
        account = Account(client_id, currency)
        client.accounts.append(account)
        self.accounts[account.number] = account
        return account
        
    def close_account(self, account_number:str):
        account = self.accounts.get(account_number)
        if not account:
            raise AccountNotFoundError(f"Счет {account_number} не найден!")
        if account.balance != 0:
            raise AccountNotEmptyError(f"Нельзя закрыть счет {account.number} с ненулевым балансом!")
        client = self.clients[account.owner_id]
        client.accounts.remove(account)
        del self.accounts[account.number]
        
    def deposit(self,account_number:str,amount:float=0.0):
        account = self.accounts.get(account_number)
        if not account:
            raise AccountNotFoundError(f"Счет {account_number} не найден!")
        if amount <=0:
            raise ValueError("Нельзя сделать отрицательный или нулевой депозит!")
        account.balance+=amount
    
    def withdraw(self,account_number:str,amount:float=0.0):
        account = self.accounts.get(account_number)
        if not account:
            raise AccountNotFoundError(f"Счет {account_number} не найден!")
        if amount <=0:
            raise ValueError("Нельзя сделать отрицательный или нулевой вывод средств!")
        if amount > account.balance:
            raise InsufficientFundsError(f"Недостаточно средств на счете {account.number}. Баланс:{account.balance}, на вывод:{amount}!")
        account.balance-=amount
        
    def transfer(self, from_numb:str, to_numb:str, amount:float=0.0):
        from_account = self.accounts.get(from_numb)
        to_account = self.accounts.get(to_numb)
        if not from_account or not to_account:
            raise AccountNotFoundError("Не найден один из счетов!")
        if from_account.owner_id == to_account.owner_id or from_account.number == to_account.number:
            raise ValueError("Нельзя переводить деньги самому себе!")
        if from_account.currency != to_account.currency:
            raise CurrencyMismatchError("Нельзя делать перевод на счет с другой валютой!")
        if amount <= 0:
            raise ValueError("Нельзя переводить отрицательное или равное 0 значение!")
        if amount > from_account.balance:
            raise InsufficientFundsError(f"Недостаточно средств на счете {from_account.number}. Баланс:{from_account.balance}, на вывод:{amount}!")
        
        from_account.balance-=amount
        to_account.balance+=amount
        
    def make_statement(self, client_id:str):
        client = self.clients.get(client_id)
        if not client:
            raise AccountNotFoundError(f"Клиент с {client_id} не найден!")
        filename = f"statement_{client.id}.txt"
        now = datetime.now()
        totals: dict[str,float] = {}
        for acc in client.accounts:
            totals[acc.currency] = totals.get(acc.currency, 0.0) + acc.balance
        with open(filename, "w", encoding="utf-8") as f:
            f.write("ВЫПИСКА ПО СЧЕТАМ КЛИЕНТА\n")
            f.write(f"Клиент: {client.full_name} (ID: {client.id})\n")
            f.write(f"Дата генерации: {now:%Y-%m-%d %H:%M:%S}\n")
            if not client.accounts:
                f.write("У клиента нет открытых счетов.\n")
            else:
                f.write("СЧЕТА:\n")
                for acc in client.accounts:
                    f.write(f"  {acc.number} | {acc.currency} | Баланс: {acc.balance:.2f}\n")
                f.write("\nИТОГОВЫЙ БАЛАНС ПО ВАЛЮТАМ:\n")
                for cur, total in totals.items():
                    f.write(f"  {cur}: {total:.2f}\n")
        return filename
    
def _input_amount(prompt):
    try:
        return float(input(prompt).strip().replace(",", "."))
    except ValueError:
        raise ValueError("Сумма должна быть числом")


def _show_accounts(client):
    print("\nВаши счета")
    if not client.accounts:
        print("Счетов пока нет.")
        return
    for acc in client.accounts:
        print(f"  {acc.number} | {acc.currency} | Баланс: {acc.balance:.2f}")


def _pick_own_account(client, action):
    if not client.accounts:
        raise AccountNotFoundError("У вас нет открытых счетов.")
    number = input(f"Введите номер счета для {action}: ").strip()
    if not any(acc.number == number for acc in client.accounts):
        raise AccountNotFoundError(f"Счет {number} не найден среди ваших счетов.")
    return number


def run_cli(bank):
    print("Банк")
    client = None
    while client is None:
        raw_id = input("Введите ID клиента(Enter-если создвть нового): ").strip()

        if raw_id == "":
            name = input("ФИО: ").strip()
            try:
                client = bank.register_client(name)
                print(f"Клиент создан. Ваш ID: {client.id}")
            except ValueError as e:
                print(f"Ошибка: {e}")
            continue

        if raw_id not in bank.clients:
            if input(f"Клиент {raw_id} не найден. Создать нового? (y/n): ").strip().lower() == "y":
                name = input("ФИО: ").strip()
                try:
                    client = bank.register_client(name)
                    print(f"Клиент создан. Ваш ID: {client.id}")
                except ValueError as e:
                    print(f"Ошибка: {e}")
            continue

        client = bank.clients[raw_id]

    print(f"\nЗдравствуйте, {client.full_name}!")

    while True:
        print("\n1. Счета   2. Открыть   3. Закрыть")
        print("4. Пополнить   5. Снять   6. Перевод")
        print("7. Выписка   0. Выход")

        choice = input("Выбор: ").strip()

        try:
            if choice == "1":
                _show_accounts(client)

            elif choice == "2":
                cur = input(f"Валюта ({Currency.RUB}, {Currency.USD}, {Currency.EUR}): ").strip().upper()
                bank.open_account(client.id, cur)
                print("Счет открыт.")

            elif choice == "3":
                _show_accounts(client)
                number = _pick_own_account(client, "закрытия")
                bank.close_account(number)
                print(f"Счет {number} закрыт.")

            elif choice == "4":
                _show_accounts(client)
                number = _pick_own_account(client, "пополнения")
                amount = _input_amount("Сумма: ")
                bank.deposit(number, amount)
                print(f"Пополнено на {amount:.2f}.")

            elif choice == "5":
                _show_accounts(client)
                number = _pick_own_account(client, "снятия")
                amount = _input_amount("Сумма: ")
                bank.withdraw(number, amount)
                print(f"Снято {amount:.2f}.")

            elif choice == "6":
                _show_accounts(client)
                from_n = _pick_own_account(client, "списания")
                to_n = input("Номер счета получателя: ").strip()
                amount = _input_amount("Сумма: ")
                bank.transfer(from_n, to_n, amount)
                print(f"Перевод {amount:.2f} выполнен.")

            elif choice == "7":
                path = bank.make_statement(client.id)
                print(f"Выписка сохранена: {os.path.abspath(path)}")

            elif choice == "0":
                print("До свидания.")
                break

            else:
                print("Нет такого пункта.")

        except (
            InsufficientFundsError,
            AccountNotFoundError,
            CurrencyMismatchError,
            DuplicateCurrencyError,
            AccountNotEmptyError,
            ValueError,
        ) as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    bank = Bank()
    try:
        run_cli(bank)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход.")
        
            
        
            
        
        
        
