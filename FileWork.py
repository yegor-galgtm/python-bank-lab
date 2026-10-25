from datetime import datetime


def save_to_txt(fileName, data):
    with open(fileName, "w", encoding="utf-8") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n")
        f.write(data)
def bank_extract(client, bank):
    if client not in bank.clients:
        print("Ошибка: Данный клиент не зарегистрирован в банке.")
        return
    fileName=f"statement_{client.id_client}.txt"
    data = f"=== ВЫПИСКА ПО СЧЕТАМ КЛИЕНТА ===\n"
    data += f"Клиент: {client.last_name} {client.first_name} {client.father_name} (ID: {client.id_client})\n"
    data+="-"*25+"\n"
    curr_sum={}

    if not client.checks:
        data += "У клиента нет открытых счетов.\n"
    else:
        for check in client.checks:
            curr_sum[check.currency]=curr_sum.get(check.currency, 0) + check.balance
            data+= f"Счет №{check.id_account} | Валюта: {check.currency} | Баланс: {check.balance:.2f}\n"
    data+="-"*25+"\n"
    data+="И того по каждой валюте:\n"
    for key, value in curr_sum.items():
        data+=f"{key}: {value:.2f}\n"
    data+="="*25+"\n"
    save_to_txt(fileName, data)
    print(f"Выписка успешно сформирована и сохранена в файл {fileName}")
