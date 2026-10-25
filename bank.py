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
    def __init__(self, name:str):
        self.name = name
        self.clients: dict[str,Client] = {}
        self.accounts: dict[str,Account] = {}
        
    def register_client(self, full_name:str):
        client = Client(full_name)
        self.clients[client.id] = client
        
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
        
            
        
            
        
        
        
