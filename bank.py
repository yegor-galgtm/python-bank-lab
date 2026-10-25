class InsufficientFundsError(Exception): #недостаточно средств для снятия/перевода
    pass
class AccountNotFoundError(Exception): #счет или клиент не найден.
    pass
class CurrencyMismatchError(Exception): #попытка перевести средства между счетами разных валют.
    pass
class DuplicateCurrencyError(Exception): #попытка открыть второй счет в той же валюте.
    pass
class AccountNotEmptyError(Exception): #попытка закрыть счет с ненулевым балансом.
    pass
class ClientAlreadyExistsError(Exception): #клиент с таким ID уже существует.
    pass


class Client():
    def __init__(self,ID:int,FIO:str):
        
        if not isinstance(ID, int) or ID <= 0:
            raise ValueError("ID клиента должен быть положительным целым числом")
    
        if not FIO or not str(FIO).strip():
            raise ValueError("ФИО не может быть пустым")
        
        self.ID=ID
        self.FIO=FIO
        self.accounts=[]
        
    def add_account(self,account):
        if account not in self.accounts:
            self.accounts.append(account)
            
    def __str__(self):
        return f"ID пользователя:{self.ID},ФИО :{self.FIO}"

class Account():  
    
    available_currencies=['RUB','USD','EUR']
    
    _count=0
    
    def __init__(self,owner_id:int,currency:str,balance:float=0.0):
        
        if currency not in self.available_currencies:
            raise ValueError("Валюта не поддерживается")
        
        if balance<0:
            raise ValueError("Баланс не может быть отрицательным")
        
        self.owner_id=owner_id
        self.currency=currency
        self.balance=balance
        Account._count+=1
        self.account_number=f"ACC{Account._count:06d}"
    
    def deposit(self,amount:float):
        if amount<=0:
            raise ValueError("Сумма должна быть положительной")
        self.balance+=amount
        
    def withdraw(self,amount:float):
        if amount<=0:
            raise ValueError("Сумма должна быть положительной")
        if amount<=self.balance:
            self.balance-=amount
        else:
            raise InsufficientFundsError("Недостаточно средств")
        
    def __str__(self):
        return f"Счет №{self.account_number}, владелец:{self.owner_id}, валюта:{self.currency}, баланс:{self.balance}"
    
class Bank():
    def __init__(self):
            self.client={}
            self.account={}
        
    def add_client(self,client:Client):
        if client.ID in self.client:
            raise ClientAlreadyExistsError("Клиент с таким ID уже существует")
        self.client[client.ID]=client
            
    def open_account(self, client_id:int, currency:str):
        if client_id not in self.client:
            raise AccountNotFoundError("Клиент не найден")
        if currency not in Account.available_currencies:
            raise ValueError("Валюта не поддерживается")
        
        client=self.client[client_id]
        for i in client.accounts:
            if i.currency==currency:
                raise DuplicateCurrencyError("У клиента уже есть счет в этой валюте")
        
        account=Account(client_id,currency)
        client.add_account(account)
        self.account[account.account_number]=account
        return account
    
    def close_account(self,account_number:str):
        if account_number not in self.account:
            raise AccountNotFoundError("Счёт не найден")
        account=self.account[account_number]
        if account.balance!=0:
            raise AccountNotEmptyError("Нельзя закрыть счёт с ненулевым балансом")
            
        client=self.client[account.owner_id]
        client.accounts.remove(account)
        del self.account[account_number]
    
    def get_account(self, account_number: str):
        if account_number not in self.account:
            raise AccountNotFoundError("Счёт не найден")
        return self.account[account_number]
        
   
    def transfer(self, from_number: str, to_number: str, amount: float):
        if from_number not in self.account or to_number not in self.account:
            raise AccountNotFoundError("Один из счетов не найден")
            
        src = self.account[from_number]
        dst = self.account[to_number]
        
        if src.account_number == dst.account_number:
            raise ValueError("Нельзя перевести на тот же счёт")
        if src.owner_id == dst.owner_id:
            raise ValueError("Нельзя перевести самому себе")
        if src.currency != dst.currency:
            raise CurrencyMismatchError("Перевод возможен только между счетами в одной валюте")
            
        src.withdraw(amount) 
        dst.deposit(amount)
            
        
        
        
    
    
    
    
            
            