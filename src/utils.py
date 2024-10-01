import csv
import pandas as pd
import logging


path = "../logs/utils.log"

# Базовые настройки логгера
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(path, "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def _read_csv(csv_file: str) -> pd.DataFrame | None:
    """Принимает на вход путь до CSV-файла и возвращает датафрейм."""
    try:
        csv_data = pd.read_csv(csv_file)
    except FileNotFoundError:
        logger.error(f"Файл {csv_file} не существует.")
        return None

    return csv_data


def _read_xlsx(xlsx_file: str)->pd.DataFrame | None:
    """Принимает на вход путь до XLSX-файла и возвращает датафрейм."""
    try:
        excel_data = pd.read_excel(xlsx_file, na_filter=False)
    except FileNotFoundError:
        logger.error(f"Файл {xlsx_file} не существует.")
        return None

    return excel_data


def read_file(file_path: str) -> pd.DataFrame:
    *_, file_extension = file_path.split(".")
    content = None
    match file_extension:
        case "csv":
            content = _read_csv(file_path)
        case "xlsx":
            content = _read_xlsx(file_path)

    return content


if __name__ == "__main__":
    # print(read_file("../data/operations.csv"))
    # print(read_file("../data/operations.xlsx"))
    # print(read_file("../tests/tests_data/operations.xlsx"))
    print(read_file("../tests/tests_data/operations.csv"))
