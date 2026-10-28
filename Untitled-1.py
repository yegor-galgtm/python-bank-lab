print("")
class BankError(Exception):
    pass

class NetDenegError(BankError):
    pass

class SchetNeNaydenError(BankError):
    pass

class ValutaNeSovpadaetError(BankError):
    pass

class ValutaUzheEstError(BankError):
    pass

class SchetNePustoyError(BankError):
    pass
class Schet:
    _nomer = 10000001
    valuty = ["RUB", "USD", "EUR"]

    def __init__(self, id_klienta, valuta, balans=0.0):
        self.nomer = Schet._nomer
        Schet._nomer = Schet._nomer + 1
        self.id_klienta = id_klienta
        self.valuta = valuta
        self.balans = balans

    def popolnit(self, summa):
        if summa <= 0:
            raise ValueError("сумма должна быть больше нуля")
        self.balans = self.balans + summa

    def snyat(self, summa):
        if summa <= 0:
            raise ValueError("сумма должна быть больше нуля")
        if summa > self.balans:
            raise NetDenegError("на счете недостаточно денег")
        self.balans = self.balans - summa