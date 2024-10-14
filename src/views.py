import datetime
import json
import os
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.utils import read_file


def get_date_interval(date_string: str) -> tuple:
    """Функция определяет диапазон дат на основе правила - с начала месяца,
    на который выпадает входящая дата, по входящую дату.
    Args:
        date_string: Строкове представление входящей даты в формате 'dd.mm.yyyy'.
    Returns:
        begin_date: Строковое представление начала месяца, на который выпадает входящая дата - первая граница диапазона
        date: Строковое представление входящей даты - вторая граница диапазона.
    """
    only_date, _ = date_string.split()

    date = datetime.datetime.strptime(only_date, "%Y-%m-%d")
    year = date.year
    month = date.month
    begin_date = datetime.date(year, month, 1)

    return begin_date.strftime("%d.%m.%Y"), date.strftime("%d.%m.%Y")


def get_greeting(date_string: str) -> str:
    """Функция возвращает приветствие: «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости
    от текущего времени. Правило:
    Утро: с 4:00 до 11:00 включительно,
    День: с 12:00 до 16:00 включительно,
    Вечер: с 17:00 до 23:00 включительно,
    Ночь: с 0:00 до 3:00 включительно.
    """
    _, only_time = date_string.split()
    time = datetime.datetime.strptime(only_time, "%H:%M:%S").time()
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
        > datetime.datetime.strptime("00:00:00", "%H:%M:%S").time()
    ):
        greeting = "Доброй ночи"

    return greeting


def spending_by_card_numbers(transactions: pd.DataFrame, first_date: str, last_date: str) -> tuple:
    """Функция обрабатывает входящий датафрейм и возвращает:
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
        :, ["Дата операции", "Номер карты", "Сумма платежа", "Валюта платежа", "Категория", "Описание"]
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
    top_transactions = sorted_transactions.iloc[:5, :].to_dict(orient="records")

    # Сгруппируем операции по номеру карты
    grouped_transactions_by_card = sorted_transactions.groupby("Номер карты")
    # Посчитаем суммы трат по номерам карт.
    sums_by_card = grouped_transactions_by_card["Сумма платежа"].sum().round(2).to_dict()
    # Посчитаем кэшбэки по номерам карт.
    cashback_by_card = grouped_transactions_by_card["Кэшбэк"].sum().round(2).to_dict()

    return sums_by_card, cashback_by_card, top_transactions


def get_currency_rate(from_currency: str, to_currency: str) -> str | float:
    """Функция делает запрос к внешнему API и возвращает курс валюты.
    Args:
        from_currency: str - Код исходной валюты
        to_currency: str - Код конечной валюты
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


def get_stock_prices(symbols: list) ->dict:
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
            stock_prices[symbol] = data[0]["price"]
        else:
            stock_prices[symbol] = None

    return stock_prices


def get_response(date: str) -> dict:
    """Функция принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ.
    Args:
        date: str - Строка с датой
    Returns:
        json_response: json - словарь с выходными данными. Пример выходных данных:
        {
        "greeting": "Добрый день",
        "cards": [
            {"last_digits": "5814", "total_spent": 1262.00, "cashback": 12.62},
            {"last_digits": "7512", "total_spent": 7.94, "cashback": 0.08}
        ],
        "top_transactions": [
            {"date": "21.12.2021", "amount": 1198.23, "category": "Переводы",
             "description": "Перевод Кредитная карта. ТП 10.2 RUR"},
            {"date": "20.12.2021", "amount": 829.00, "category": "Супермаркеты", "description": "Лента"},
            {"date": "20.12.2021", "amount": 421.00, "category": "Различные товары", "description": "Ozon.ru"},
            {"date": "16.12.2021", "amount": -14216.42, "category": "ЖКХ", "description": "ЖКУ Квартира"},
            {"date": "16.12.2021", "amount": 453.00, "category": "Бонусы", "description": "Кешбэк за обычные покупки"}
        ],
        "currency_rates": [{"currency": "USD", "rate": 73.21}, {"currency": "EUR", "rate": 87.08}],
        "stock_prices": [
            {"stock": "AAPL", "price": 150.12},
            {"stock": "AMZN", "price": 3173.18},
            {"stock": "GOOGL", "price": 2742.39},
            {"stock": "MSFT", "price": 296.71},
            {"stock": "TSLA", "price": 1007.08}
        ]
    }
    """

    # Получим приветствие в соответствии с временем суток согласно ТЗ.
    greeting_string = get_greeting(date)

    # Определяем интервал дат в соответствии с ТЗ
    date_interval = get_date_interval(date)

    # Считываем из файла с транзакциями датафрейм
    transactions_data = read_file("../data/operations.csv")

    # Получим по каждой карте: последние 4 цифры карты, общая сумма расходов, кешбэк (1 рубль на каждые 100 рублей) и
    # Топ-5 транзакций по сумме платежа.
    sums_by_cards, cashback_by_cards, top_transactions = spending_by_card_numbers(transactions_data, *date_interval)

    cards_list = [
        {"last_digits": spnd[0][1:], "total_spent": spnd[1], "cashback": csbk[1]}
        for spnd, csbk in zip(sums_by_cards.items(), cashback_by_cards.items())
    ]

    top_transactions_list = [
        {
            "date": str(rds["Дата операции"]),
            "amount": rds["Сумма платежа"],
            "category": rds["Категория"],
            "description": rds["Описание"],
        }
        for rds in top_transactions
    ]

    # Получим курсы валют из внешнего API.
    currencies = ["USD", "EUR"]
    currency_rates_list = []
    for currency in currencies:
        rate = get_currency_rate(currency, "RUB")
        currency_rates_list.append({"currency": currency, "rate": round(float(rate), 2)})

    # Получим стоимости акций на бирже S&P500 из внешнего API.
    symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    prices = get_stock_prices(symbols)
    stock_prices_list = [{"stock": k, "price": v} for k, v in prices.items()]

    json_response = {
        "greeting": greeting_string,
        "cards": cards_list,
        "top_transactions": top_transactions_list,
        "currency_rates": currency_rates_list,
        "stock_prices": stock_prices_list,
    }

    return json_response


if __name__ == "__main__":
    # Получим стоимости акций на бирже S&P500 из внешнего API.
    symbols = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    prices = get_stock_prices(symbols)
    print(prices)

    # input_date = "2021-12-15 20:00:00"
    # json_result = get_response(input_date)
    # print(json_result)
