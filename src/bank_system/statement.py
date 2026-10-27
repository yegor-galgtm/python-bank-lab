from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from bank_system.models.client import Client


def generate_statement(client: Client, directory: Path = Path("statements")) -> Path:

    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"statement_{client.client_id}.txt"

    accounts = client.get_accounts()

    totals: dict = defaultdict(Decimal)
    for account in accounts:
        totals[account.currency] += account.balance

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Выписка по клиенту: {client.name} (ID {client.client_id})\n")
        f.write(f"Дата и время: {datetime.now():%Y-%m-%d %H:%M:%S}\n")
        f.write("Счета:\n")
        if not accounts:
            f.write("Счетов нет\n")
        for account in accounts:
            f.write(
                f"  №{account.number} | {account.currency.value} | "
                f"{account.balance}\n"
            )
        f.write("Итого по валютам:\n")
        for currency, total in totals.items():
            f.write(f"{currency.value}: {total}\n")
    return path