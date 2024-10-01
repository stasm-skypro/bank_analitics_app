import os

import pytest

from src.utils import read_file


@pytest.mark.parametrize(
    "x, expected",
    [
        ("bad/path", []),
        (os.path.dirname(__file__) + "/data_for_tests/operations_empty_sample.json", []),
        (os.path.dirname(__file__) + "/data_for_tests/operations_notlist_sample.json", []),
    ],
)
def test_read_file_failure(x: str, expected: list) -> None:
    """Тестируем функцию read_file с невалидным аргументом."""
    assert read_file(x) == expected


def test_read_file_success() -> None:
    """Тестируем функцию read_file с валидным аргументом."""
    assert read_file(os.path.dirname(__file__) + "/data_for_tests/operations_sample.json") == [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        }
    ]
