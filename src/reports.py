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
        used_date = datetime.datetime.now()
    else:
        used_date = datetime.datetime.strptime(date, "%d.%m.%Y")

    # Определяем дату на три месяца назад.
    three_months_ago = used_date - datetime.timedelta(3 * 365.25 / 12)

    # Преобразуем дату - отрежем время.
    transactions["Дата операции"] = transactions["Дата операции"].map(lambda x: x[:10])

    # Преобразуем строки с датами в datetime объекты.
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y")

    # Отрезаем нужные столбцы из датафрейма.
    transactions = transactions.loc[
        :,
        [
            "Дата операции",
            "Номер карты",
            "Статус",
            "Сумма платежа",
            "Валюта платежа",
            "Категория",
        ],
    ]

    # Отфильтруем в датафрейме нужные столбцы (поля).
    recent_transactions = transactions[
        (transactions["Статус"] == "OK")
        & (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= used_date)
    ]
    sorted_transactions = recent_transactions.sort_values(by="Дата операции", ascending=False)

    # Преобразуем даты обратно в строковый формат.
    sorted_transactions["Дата операции"] = sorted_transactions["Дата операции"].dt.strftime("%d.%m.%Y")

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
        used_date = datetime.datetime.now()
    else:
        used_date = datetime.datetime.strptime(date, "%d.%m.%Y")

    # Определяем дату на три месяца назад.
    three_months_ago = used_date - datetime.timedelta(3 * 365.25 / 12)

    # Преобразуем дату - отрежем время.
    transactions["Дата операции"] = transactions["Дата операции"].map(lambda x: x[:10])

    # Преобразуем строки с датами в datetime объекты.
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y")

    transactions = transactions.loc[
        :,
        [
            "Дата операции",
            "Номер карты",
            "Статус",
            "Сумма платежа",
            "Валюта платежа",
            "Категория",
        ],
    ]

    # Отфильтруем в датафрейме нужные столбцы (поля).
    recent_transactions = transactions[
        (transactions["Статус"] == "OK")
        & (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= used_date)
    ]

    sorted_transactions = recent_transactions.sort_values(by="Дата операции", ascending=False)

    # Преобразуем даты обратно в строковый формат.
    sorted_transactions["Дата операции"] = sorted_transactions["Дата операции"].dt.strftime("%d.%m.%Y")

    # Нужно конвертировать строковые значения трат в числа float.
    sorted_transactions["Сумма платежа"] = sorted_transactions["Сумма платежа"].map(lambda x: x.replace(",", "."))
    # Заменим запятую на точку,
    sorted_transactions["Сумма платежа"] = sorted_transactions["Сумма платежа"].map(lambda x: float(x))
    # теперь произвыедём конвертацию.
    grouped_transactions = sorted_transactions.groupby("Дата операции")

    # Средни е траты по дням
    avg_weekday_spending = grouped_transactions["Сумма платежа"].mean()

    # Выводим результат
    result = pd.DataFrame(avg_weekday_spending)

    return result


# Интерфейс трат в рабочий/выходной день
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты).
    Args:
        transactions: pandas DataFrame - датафрейм с транзакциями
        date: Optional[str] - опциональная дата, по умолчанию None
    Returns:
        отсортированный датафрейм с транзакциями
    """
    # Если дата не передана, то используем текущую дату.
    if date is None:
        used_date = datetime.datetime.now()
    else:
        used_date = datetime.datetime.strptime(date, "%d.%m.%Y")

    # Определяем дату на три месяца назад.
    three_months_ago = used_date - datetime.timedelta(3 * 365.25 / 12)

    # Преобразуем дату - отрежем время.
    transactions["Дата операции"] = transactions["Дата операции"].map(lambda x: x[:10])

    # Преобразуем строки с датами в datetime объекты.
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y")

    transactions = transactions.loc[
        :,
        [
            "Дата операции",
            "Номер карты",
            "Статус",
            "Сумма платежа",
            "Валюта платежа",
            "Категория",
        ],
    ]

    # Отфильтруем в датафрейме нужные столбцы (поля).
    recent_transactions = transactions[
        (transactions["Статус"] == "OK")
        & (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= used_date)
    ]

    sorted_transactions = recent_transactions.sort_values(by="Дата операции", ascending=False)

    # Нужно конвертировать строковые значения трат в числа float.
    sorted_transactions["Сумма платежа"] = sorted_transactions["Сумма платежа"].map(lambda x: x.replace(",", "."))
    # Заменим запятую на точку,
    sorted_transactions["Сумма платежа"] = sorted_transactions["Сумма платежа"].map(lambda x: float(x))

    # Добавляем колонку с днем недели
    sorted_transactions["День недели"] = sorted_transactions["Дата операции"].dt.weekday

    # Определяем рабочие и выходные дни
    workdays = sorted_transactions[sorted_transactions["День недели"] < 5]
    weekends = sorted_transactions[sorted_transactions["День недели"] >= 5]

    # Считаем средние траты
    avg_workday_spending = workdays["Сумма платежа"].mean()
    avg_weekend_spending = weekends["Сумма платежа"].mean()

    # Выводим результат
    result = pd.DataFrame(
        {
            "День": ["Рабочий", "Выходной"],
            "Средние траты": [round(avg_workday_spending, 2), round(avg_weekend_spending, 2)],
        }
    )
    return result


if __name__ == "__main__":
    transactions_data = read_file("../data/operations.csv")
    result = spending_by_category(transactions_data, "Супермаркеты", "01.12.2021")
    print(result)

    transactions_data = read_file("../data/operations.csv")
    result = spending_by_weekday(transactions_data, "01.12.2021")
    print(result)

    transactions_data = read_file("../data/operations.csv")
    result = spending_by_workday(transactions_data, "01.12.2021")
    print(result)
