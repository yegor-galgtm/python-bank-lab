# просто доп функции для удобства ввода

from decimal import Decimal, InvalidOperation

from bank_system.models.account import Currency


def read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Нужно ввести целое число, попробуйте ещё раз.")


def read_amount(prompt: str) -> Decimal:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = Decimal(raw)
        except InvalidOperation:
            print("Введите сумму числом, например 100.50")
            continue
        if not value.is_finite():
            print("Введите сумму числом, например 100.50")
            continue
        if value <= 0:
            print("Сумма должна быть больше нуля.")
            continue
        if value.as_tuple().exponent < -2:
            print("Не больше двух знаков после запятой.")
            continue
        return value


def read_currency(prompt: str) -> Currency:
    available = ", ".join(c.value for c in Currency)
    while True:
        raw = input(prompt).strip().upper()
        try:
            return Currency(raw)
        except ValueError:
            print(f"Неизвестная валюта. Доступны: {available}")


def read_non_empty(prompt: str) -> str:
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("Поле не может быть пустым.")


def read_yes_no(prompt: str) -> bool:
    while True:
        raw = input(prompt + " (д/н): ").strip().lower()
        if raw in ("д", "y"):
            return True
        if raw in ("н", "n"):
            return False
        print("Ответьте «д» или «н».")