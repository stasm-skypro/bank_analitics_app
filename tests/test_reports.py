import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import pandas as pd

from src.reports import spending_by_category


# Простой тест для проверки работы функции при передаче пустого датафрейма.
def test_spending_by_category_failure() -> None:
    """Если в качестве первого аргумента передать пустой датафрейм, функйия должа также вернуть пустой датафрейм."""
    assert spending_by_category(pd.DataFrame(), "some_category", "some_date").empty


# Пример данных для тестирования
class TestSpendingByCategory(unittest.TestCase):

    @patch("src.reports.datetime")
    def test_spending_by_category(self, mock_datetime) -> None:
        # Настройка mock для текущей даты
        mock_datetime.now.return_value = datetime(2024, 10, 3)
        mock_datetime.strptime.side_effect = lambda *args, **kw: datetime.strptime(*args, **kw)
        mock_datetime.timedelta = timedelta

        # Пример данных
        data = {
            "Дата операции": ["01.07.2024", "15.08.2024", "20.09.2024", "01.10.2024"],
            "Номер карты": ["1234", "1234", "1234", "1234"],
            "Статус": ["FAILED", "OK", "OK", "OK"],
            "Сумма платежа": [100, 200, 300, 400],
            "Валюта платежа": ["KZT", "KZT", "KZT", "KZT"],
            "Категория": ["еда", "еда", "транспорт", "еда"],
        }
        transactions = pd.DataFrame(data)

        # Ожидаемый результат
        expected_data = {
            "Дата операции": ["01.10.2024", "15.08.2024"],
            "Номер карты": ["1234", "1234"],
            "Статус": ["OK", "OK"],
            "Сумма платежа": [400, 200],
            "Валюта платежа": ["KZT", "KZT"],
            "Категория": ["еда", "еда"],
        }
        expected_df = pd.DataFrame(expected_data)

        # Вызов тестируемой функции
        result = spending_by_category(transactions, "еда")
        print(result)

        # Проверка результата
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))


if __name__ == "__main__":
    unittest.main()
