import datetime
from typing import Optional

import pandas as pd

from src.utils import read_file


def get_date_interval(date_string):
    """Функция определяет диапазон дат на основе правила - с начала месяца, на который выпадает входящая дата,
    по входящую дату.
    Args:
        date_string: Строкове представление входящей даты в формате 'dd.mm.yyyy'.
    Returns:
        begin_date: Строковое представление начала месяца, на который выпадает входящая дата - первая граница диапазона.
        date: Строковое представление входящей даты - вторая граница диапазона.
    """
    date, time = date_string.split()

    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    year = date.year
    month = date.month
    begin_date = datetime.date(year, month, 1)

    return begin_date.strftime("%d.%m.%Y"), date.strftime("%d.%m.%Y")


def get_greeting(date_string):
    """Функция возвращает приветствие: «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости
    от текущего времени. Правило:
    Утро: с 4:00 до 11:00 включительно
    День: с 12:00 до 16:00 включительно
    Вечер: с 17:00 до 23:00 включительно
    Ночь: с 0:00 до 3:00 включительно.
    """
    date, time = date_string.split()
    time = datetime.datetime.strptime(time, "%H:%M:%S").time()
    greeting = ""
    if (
        datetime.datetime.strptime("11:59:59", "%H:%M:%S").time()
        >= time
        > datetime.datetime.strptime("04:00:00", "%H:%M:%S").time()
    ):
        greeting = "Доброе утро"
    elif (
        datetime.datetime.strptime("16:59:59", "%H:%M:%S").time()
        >= time
        > datetime.datetime.strptime("12:00:00", "%H:%M:%S").time()
    ):
        greeting = "Добрый день"
    elif (
        datetime.datetime.strptime("23:59:59", "%H:%M:%S").time()
        >= time
        > datetime.datetime.strptime("17:00:00", "%H:%M:%S").time()
    ):
        greeting = "Добрый вечер"
    elif (
        datetime.datetime.strptime("03:59:59", "%H:%M:%S").time()
        >= time
        > datetime.datetime.strptime("24:00:00", "%H:%M:%S").time()
    ):
        greeting = "Доброй ночи"

    return greeting


def spanding_by_card_numbers(transactions: pd.DataFrame, first_date: Optional[str], last_date: Optional[str]):
    """Функция обрабатывает входящий датафрей и возращает:
    1. Последние 4 цифры номера карты.
    2. Общую сумму расходов по каждой карте.
    3. Кэшбэк (1 рубль на каждые 100 рублей) по каждой карте.
    4. Топ-5 транзакций по сумме платежа.
    Args:
        transactions: transactions: pandas DataFrame - датафрейм с транзакциями
        first_date: Optional[str] - дата начала диапазона
        last_date: Optional[str] - дата конца диапазона
    Returns:
        sums_by_card: pandas DataFrame - сумма расходов по каждой карте
        cashback_by_card: pandas DataFrame - кэшбэк по каждой карте (1 руб на 100 руб)
    """
    # Если переданный в качестве параметра датафрейм пустой датафрейм
    if transactions.empty:
        # logger.info(f"Параметр {transactions} содержит пустой датафрейм.")
        return transactions

    pd.options.mode.copy_on_write = True

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
            "Сумма платежа",
            "Валюта платежа",
        ],
    ]

    # Отфильтруем в датафрейме нужные столбцы (поля) и сортируем по дате операции.
    recent_transactions = transactions[
        (transactions["Дата операции"] >= datetime.datetime.strptime(first_date, "%d.%m.%Y"))
        & (transactions["Дата операции"] <= datetime.datetime.strptime(last_date, "%d.%m.%Y"))
    ]

    # Нужно конвертировать строковые значения трат в числа float. Сначала заменим запятую на точку,
    recent_transactions["Сумма платежа"] = recent_transactions["Сумма платежа"].map(lambda x: x.replace(",", "."))
    # Произведём конвертацию формата.
    recent_transactions["Сумма платежа"] = recent_transactions["Сумма платежа"].map(lambda x: float(x))

    # Добавляем поле с кэшбэком.
    recent_transactions["Кэшбэк"] = recent_transactions["Сумма платежа"].map(lambda x: x / 100)

    # Сортируем по дате платежа.
    sorted_transactions = recent_transactions.sort_values(by="Сумма платежа", ascending=False)

    # Отрежем топ-5 платежей по убыванию.
    top_transactions = sorted_transactions.iloc[:5, :]

    # Сгруппируем операции по номеру карты
    grouped_transactions_by_card = sorted_transactions.groupby("Номер карты")
    # Посчитаем суммы трат по номерам карт.
    sums_by_card = grouped_transactions_by_card["Сумма платежа"].sum()
    # Посчитаем кэшбэки по номерам карт.
    cashback_by_card = grouped_transactions_by_card["Кэшбэк"].sum()

    return sums_by_card, cashback_by_card, top_transactions


def get_currency_rate(currency_list: list):
    pass


def get_responce(date):
    pass


if __name__ == "__main__":
    # Считываем из файла с трансакциями датафрейм
    transactions_data = read_file("../data/operations.csv")

    # Определяем интервал дат в соответствии с ТЗ
    input_date = "2021-12-15 20:00:00"
    date_interval = get_date_interval(input_date)

    # Отсортируем датафрейм по тем полям, которые в дальнейшем будем использовать.
    sums_by_cards, cashback_by_cards, top_transactions = spanding_by_card_numbers(transactions_data, *date_interval)
    print(sums_by_cards)
    print()
    print(cashback_by_cards)
    print()
    print(top_transactions)

    # Получим курсы валют из внешенго API.
    rates = get_currency_rate(caurrencies)
    print()
    print(rates)
