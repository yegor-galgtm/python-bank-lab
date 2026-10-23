class Bank:
    def __init__(self, clients:list=None, accounts:list=None):
        self.clients = clients if clients is not None else []
        self.accounts = accounts if accounts is not None else []