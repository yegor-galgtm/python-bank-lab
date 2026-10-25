class InsufficientFundsError(Exception):
    def __init__(self, current_balance, requested_amount):
        # Вычисляем, скольких денег клиенту не хватило для операции
        deficit = requested_amount - current_balance
        message = (f"Недостаточно средств! На счете: {current_balance}, "
                   f"запрошено: {requested_amount} (не хватает: {deficit})")
        super().__init__(message)
        self.current_balance = current_balance
        self.requested_amount = requested_amount
        self.deficit = deficit
