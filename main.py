from datetime import datetime
from decimal import Decimal, InvalidOperation
from bank import Bank
from exceptions import BankError

b = Bank()

#login
while True:
    try:
        clientID = int(input("введите ID клиента "))
    except ValueError:
        print("ID должен быть целым числом")
        continue
    if clientID in b.clientList:
        client = b.clientList[clientID]
        print(f"добро пожаловать, {client.name}")
        break
    ch = input("клиент не найден. зарегистрироваться? (да/нет) ").strip().lower()
    if ch == "да": #регистрация
        name = input("введите фио ").strip()
        if not name:
            print("фио не может быть пустым")
            continue
        client = b.registration(name)
        clientID = client.ID
        print(f"{name} зарегистрирован под ID {client.ID}")
        break
    elif ch == "нет":
        continue
    else:
        print("ответ не распознан")

#меню
while True:
    print("меню")
    print("1. просмотр своих счетов")
    print("2. пополнение счета")
    print("3. снятие средств")
    print("4. перевод средств")
    print("5. формирование выписки")
    print("6. открытие счета")
    print("7. закрытие счета")
    print("8. выход")

    try:
        ch = int(input())

        if ch == 1:
            if not client.accountList:
                print("у вас пока нет счетов")
            else:
                print("ваши счета:")
                for value in client.accountList.values():
                    print(f"ID: {value.ID}  валюта: {value.currency}  баланс: {value.balance}")

        elif ch == 2:
            accountID = int(input("введите ID счета, который хотите пополнить "))
            if accountID not in client.accountList:
                print("у вас нет счета с таким ID")
                continue
            quantity = Decimal(input("введите сумму ").strip().replace(",", "."))
            if not quantity.is_finite() or quantity.as_tuple().exponent < -2:
                raise ValueError
            print(f"баланс до пополнения: {client.accountList[accountID].balance}")
            client.accountList[accountID].add(quantity)
            print(f"баланс после пополнения: {client.accountList[accountID].balance}")

        elif ch == 3:
            accountID = int(input("введите ID счета, с которого хотите снять средства "))
            if accountID not in client.accountList:
                print("у вас нет счета с таким ID")
                continue
            quantity = Decimal(input("введите сумму ").strip().replace(",", "."))
            if not quantity.is_finite() or quantity.as_tuple().exponent < -2:
                raise ValueError
            print(f"баланс до снятия средств: {client.accountList[accountID].balance}")
            client.accountList[accountID].withdraw(quantity)
            print(f"баланс после снятия средств: {client.accountList[accountID].balance}")

        elif ch == 4:
            accountID1 = int(input("введите ID счета, с которого вы хотите перевести "))
            if accountID1 not in client.accountList:
                print("вы не владелец этого счета")
                continue
            accountID2 = int(input("введите ID счета, на который вы хотите перевести "))
            quantity = Decimal(input("введите сумму перевода ").strip().replace(",", "."))
            if not quantity.is_finite() or quantity.as_tuple().exponent < -2:
                raise ValueError
            b.transfer(accountID1, accountID2, quantity)
            print(f"перевод успешно осуществлён. баланс после перевода: {client.accountList[accountID1].balance}")

        elif ch == 5:
            fileName = f"statement_{clientID}.txt"
            totals = {}
            with open(fileName, "w", encoding="utf-8") as f:
                f.write(f"выписка клиента {client.name} (ID {clientID})\n")
                f.write(f"дата и время формирования: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")
                f.write("счета:\n")
                if not client.accountList:
                    f.write("счетов нет\n")
                for value in client.accountList.values():
                    f.write(f"номер: {value.ID}  валюта: {value.currency}  баланс: {value.balance}\n")
                    totals[value.currency] = totals.get(value.currency, 0) + value.balance
                f.write("\nитоговый баланс по валютам:\n")
                for cur, total in totals.items():
                    f.write(f"{cur}: {total}\n")
            print(f"выписка сохранена в файл {fileName}")

        elif ch == 6:
            currency = input("введите валюту, в которой вы хотите открыть счет (например, RUB) ").strip().upper()
            if len(currency) != 3 or not currency.isalpha():
                print("валюта должна состоять из 3 букв, например RUB, USD, EUR")
                continue
            accountID = b.openAccount(clientID, currency)
            print(f"ваш счет с ID {accountID} успешно создан")

        elif ch == 7:
            accountID = int(input("введите номер счета, который вы хотите закрыть "))
            b.closeAccount(clientID, accountID)
            print("счет успешно закрыт")

        elif ch == 8:
            print("до свидания")
            break

        else:
            print("нет такого пункта меню, введите число от 1 до 8")

    except BankError as e:
        print(f"ошибка: {e}")
    except (ValueError, InvalidOperation):
        print("некорректный ввод. введите число в нужном формате (сумма - не более 2 знаков после запятой)")
    except OSError:
        print("не удалось сохранить файл выписки")