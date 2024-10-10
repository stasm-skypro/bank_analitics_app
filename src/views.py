import datetime
import json

from typing import Optional, Any

import pandas as pd

from src.utils import read_file

import requests
import os
from dotenv import load_dotenv


def get_date_interval(date_string):
    """Функция определяет диапазон дат на основе правила - с начала месяца, на который выпадает входящая дата,
    по входящую дату.
    Args:
        date_string: Строкове представление входящей даты в формате 'dd.mm.yyyy'.
    Returns:
        begin_date: Строковое представление начала месяца, на который выпадает входящая дата - первая граница диапазона,
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
    Утро: с 4:00 до 11:00 включительно,
    День: с 12:00 до 16:00 включительно,
    Вечер: с 17:00 до 23:00 включительно,
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


def spending_by_card_numbers(transactions: pd.DataFrame, first_date: str, last_date: str) -> tuple:
    """Функция обрабатывает входящий датафрей и возращает:
    1. Последние 4 цифры номера карты.
    2. Общую сумму расходов по каждой карте.
    3. Кэшбэк (1 рубль на каждые 100 рублей) по каждой карте.
    4. Топ-5 транзакций по сумме платежа.
    Args:
        transactions: transactions: pandas DataFrame - датафрейм с транзакциями,
        first_date: Optional[str] - дата начала диапазона,
        last_date: Optional[str] - дата конца диапазона,
    Returns:
        sums_by_card: pandas DataFrame - сумма расходов по каждой карте,
        cashback_by_card: pandas DataFrame - кэшбэк по каждой карте (1 руб на 100 руб).
    """
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


def get_currency_rate(from_currency: str, to_currency: str)->str | float:
    """Функция делает запрос к внешнему API и возвращает курс валюты.
    Args:
        from_currency: str - Код валюты, из которой нужно произвести конвертацию
        to_currency: str - Код валюты, в которую нужно произвести конвертацию
    Returns:
        float: курс валюты
    """
    # Загрузка переменных из .env-файла и получение значения API_KEY
    load_dotenv()
    api_key = os.getenv("API_KEY1")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    payload: dict[Any, Any] = {"amount": str(1), "from": from_currency, "to": to_currency}

    response = requests.request("GET", url, headers=headers, params=payload)

    status_code = response.status_code
    # Если запрос обработан успешно (код 200), то возвращаем значение валюты после конвертации.
    if status_code == 200:
        result = json.loads(response.text)["info"]["rate"]
        return float(result)

    # Иначе возвращаем причину ошибки.
    else:
        return response.reason


def get_stock_prices(symbols: list)->dict:
    """
    Функция возвращает стоимости акций на бирже S&P500.
    Args:
        symbols: list - Список акций
    Returns:
        dict - Стоимости акций в виде словаря.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY2")
    api_url = "https://financialmodelingprep.com/api/v3/quote/"

    stock_prices = {}

    for symbol in symbols:
        response = requests.get(f"{api_url}{symbol}?apikey={api_key}")
        data = response.json()
        if data:
            stock_prices[symbol] = data[0]['price']
        else:
            stock_prices[symbol] = None

    return stock_prices


def get_response(input_date: str):

    # Определяем интервал дат в соответствии с ТЗ
    date_interval = get_date_interval(input_date)

    # Считываем из файла с трансакциями датафрейм
    transactions_data = read_file("../data/operations.csv")
    # Отсортируем датафрейм по тем полям, которые в дальнейшем будем использовать.
    sums_by_cards, cashback_by_cards, top_transactions = spending_by_card_numbers(transactions_data, *date_interval)

    # Получим курсы валют из внешнего API.
    currencies = ["USD", "EUR"]
    rates = []
    for currency in currencies:
        rate = get_currency_rate(currency, "RUB")
        rates.append(rate)

    # Получим стоимости акций на бирже S&P500 из списка.
    symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    prices = get_stock_prices(symbols)

    json_response = {

    }




if __name__ == "__main__":
    # # Определяем интервал дат в соответствии с ТЗ
    # input_date = "2021-12-15 20:00:00"
    # date_interval = get_date_interval(input_date)


    # # Считываем из файла с трансакциями датафрейм
    # transactions_data = read_file("../data/operations.csv")
    # # Отсортируем датафрейм по тем полям, которые в дальнейшем будем использовать.
    # sums_by_cards, cashback_by_cards, top_transactions = spending_by_card_numbers(transactions_data, *date_interval)
    # # print(sums_by_cards)
    # # print()
    # # print(cashback_by_cards)
    # # print()
    # # print(top_transactions)


    # # Получим курсы валют из внешнего API.
    # currencies = ["USD", "EUR"]
    # rates = []
    # for currency in currencies:
    #     rate = get_currency_rate(currency, "RUB")
    #     rates.append(rate)
    # # print()
    # # print(rates)


    # # Получим стоимости акций на бирже S&P500 из списка.
    # symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    # prices = get_stock_prices(symbols)
    # # print(prices)

    input_date = "2021-12-15 20:00:00"
    get_response(input_date)