
import sys

from Bank import Bank
from Client import Client
from Account import Account
from Exceptions import *
from FileWork import *


def get_positive_float(prompt_text):
    """Безопасно запрашивает положительное число с плавающей точкой."""
    while True:
        try:
            user_input = input(prompt_text).strip()
            amount = float(user_input)
            if amount <= 0:
                print("⚠️ Ошибка! Сумма должна быть строго больше нуля. Попробуйте снова.")
                continue
            return amount
        except ValueError:
            print("⚠️ Ошибка! Некорректный формат. Пожалуйста, введите число (например, 1500.50).")


def get_int(prompt_text):
    """Безопасно запрашивает целое число."""
    while True:
        try:
            return int(input(prompt_text).strip())
        except ValueError:
            print("⚠️ Ошибка! Пожалуйста, введите целое число.")


def find_account_by_id(client, account_id):
    """Ищет объект счета по его ID в списке счетов клиента."""
    for acc in client.checks:
        if acc.id_account == account_id:
            return acc
    # Если не нашли, вернем временный пустой объект для вызова AccountNotFoundError внутри банка
    return Account(id_client=client.id_client, currency="???")


def find_client_by_id(bank, client_id):
    """Ищет клиента по ID в банке. Возвращает None, если не найден."""
    for c in bank.clients:
        if c.id_client == client_id:
            return c
    return None


def client_menu(bank, client):
    """Отображает интерактивное меню операций для авторизованного клиента."""
    while True:
        print(f"\n💻 МЕНЮ КЛИЕНТА: {client.first_name} {client.last_name} (ID: {client.id_client})")
        print("1. Просмотр своих счетов")
        print("2. Открыть новый счет")
        print("3. Пополнение счета")
        print("4. Снятие наличных")
        print("5. Перевод другому клиенту")
        print("6. Закрыть счет")
        print("7. Смена пользователя / Выход")
        print("8. Получить выписку по счетам")

        choice = input("Выберите пункт меню (1-8): ").strip()

        try:
            if choice == "1":
                print("\n--- ВАШИ СЧЕТА ---")
                if not client.checks:
                    print("У вас пока нет открытых счетов.")
                for acc in client.checks:
                    print(acc)

            elif choice == "2":
                currency = input("Введите валюту нового счета (например, RUB, USD, EUR): ").strip().upper()
                if not currency:
                    print("⚠️ Валюта не может быть пустой.")
                    continue
                new_acc = Account(id_client=client.id_client, currency=currency, balance=0.0)
                bank.add_account(new_acc, client)
                print(f"✅ Счет в валюте {currency} успешно открыт! Номер счета: {new_acc.id_account}")

            elif choice == "3":
                acc_id = get_int("Введите номер вашего счета для пополнения: ")
                acc = find_account_by_id(client, acc_id)
                amount = get_positive_float("Введите сумму пополнения: ")
                bank.add_money(client, acc, amount)
                print(f"✅ Баланс успешно пополнен. Текущий баланс: {acc.balance:.2f} {acc.currency}")

            elif choice == "4":
                acc_id = get_int("Введите номер вашего счета для снятия: ")
                acc = find_account_by_id(client, acc_id)
                amount = get_positive_float("Введите сумму снятия: ")
                bank.withdraw_money(client, acc, amount)
                print(f"✅ Деньги успешно сняты. Остаток: {acc.balance:.2f} {acc.currency}")

            elif choice == "5":
                # Сбор данных отправителя
                sender_acc_id = get_int("Введите номер вашего счета, С КОТОРОГО перевести: ")
                sender_acc = find_account_by_id(client, sender_acc_id)

                # Сбор данных получателя
                rec_client_id = get_int("Введите ID клиента-получателя: ")
                recipient = find_client_by_id(bank, rec_client_id)
                if recipient is None:
                    # Создаем фиктивного клиента для корректного перехвата ошибки AccountNotFoundError внутри банка
                    recipient = Client("?", "?", "?")

                rec_acc_id = get_int("Введите номер счета получателя, НА КОТОРЫЙ перевести: ")
                res_acc = find_account_by_id(recipient, rec_acc_id)

                amount = get_positive_float("Введите сумму перевода: ")

                # Вызов метода перевода
                bank.transfer_money(client, sender_acc, amount, recipient, res_acc)
                print(f"✅ Перевод на сумму {amount:.2f} {sender_acc.currency} успешно выполнен!")

            elif choice == "6":
                acc_id = get_int("Введите номер счета, который вы хотите ЗАКРЫТЬ: ")
                acc = find_account_by_id(client, acc_id)
                bank.close_account(client, acc)
                print(f"✅ Счет {acc_id} успешно закрыт и удален из базы банка.")

            elif choice == "7":
                print("Выход из профиля клиента...")
                break
            elif choice == "8":
                bank_extract(client, bank)
            else:
                print("⚠️ Неверный пункт меню. Пожалуйста, выберите число от 1 до 8.")

        # Централизованный  кастомных ошибок
        except AccountNotFoundError as e:
            print(f"❌ Ошибка операции: {e}")
        except DuplicateCurrencyError as e:
            print(f"❌ Ошибка операции: {e}")
        except InsufficientFundsError as e:
            print(f"❌ На счете не хватает денег: {e}")
        except CurrencyMismatchError as e:
            print(f"❌ Ошибка конвертации: {e}")
        except AccountNotEmptyError as e:
            print(f"❌ Ошибка закрытия: {e}")
        except ValueError as e:
            print(f"❌ Некорректное значение: {e}")


def main():
    my_bank = Bank()

    # Стартовый демонстрационный клиент для удобства (ID: 1)
    test_client = Client("Иван", "Иванов", "Иванович")
    my_bank.add_client(test_client)

    print("=" * 25 + " БАНКОВСКАЯ СИСТЕМА ИНИЦИАЛИЗИРОВАНА " + "=" * 25)
    print(f"💡 Для теста: в системе уже есть {test_client} (Используйте ID: 1 для входа)")

    while True:
        print("\n=== ГЛАВНЫЙ ВХОД ===")
        print("1. Войти по ID клиента")
        print("2. Выйти из программы")

        main_choice = input("Выберите действие (1-2): ").strip()

        if main_choice == "1":
            client_id = get_int("Введите ваш ID клиента: ")
            client = find_client_by_id(my_bank, client_id)

            if client is not None:
                print(f"✅ Успешный вход!")
                client_menu(my_bank, client)
            else:
                print("❌ Клиент с таким ID не найден в базе данных банка.")
                create_new = input("Хотите зарегистрировать нового клиента? (да/нет): ").strip().lower()
                if create_new in ['да', 'd', 'yes', 'y']:
                    last_name = input("Введите фамилию: ").strip()
                    first_name = input("Введите имя: ").strip()
                    father_name = input("Введите отчество: ").strip()

                    if not last_name or not first_name:
                        print("⚠️ Ошибка: Имя и Фамилия не могут быть пустыми. Регистрация отменена.")
                        continue

                    new_client = Client(first_name, last_name, father_name)
                    my_bank.add_client(new_client)
                    print(f"🎉 Клиент успешно зарегистрирован! Ваш новый ID клиента: {new_client.id_client}")

                    client_menu(my_bank, new_client)

        elif main_choice == "2":
            print("Спасибо за использование нашего банка. Завершение работы программы.")
            sys.exit()
        else:
            print("⚠️ Неверный выбор. Пожалуйста, введите 1 или 2.")


if __name__ == "__main__":
    main()