from typing import Optional

import pandas as pd

from src.utils import read_file


# Интерфейс трат по категории
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    Args:
        transactions: pandas DataFrame - исходный датафрейм с транзакциями
        category: str - название категории
        date: Optional[str] - опциональная дата, по умолчанию None
    Returns:
        датафрейм с транзакциями отсортированный по категории и дате
        """
    transactions = transactions.loc[:, ["Дата операции", "Сумма платежа", "Валюта платежа",  "Категория", ]]
    return transactions.loc[(transactions["Категория"] == "Супермаркеты") & (transactions["Дата операции"] >= "20.12.2021 22:14:18")]


# Интерфейс трат по дням недели
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    pass


# Интерфейс трат в рабочий/выходной день
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    pass


if __name__ == "__main__":
    data = read_file("../tests/tests_data/operations.xlsx")
    result = spending_by_category(data, "Супермаркеты", "01.12.2021")
    print(result)