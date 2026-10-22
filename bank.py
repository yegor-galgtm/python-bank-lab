import uuid

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
    
    def __init__(self,owner_id:int,currency:str,balance:float=0.0):
        
        if currency not in self.available_currencies:
            raise ValueError("Валюта не поддерживается")
        
        if balance<0:
            raise ValueError("Баланс не может быть отрицательным")
        
        self.owner_id=owner_id
        self.currency=currency
        self.balance=balance
        self.account_number = str(uuid.uuid4())[:8].upper()
    
    def deposit(self,amount:float):
        if amount<0:
            raise ValueError("Сумма должна быть положительной")
        self.balance+=amount
        
    def withdraw(self,amount:float):
        if amount<0:
            raise ValueError("Сумма должна быть положительной")
        if amount<self.balance:
            self.balance-=amount
        else:
            raise ValueError("Недостаточно средств")
        
    def __str__(self):
        return f"Счет №{self.account_number}, владелец:{self.owner_id}, валюта:{self.currency}, баланс:{self.balance}"
    
    class Bank():
        def __init__(self):
            self.client={}
            self.account={}
        
        def add_client(self,client:Client):
            if client.client.ID in self.client:
                raise ValueError("Клиент с таким ID уже существует")
            self.client[client.client.ID]=client
            
            #Продолжить тут!