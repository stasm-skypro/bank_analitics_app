import json
from typing import Any
from unittest.mock import patch

import pytest

from src.views import get_date_interval, get_greeting


def test_get_date_interval() -> None:
    """Тестируем функцию get_date_interval с валидным аргументом."""

    # Тестовые данные
    date_string = "2023-04-15 20:00:00"
    expected_begin_date = "01.04.2023"
    expected_date = "15.04.2023"

    # Вызов функции
    begin_date, end_date = get_date_interval(date_string)

    # Проверка результатов
    assert begin_date == expected_begin_date
    assert end_date == expected_date


@pytest.mark.parametrize(
    "x, expected_result",
    [
        ("2023-04-15 04:15:00", "Доброе утро"),
        ("2023-04-15 12:15:00", "Добрый день"),
        ("2023-04-15 17:15:00", "Добрый вечер"),
        ("2023-04-15 00:15:00", "Доброй ночи"),
    ],
)
def test_get_greeting(x: str, expected_result: str) -> None:
    """Тестируем функцию get_greeting с валидным аргументом."""

    # Проверка результатов
    assert get_greeting(x) == expected_result


def test_get_currency_rate_success() -> None:
    """Тестируем функцию полученя курса валют при успешном завершении."""
    from_currency = "USD"
    to_currency = "EUR"
    expected_rate = 0.85

    # Пример ответа от API
    mock_response = {"info": {"rate": expected_rate}}

    with patch("requests.request") as mock_request:
        mock_request.return_value.status_code = 200
        mock_request.return_value.text = json.dumps(mock_response)

        from src.views import get_currency_rate

        rate = get_currency_rate(from_currency, to_currency)

        assert rate == expected_rate


def test_get_currency_rate_failure() -> None:
    """Тестируем функцию полученя курса валют в случае ошибки 404."""
    from_currency = "USD"
    to_currency = "EUR"
    expected_reason = "Not Found"

    with patch("requests.request") as mock_request:
        mock_request.return_value.status_code = 404
        mock_request.return_value.reason = expected_reason

        from src.views import get_currency_rate

        reason = get_currency_rate(from_currency, to_currency)

        assert reason == expected_reason


def test_get_stock_prices_success() -> None:
    """Тестируем функцию получения стоимостей акций при успешном завершении."""
    symbols = ["AAPL", "GOOGL"]
    expected_prices = {"AAPL": 150.0, "GOOGL": 2800.0}

    mock_response_aapl = [{"price": 150.0}]
    mock_response_googl = [{"price": 2800.0}]

    def mock_get(url: str) -> MockResponse | None:
        if "AAPL" in url:
            return MockResponse(mock_response_aapl)
        elif "GOOGL" in url:
            return MockResponse(mock_response_googl)
        # return MockResponse(None, status=404)
        return MockResponse({"price": None})

    with patch("requests.get", side_effect=mock_get):
        from src.views import get_stock_prices

        prices = get_stock_prices(symbols)

        assert prices == expected_prices


class MockResponse:
    def __init__(self, json_data: dict, status: int = 200):
        self.json_data = json_data
        self.status_code = status

    def json(self) -> dict:
        return self.json_data


def test_get_stock_prices_failure() -> None:
    """Тестируем функцию получения стоимостей акций в случае ошибки 404."""
    symbols = ["INVALID"]
    expected_prices = {"INVALID": None}

    # mock_response_invalid = []
    mock_response_invalid: dict = {}

    with patch("requests.get") as mock_get:
        mock_get.return_value = MockResponse(mock_response_invalid, status=404)

        from src.views import get_stock_prices

        prices = get_stock_prices(symbols)

        assert prices == expected_prices
