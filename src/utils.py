from datetime import datetime
from typing import Any

import pandas as pd



def get_xlsx_data_dict(file_name: str) -> list[dict] | str:
    """Считывает данные о финансовых операциях из excel файла и преобразует их в список словарей"""
    try:
        xlsx_data = pd.read_excel(file_name)
        data_list = xlsx_data.apply(
            lambda row: {
                "operation_date": row["Дата операции"],
                "payment_date": row["Дата платежа"],
                "card_number": row["Номер карты"],
                "status": row["Статус"],
                "operation_sum": row["Сумма операции"],
                "operation_cur": row["Валюта операции"],
                "payment_sum": row["Сумма платежа"],
                "payment_cur": row["Валюта платежа"],
                "cashback": row["Кэшбэк"],
                "category": row["Категория"],
                "MCC": row["MCC"],
                "description": row["Описание"],
                "Bonus": row["Бонусы (включая кэшбэк)"],
                "Invest_bank": row["Округление на инвесткопилку"],
                "rounded_operation_sum": row["Сумма операции с округлением"],
            },
            axis=1,
        )
        new_dict_list = []
        row_index = 0
        for row in data_list:
            new_dict_list.append(data_list[row_index])
            row_index += 1
        return new_dict_list

    except Exception:
        return "Файл не может быть прочитан"

def get_greeting(time_data: str) -> str:
    """Принимает текущее время и возвращает приветствие в зависимости от времени суток"""
    if 0 <= int(time_data[11:13]) <= 5:
        return "Доброй ночи"
    elif 6 <= int(time_data[11:13]) <= 11:
        return "Доброе утро"
    elif 12 <= int(time_data[11:13]) <= 17:
        return "Добрый день"
    else:
        return "Добрый вечер"

def get_time_data() -> str:
    """Возвращает текущее время"""
    time_data = datetime.datetime.now()
    return str(time_data)


def get_card_number_list(transactions: list[dict[Any, Any]]) -> list:
    """Выводит список уникальных номеров карт из списка транзакций"""
    card_list_full = []
    for transaction in transactions:
        if transaction["card_number"]:
            card_list_full.append(transaction["card_number"])
    card_list_short = []
    for card in card_list_full:
        if card not in card_list_short and type(card) is str:
            card_list_short.append(card)
    return card_list_short