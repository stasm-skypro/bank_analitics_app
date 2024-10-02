import pandas as pd
from datetime import datetime
from unittest.mock import patch
from src.reports import spending_by_category

# Пример данных для тестирования
data = {
    "Дата операции": ["2023-07-01", "2023-08-15", "2023-09-10", "2023-10-01"],
    "Сумма платежа": [100, 200, 150, 300],
    "Валюта платежа": ["KZT", "KZT", "KZT", "KZT"],
    "Категория": ["Супермаркеты", "Супермаркеты", "Рестораны", "Супермаркеты"]
}

transactions = pd.DataFrame(data)


# Mock-тест
def test_spending_by_category():
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 10, 1)
        result = spending_by_category(transactions, "Супермаркеты", "2023-07-01")
        expected = transactions.loc[(transactions["Категория"] == "Супермаркеты") & (transactions["Дата операции"] >= "2023-07-01")]
        assert result.equals(expected), "Тест не пройден"


