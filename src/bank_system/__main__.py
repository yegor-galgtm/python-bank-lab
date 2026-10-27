from bank_system.bank import Bank
from bank_system.cli.menu import BankCLI


def main() -> None:
    bank = Bank()
    try:
        BankCLI(bank).run()
    except (KeyboardInterrupt, EOFError):    # Ctrl+C или Ctrl+D
        print("\nЗавершение работы.")


if __name__ == "__main__":
    main()