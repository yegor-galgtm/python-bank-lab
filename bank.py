import uuid

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
    def __init__(self,full_name:str):
        if not full_name or not full_name.strip():
            raise ValueError("ФИО клиента не может быть пустым")
        self.full_name = full_name
        self.id = str(uuid.uuid4())
        self.accounts: list[Account] = []      
        
class Bank:
    def __init__(self, name:str):
        self.name = name
        self.clients: dict[str,Client] = {}
        self.accounts: dict[str,Account] = {}

        
