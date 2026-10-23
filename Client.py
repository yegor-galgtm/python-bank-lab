
class Client:
    _id_client = 0
    def __init__(self, first_name: str, last_name: str, father_name: str, checks: list = None):
        Client._id_client +=1
        self.id_client = Client._id_client
        self.first_name = first_name
        self.last_name = last_name
        self.father_name = father_name

        self.checks = checks if checks is not None else []

    # Удобный метод для вывода информации о клиенте на экран
    def __str__(self):
        return f"Клиент [{self.id_client}]: {self.last_name} {self.first_name} {self.father_name}. Счетов: {len(self.checks)}"
