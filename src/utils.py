import logging
import os

import pandas as pd

# Базовые настройки логгера
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("../logs/utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def _read_csv(path: str) -> pd.DataFrame:
    """Принимает на вход путь до CSV-файла и возвращает датафрейм."""
    full_path = os.path.abspath(path)
    csv_data = pd.DataFrame()
    try:
        csv_data = pd.read_csv(full_path, delimiter=";")
        logger.info(f"Файл {full_path} успешно обработан.")
    except FileNotFoundError:
        logger.error(f"Файл {full_path} не существует.")

    return csv_data


def _read_xlsx(path: str) -> pd.DataFrame:
    """Принимает на вход путь до XLSX-файла и возвращает датафрейм."""
    full_path = os.path.abspath(path)
    excel_data = pd.DataFrame()
    try:
        excel_data = pd.read_excel(full_path, na_filter=False)
        logger.info(f"Файл {full_path} успешно обработан.")
    except FileNotFoundError:
        logger.error(f"Файл {full_path} не существует.")

    return excel_data


def read_file(file_path: str) -> pd.DataFrame:
    *_, file_extension = file_path.split(".")
    content = pd.DataFrame()
    match file_extension:
        case "csv":
            content = _read_csv(file_path)
        case "xlsx":
            content = _read_xlsx(file_path)

    return content


if __name__ == "__main__":

    print(read_file("../data/operations.csv"))
    print(read_file("../data/operations.xlsx"))
    print(read_file("../tests/tests_data/operations.xlsx"))
    print(read_file("../tests/tests_data/operations.xlsx"))
