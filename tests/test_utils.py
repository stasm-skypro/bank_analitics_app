from src.utils import _read_csv, _read_xlsx, read_file


def test_read_csv_faiure() -> None:
    """Тестируем функцию _read_csv при условии передачи в неё несуществующего пути к файлу."""
    assert _read_csv("bad/path").empty


def test_read_xlsx_faiure() -> None:
    """Тестируем функцию _read_xlsx при условии передачи в неё несуществующего пути к файлу."""
    assert _read_xlsx("bad/path").empty


def test_read_file_failure() -> None:
    """Тестируем функцию read_file с невалидным аргументом."""
    assert read_file("bad/path").empty


if __name__ == "__main__":
    test_read_csv_faiure()
    test_read_xlsx_faiure()
    test_read_file_failure()
