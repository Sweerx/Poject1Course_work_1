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


def get_operations_sum(time_data: str, transactions: list[dict[str, Any]], card_number: str) -> Any:
    """Выводит общую сумму расходов по номеру карты в формате *1234"""
    month = time_data[5:7] + "." + time_data[:4]
    transactions_sum_list = []
    for transaction in transactions:
        date = str(transaction["payment_date"])
        if transaction["card_number"] == card_number and date[3:] == month and transaction["payment_sum"] < 0:
            transactions_sum_list.append(transaction["payment_sum"])
    total_operations_sum = abs(sum(transactions_sum_list))
    return total_operations_sum


def get_cashback_sum(operations_sum: float) -> float:
    """Высчитывает процент кэшбэка от общей суммы(1%)"""
    cash_back_sum = round(operations_sum / 100, 2)
    return cash_back_sum


def show_cards(time_data: str, transactions: list | Any) -> list[dict]:
    """Выводит информацию по каждой карте (последние 4 цифры карты, общая сумма расходов, кэшбэк)"""
    show_cards_list = []
    cards_list = get_card_number_list(transactions)
    for card in cards_list:
        total_spent = get_operations_sum(time_data, transactions, card)
        card_dict = {}
        card_dict["last_digits"] = card[1:]
        card_dict["total_spent"] = get_operations_sum(time_data, transactions, card)
        card_dict["cashback"] = get_cashback_sum(total_spent)
        show_cards_list.append(card_dict)
    return show_cards_list