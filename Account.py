class Account:
    _id_account_counter=0
    def __init__(self,id_client:int, currency:str, balance:float=0.0):
        Account._id_account_counter+=1
        self.id_account = Account._id_account_counter
        self.id_client = id_client
        self.currency = currency
        self.balance = balance

    def __str__(self) -> str:
        return f"Счет [{self.id_account}]: Владелец ID {self.id_client} | Валюта: {self.currency} | Баланс: {self.balance:.2f}"