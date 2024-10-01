import pytest

from src.utils import read_file, _read_csv, _read_xlsx


def test_read_csv_faiure() -> None:
    assert _read_csv("bad/path") == None

def test_read_exls_faiure() -> None:
    assert _read_xlsx("bad/path") == None

def test_read_file_failure() -> None:
    """Тестируем функцию read_file с невалидным аргументом."""
    assert read_file("bad/path") == None

