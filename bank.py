class Account():
    _next_id = 1
    id_owner = 0
    id_account = 0
    valute = '' #RUB USD EUR
    balance = 0

    def __init__(self, valute, balance, id_owner):
        self.id_account = Account._next_id
        Account._next_id += 1

        self.id_owner = id_owner
        self.valute = valute
        self.balance = balance


class Client():
    _next_id = 1
    id_client = 0
    name = ''
    last_name = ''
    first_name = ''

    def __init__(self, name, last_name, first_name):
        self.id_client = Client._next_id
        Client._next_id += 1

        self.name = name
        self.last_name = last_name
        self.first_name = first_name
        self.accounts = []


class Bank():
    def __init__(self):
        self.clients = {}
        self.accounts = {}