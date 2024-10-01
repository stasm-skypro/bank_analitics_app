import json
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


def _read_json(json_file: str) -> list[dict | None]:
    """Принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях."""
    # Если файл, указанный в переменной json_file не существует, то вернуть пустой список.
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            content = f.read()
        logger.info(f"Файл {json_file} открыт на чтение.")
    except FileNotFoundError:
        logger.error(f"Файл {json_file} не существует.")
        return []

    # Если json-файл пустой, то вернуть пустой список.
    try:
        data = json.loads(content)
        logger.info(f"Данные из файла {json_file} прочитаны.")
    except json.JSONDecodeError:
        logger.error(f"Ошибка чтения json из файла {json_file}.")
        return []

    # Если содержимое файла не является списком (содержит несписок), то вернуть пустой список.
    if not isinstance(data, list):
        logger.error(f"Содержимое файла {json_file} не является объектом типа list.")
        return []

    return data


def _read_csv(csv_file: str) -> list:
    """Принимает на вход путь до CSV-файла и возвращает список словарей с данными о финансовых транзакциях."""
    # Если файл, указанный в переменной csv_file не существует, то вернуть пустой список.
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=",")
            data = list(reader)
            logger.info(f"Данные из файла {csv_file} прочитаны.")
    except FileNotFoundError:
        logger.error(f"Файл {csv_file} не существует.")
        return []

    # Если csv-файл пустой, то вернуть пустой список.
    if not data:
        logger.error(f"Ошибка чтения json из файла {csv_file}.")
        return []

    # Если содержимое файла не является списком (содержит несписок), то вернуть пустой список.
    if not isinstance(data, list):
        logger.error(f"Содержимое файла {csv_file} не является объектом типа list.")
        return []

    return data


def _read_xlsx(xlsx_file: str) -> list:
    """Принимает на вход путь до XLSX-файла и возвращает список словарей с данными о финансовых транзакциях."""
    try:
        excel_data = pd.read_excel(xlsx_file, na_filter=False).to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"Файл {xlsx_file} не существует.")
        return []

    # Если xlsx-файл пустой, то вернуть пустой список.
    if not excel_data:
        logger.error(f"Ошибка чтения json из файла {xlsx_file}.")
        return []

    # Если содержимое файла не является списком (содержит несписок), то вернуть пустой список.
    if not isinstance(excel_data, list):
        logger.error(f"Содержимое файла {xlsx_file} не является объектом типа list.")
        return []

    return excel_data


def read_file(file_path: str) -> list[dict | None]:
    *file_name, file_extension = file_path.split(".")
    content: list = []
    match file_extension:
        case "json":
            content = _read_json(file_path)
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
