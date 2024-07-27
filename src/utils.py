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