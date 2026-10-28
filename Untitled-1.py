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