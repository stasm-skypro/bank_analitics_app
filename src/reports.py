import logging
from typing import Optional

import pandas as pd
from datetime import datetime, timedelta
from src.utils import read_file

from decorators.decorators import report_writer


path = "../logs/reports.log"

# Базовые настройки логгера
logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(path, "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


# Интерфейс трат по категории
@report_writer()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    Args:
        transactions: pandas DataFrame - датафрейм с транзакциями
        category: str - название категории
        date: Optional[str] - опциональная дата, по умолчанию None
    Returns:
        отсортированный датафрейм с транзакциями
    """
    # Если переданный в качестве параметра датафрейм пустой датафрейм
    if transactions.empty:
        logger.info(f"Параметр {transactions} содержит пустой датафрейм.")
        return transactions

    # Если параметр category не задан, то возвращаем пустой датафрейм.
    if not category:
        logger.error(f"Параметр {category} должен содержать название категории трат.")
        return transactions

    # Если дата не передана, то используем текущую дату.
    if date is None:
        used_date = datetime.now()
    else:
        used_date = datetime.strptime(date, "%d.%m.%Y")

    # Определяем дату на три месяца назад.
    three_months_ago = used_date - timedelta(3 * 365.25 / 12)

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
    logger.info("Функция завершает работу с валидным результатом.")

    return sorted_transactions


# Интерфейс трат по дням недели
@report_writer()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты).
    Args:
        transactions: pandas DataFrame - датафрейм с транзакциями
        date: Optional[str] - опциональная дата, по умолчанию None
    Returns:
        отсортированный датафрейм с транзакциями
        :rtype: object
    """
    # Если переданный в качестве параметра датафрейм пустой датафрейм
    if transactions.empty:
        logger.info(f"Параметр {transactions} содержит пустой датафрейм.")
        return transactions

    # Если дата не передана, то используем текущую дату.
    if date is None:
        used_date = datetime.now()
    else:
        used_date = datetime.strptime(date, "%d.%m.%Y")

    # Определяем дату на три месяца назад.
    three_months_ago = used_date - timedelta(3 * 365.25 / 12)

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
    # теперь произведём конвертацию.
    grouped_transactions = sorted_transactions.groupby("Дата операции")
    # Средние траты по дням
    avg_weekday_spending = grouped_transactions["Сумма платежа"].mean()
    # Выводим результат
    result = pd.DataFrame(avg_weekday_spending)
    logger.info("Функция завершает работу с валидным результатом.")

    return result


# Интерфейс трат в рабочий/выходной день
@report_writer()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты).
    Args:
        transactions: pandas DataFrame - датафрейм с транзакциями
        date: Optional[str] - опциональная дата, по умолчанию None
    Returns:
        отсортированный датафрейм с транзакциями
    """
    # Если переданный в качестве параметра датафрейм пустой датафрейм
    if transactions.empty:
        logger.info(f"Параметр {transactions} содержит пустой датафрейм.")
        return transactions

    # Если дата не передана, то используем текущую дату.
    if date is None:
        used_date = datetime.now()
    else:
        used_date = datetime.strptime(date, "%d.%m.%Y")

    # Определяем дату на три месяца назад.
    three_months_ago = used_date - timedelta(3 * 365.25 / 12)

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
    print(sorted_transactions)
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
    logger.info("Функция завершает работу с валидным результатом.")
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
