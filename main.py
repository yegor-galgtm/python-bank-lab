from bank import Bank
from exceptions import AccountNotFoundError, BankError, InvalidAmountError
from models import Client
def prompt_amount(prompt_text: str = "Введите сумму: ") -> float:
    raw_value = input(prompt_text).strip().replace(",", ".")
    try:
        amount = float(raw_value)
    except ValueError:
        raise InvalidAmountError("Ошибка ввода: сумма должна быть числом (например, 1500 или 250.50).")
    if amount <= 0:
        raise InvalidAmountError("Сумма операции должна быть строго больше нуля.")
    return amount
def authenticate_client(bank: Bank) -> Client | None:
    while True:
        print("\n" + "=" * 50)
        print("БАНКОВСКАЯ СИСТЕМА — ВХОД")
        print("=" * 50)
        client_id = input("Введите ваш ID клиента (или '0' для выхода из программы): ").strip()
        if client_id == "0":
            return None
        if not client_id:
            print("ID клиента не может быть пустым. Попробуйте снова.")
            continue
        try:
            client = bank.get_client(client_id)
            print(f"\nДобро пожаловать, {client.full_name}!")
            return client
        except AccountNotFoundError:
            print(f"\n[i] Клиент с ID '{client_id}' не найден.")
            choice = input("Хотите зарегистрировать нового клиента с этим ID? (да/нет): ").strip().lower()
            if choice in ("да", "д", "yes", "y", "+"):
                full_name = input("Введите ваше ФИО: ").strip()
                try:
                    client = bank.register_client(client_id, full_name)
                    print(f"Клиент '{client.full_name}' (ID: {client.client_id}) успешно зарегистрирован!")
                    return client
                except BankError as error:
                    print(f"Ошибка {error}")
            else:
                print("Возврат к вводу ID...")
def show_client_accounts(client: Client) -> None:
    print(f"\n--- Счета клиента {client.full_name} (ID: {client.client_id}) ---")
    if not client.accounts:
        print("У вас пока нет открытых счетов.")
    else:
        for acc in client.accounts:
            print(f"  • {acc}")
def verify_own_account(bank: Bank, client: Client, account_number: str) -> str:
    account = bank.get_account(account_number)
    if account.owner_id != client.client_id:
        raise AccountNotFoundError(f"Счет №{account.account_number} не принадлежит вам.")
    return account.account_number
def client_menu(bank: Bank, client: Client) -> bool:
    while True:
        print("\n" + "-" * 50)
        print(f"Личный кабинет: {client.full_name} [ID: {client.client_id}]")
        print("-" * 50)
        print("1. Просмотр моих счетов")
        print("2. Открыть новый счет")
        print("3. Закрыть счет")
        print("4. Пополнить счет")
        print("5. Снять средства")
        print("6. Перевести средства другому клиенту")
        print("7. Сформировать выписку в файл")
        print("8. Сменить клиента (выйти из аккаунта)")
        print("0. Выход из программы")
        print("-" * 50)
        choice = input("Выберите действие (0-8): ").strip()
        try:
            if choice == "1":
                show_client_accounts(client)
            elif choice == "2":
                print(f"Доступные примеры валют: {', '.join(Bank.SUPPORTED_CURRENCIES)}")
                currency = input("Введите трехбуквенный код валюты (например, RUB, USD, EUR): ").strip().upper()
                account = bank.open_account(client.client_id, currency)
                print(f"Открыт новый счет: {account}")
            elif choice == "3":
                show_client_accounts(client)
                if client.accounts:
                    acc_num = input("Введите номер счета для закрытия: ").strip()
                    bank.close_account(client.client_id, acc_num)
                    print(f"Счет №{acc_num} успешно закрыт.")
            elif choice == "4":
                show_client_accounts(client)
                if client.accounts:
                    acc_num = input("Введите номер вашего счета для пополнения: ").strip()
                    verify_own_account(bank, client, acc_num)
                    amount = prompt_amount("Введите сумму пополнения: ")
                    bank.deposit(acc_num, amount)
                    updated_acc = bank.get_account(acc_num)
                    print(f"Счет пополнен. Текущий баланс: {updated_acc.balance:.2f} {updated_acc.currency}")
            elif choice == "5":
                show_client_accounts(client)
                if client.accounts:
                    acc_num = input("Введите номер вашего счета для снятия: ").strip()
                    verify_own_account(bank, client, acc_num)
                    amount = prompt_amount("Введите сумму снятия: ")
                    bank.withdraw(acc_num, amount)
                    updated_acc = bank.get_account(acc_num)
                    print(f"Средства сняты. Остаток на счете: {updated_acc.balance:.2f} {updated_acc.currency}")
            elif choice == "6":
                show_client_accounts(client)
                if client.accounts:
                    from_acc = input("Введите номер вашего счета списания: ").strip()
                    verify_own_account(bank, client, from_acc)
                    to_acc = input("Введите номер счета получателя: ").strip()
                    amount = prompt_amount("Введите сумму перевода: ")
                    bank.transfer(from_acc, to_acc, amount)
                    updated_acc = bank.get_account(from_acc)
                    print(
                        f"Перевод выполнен успешно! "
                        f"Остаток на счете: {updated_acc.balance:.2f} {updated_acc.currency}"
                    )
            elif choice == "7":
                filename = bank.generate_statement(client.client_id)
                print(f"Выписка успешно сохранена в файл: {filename}")
            elif choice == "8":
                print("Выход из текущего аккаунта...")
                return True
            elif choice == "0":
                return False
            else:
                print("Неизвестная команда. Пожалуйста, введите цифру от 0 до 8.")
        except BankError as error:
            print(f"Ошибка операции {error}")
def main() -> None:
    bank = Bank()
    try:
        while True:
            current_client = authenticate_client(bank)
            if current_client is None:
                print("\nЗавершение работы банковской системы. До свидания!")
                break
            switch_user = client_menu(bank, current_client)
            if not switch_user:
                print("\nЗавершение работы банковской системы. До свидания!")
                break
    except (KeyboardInterrupt, EOFError):
        print("\n\nПрограмма принудительно завершена пользователем. До свидания!")
if __name__ == "__main__":
    main()