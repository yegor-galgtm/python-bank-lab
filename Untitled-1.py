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
        class Klient: 
         _id = 1

    def __init__(self, fio):
        self.id = Klient._id
        Klient._id = Klient._id + 1
        self.fio = fio
        self.scheta = []

    def nayti_schet(self, nomer):
        for s in self.scheta:
            if s.nomer == nomer:
                return s
        raise SchetNeNaydenError("счет не найден")
    class Bank:
    def __init__(self):
        self.klienty = {}

    def dobavit_klienta(self, fio):
        if fio == "":
            raise ValueError("фио не может быть пустым")
        k = Klient(fio)
        self.klienty[k.id] = k
        return k

    def vzyat_klienta(self, id_klienta):
        if id_klienta not in self.klienty:
            raise SchetNeNaydenError("клиент не найден")
        return self.klienty[id_klienta]

    def otkryt_schet(self, id_klienta, valuta):
        k = self.vzyat_klienta(id_klienta)
        for s in k.scheta:
            if s.valuta == valuta:
                raise ValutaUzheEstError("у клиента уже есть счет в этой валюте")
        s = Schet(id_klienta, valuta)
        k.scheta.append(s)
        return s

    def zakryt_schet(self, id_klienta, nomer):
        k = self.vzyat_klienta(id_klienta)
        s = k.nayti_schet(nomer)
        if s.balans != 0:
            raise SchetNePustoyError("нельзя закрыть счет, на нем есть деньги")
        k.scheta.remove(s)
            def popolnit(self, id_klienta, nomer, summa):
        k = self.vzyat_klienta(id_klienta)
        s = k.nayti_schet(nomer)
        s.popolnit(summa)

    def snyat(self, id_klienta, nomer, summa):
        k = self.vzyat_klienta(id_klienta)
        s = k.nayti_schet(nomer)
        s.snyat(summa)

    def perevod(self, id_klienta, nomer_ot, nomer_komu, summa):
        k = self.vzyat_klienta(id_klienta)
        s_ot = k.nayti_schet(nomer_ot)

        s_komu = None
        for kl in self.klienty.values():
            for s in kl.scheta:
                if s.nomer == nomer_komu:
                    s_komu = s
        if s_komu is None:
            raise SchetNeNaydenError("счет получателя не найден")
        if s_ot.id_klienta == s_komu.id_klienta:
            raise ValueError("нельзя переводить самому себе")
        if s_ot.valuta != s_komu.valuta:
            raise ValutaNeSovpadaetError("валюты счетов не совпадают")

        s_ot.snyat(summa)
        s_komu.popolnit(summa)
            def sdelat_vypisku(self, id_klienta):
        k = self.vzyat_klienta(id_klienta)
        imya = "statement_" + str(id_klienta) + ".txt"
        f = open(imya, "w", encoding="utf-8")

        f.write("выписка по счетам: " + k.fio + "\n")
        f.write("дата: " + str(datetime.now()) + "\n")
        f.write("----\n")

        itogi = {}
        if len(k.scheta) == 0:
            f.write("счетов нет\n")
        for s in k.scheta:
            f.write("номер " + str(s.nomer) + " | " + s.valuta + " | " + str(s.balans) + "\n")
            if s.valuta in itogi:
                itogi[s.valuta] = itogi[s.valuta] + s.balans
            else:
                itogi[s.valuta] = s.balans

        f.write("----\n")
        f.write("итоги по валютам:\n")
        for v in itogi:
            f.write(v + ": " + str(itogi[v]) + "\n")
        f.close()
        return imya
    def vvod_celoe(prompt):
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("нужно целое число")


def vvod_summa(prompt):
    while True:
        s = input(prompt).strip().replace(",", ".")
        try:
            x = float(s)
        except ValueError:
            print("нужно число")
            continue
        if x <= 0:
            print("сумма должна быть больше нуля")
            continue
        return x


def vvod_valuty(prompt):
    while True:
        s = input(prompt).strip().upper()
        if s in ["RUB", "USD", "EUR"]:
            return s
        print("можно только RUB, USD, EUR")


def main():
    bank = Bank()

    demo = bank.dobavit_klienta("иванов иван")
    bank.otkryt_schet(demo.id, "RUB")
    bank.otkryt_schet(demo.id, "USD")
    print("тестовый клиент id =", demo.id)

    k = None
    while k is None:
        id_kl = vvod_celoe("введите ваш id: ")
        try:
            k = bank.vzyat_klienta(id_kl)
            print("здравствуйте,", k.fio)
        except SchetNeNaydenError:
            print("клиент не найден")
            otvet = input("создать нового? (y/n): ").strip().lower()
            if otvet == "y":
                fio = input("введите фио: ").strip()
                try:
                    k = bank.dobavit_klienta(fio)
                    print("создан клиент id =", k.id)
                except ValueError as e:
                    print(e)

    while True:
        print("\n1. показать счета")
        print("2. открыть счет")
        print("3. закрыть счет")
        print("4. пополнить")
        print("5. снять")
        print("6. перевод")
        print("7. выписка")
        print("0. выход")

        vybor = input("пункт: ").strip()

        try:
            if vybor == "1":
                if len(k.scheta) == 0:
                    print("у вас нет счетов")
                for s in k.scheta:
                    print(s.nomer, s.valuta, s.balans)

            elif vybor == "2":
                v = vvod_valuty("валюта: ")
                s = bank.otkryt_schet(k.id, v)
                print("открыт счет", s.nomer)

            elif vybor == "3":
                n = vvod_celoe("номер счета: ")
                bank.zakryt_schet(k.id, n)
                print("счет закрыт")

            elif vybor == "4":
                n = vvod_celoe("номер счета: ")
                s = vvod_summa("сумма: ")
                bank.popolnit(k.id, n, s)
                print("пополнено")

            elif vybor == "5":
                n = vvod_celoe("номер счета: ")
                s = vvod_summa("сумма: ")
                bank.snyat(k.id, n, s)
                print("снято")

            elif vybor == "6":
                n1 = vvod_celoe("счет откуда: ")
                n2 = vvod_celoe("счет кому: ")
                s = vvod_summa("сумма: ")
                bank.perevod(k.id, n1, n2, s)
                print("переведено")

            elif vybor == "7":
                imya = bank.sdelat_vypisku(k.id)
                print("выписка сохранена:", imya)

            elif vybor == "0":
                print("пока")
                break

            else:
                print("нет такого пункта")

        except BankError as e:
            print("ошибка:", e)
        except ValueError as e:
            print("ошибка:", e)


if __name__ == "__main__":
    main()