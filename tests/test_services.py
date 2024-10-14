import pandas as pd

from src.services import get_increased_cashback_criteria


def test_get_increased_cashback_criteria() -> None:
    data = pd.DataFrame(
        {
            "Дата операции": ["01.04.2023", "05.04.2023", "15.04.2023", "25.04.2023"],
            "Категория": ["Продукты", "Транспорт", "Развлечения", "Продукты"],
            "Кэшбэк": [50, 30, 20, 40],
        }
    )
    year = "2023"
    month = "04"

    expected_output: dict = {"Продукты": 90.0, "Транспорт": 30.0, "Развлечения": 20.0}

    result = get_increased_cashback_criteria(data, year, month)

    assert result == expected_output


def test_get_increased_cashback_criteria_incorrect_data() -> None:
    """Тестируем функцию increased_cashback_criteria для случая, когда передана дата, которой нет в датафрэйме."""
    data = pd.DataFrame(
        {
            "Дата операции": ["01.05.2023", "05.05.2023", "15.05.2023", "25.05.2023"],
            "Категория": ["Продукты", "Транспорт", "Развлечения", "Продукты"],
            "Кэшбэк": [50, 30, 20, 40],
        }
    )
    year = "2023"
    month = "04"

    expected_output: dict = {}

    result = get_increased_cashback_criteria(data, year, month)

    assert result == expected_output
