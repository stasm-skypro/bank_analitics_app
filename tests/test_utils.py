from src.utils import read_file, _read_csv, _read_xlsx


def test_read_csv_faiure() -> None:
    """Тестируем функцию _read_csv при условии передачи в неё несуществующего пути к файлу."""
    assert _read_csv("bad/path") is None


def test_read_xlsx_faiure() -> None:
    """Тестируем функцию _read_xlsx при условии передачи в неё несуществующего пути к файлу."""
    assert _read_xlsx("bad/path") is None


def test_read_file_failure() -> None:
    """Тестируем функцию read_file с невалидным аргументом."""
    assert read_file("bad/path") is None
