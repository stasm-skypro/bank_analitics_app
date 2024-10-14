import datetime

import pandas as pd

from src.utils import read_file


def get_increased_cashback_criteria(data: pd.DataFrame, year: str, month: str) -> dict:
    """
    Функция анализирует какие категории были наиболее выгодными для выбора в качестве категорий повышенного кешбэка.
    :param data: Данные с транзакциями.
    :param year: Год, за который проводится анализ.
    :param month: Месяц, за который проводится анализ.
    :return: JSON с анализом, сколько на каждой категории можно заработать кэшбэка в указанном месяце года.
    """
    pd.options.mode.copy_on_write = True

    # Преобразуем дату - отрежем время.
    data["Дата операции"] = data["Дата операции"].map(lambda x: x[:10])

    # Преобразуем строки с датами в datetime объекты.
    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y")

    # Отрезаем нужные столбцы из датафрейма.
    reduced_data = data.loc[:, ["Дата операции", "Категория", "Кэшбэк"]]

    # Отфильтруем в датафрейме нужные столбцы (поля).
    day_in_month = {
        "01": 31,
        "02": 28,
        "03": 31,
        "04": 30,
        "05": 31,
        "06": 30,
        "07": 31,
        "08": 31,
        "09": 30,
        "10": 31,
        "11": 30,
        "12": 31,
    }
    recent_transactions = reduced_data[
        (reduced_data["Дата операции"] >= datetime.datetime(int(year), int(month), 1))
        & (reduced_data["Дата операции"] <= datetime.datetime(int(year), int(month), day_in_month[month]))
    ]

    # Заменим все NaN на ноль.
    recent_transactions["Кэшбэк"] = recent_transactions["Кэшбэк"].fillna(0)

    # Сгруппируем по полю Категория и отсортируем по полю Кешбэк.
    grouped_transactions = recent_transactions.groupby("Категория")
    cashback = grouped_transactions["Кэшбэк"].sum().round(2).to_dict()

    return cashback


if __name__ == "__main__":
    # Считываем из файла с транзакциями датафрейм
    transactions_data = read_file("../data/operations.csv")

    cashback_json = get_increased_cashback_criteria(transactions_data, "2021", "11")
    print(cashback_json)
