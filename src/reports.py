from typing import Optional

import pandas as pd

from src.utils import read_file
import datetime


# Интерфейс трат по категории
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    Args:
        transactions: pandas DataFrame - датафрейм с транзакциями
        category: str - название категории
        date: Optional[str] - опциональная дата, по умолчанию None
    Returns:
        отсортированный датафрейм с транзакциями
    """
    # Если дата не передана, то используем текущую дату.
    if date is None:
        date = datetime.date.today()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")

    # Определяем дату на три месяца назад
    three_months_ago = date - datetime.timedelta(3 * 365.25 / 12)
    print(three_months_ago, date)

    # Преобразуем строки с датами в datetime объекты.
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")

    # Отрезаем нужные столбцы из датафрейма
    transactions = transactions.loc[
        :,
        [
            "Дата платежа",
            "Сумма платежа",
            "Валюта платежа",
            "Категория",
        ],
    ]

    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата платежа"] >= three_months_ago)
        & (transactions["Дата платежа"] <= date)
    ]

    sorted_transactions = filtered_transactions.sort_values(by="Дата платежа", ascending=False)

    # Преобразуем даты обратно в строковый формат
    sorted_transactions["Дата платежа"] = sorted_transactions["Дата платежа"].dt.strftime("%d.%m.%Y")

    return sorted_transactions


# Интерфейс трат по дням недели
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты).
    Args:
        transactions: pandas DataFrame - датафрейм с транзакциями
        date: Optional[str] - опциональная дата, по умолчанию None
    Returns:
        отсортированный датафрейм с транзакциями
    """
    # Если дата не передана, то используем текущую дату.
    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    # Определяем дату на три месяца назад
    three_months_ago = date - datetime.timedelta(3 * 365.25 / 12)
    print(three_months_ago, date)

    # Преобразуем строки с датами в datetime объекты.
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    transactions = transactions.loc[
        :,
        [
            "Дата операции",
            "Сумма платежа",
            "Валюта платежа",
            "Категория",
        ],
    ]
    filtered_transactions = transactions[
        (transactions["Дата операции"] >= three_months_ago) & (transactions["Дата операции"] <= date)
    ]
    return filtered_transactions.sort_values(by="Дата операции", ascending=False)


# Интерфейс трат в рабочий/выходной день
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    pass


if __name__ == "__main__":
    transactions_data = read_file("../data/operations.xlsx")

    result = spending_by_category(transactions_data, "Супермаркеты", "31.12.2021")
    print(result)

    # result = spending_by_weekday(transactions_data, "31.12.2021")
    # print(result)
