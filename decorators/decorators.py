from datetime import datetime
from typing import Any


def _write_file(filename: str, text: str) -> None:
    """Делает запись сообщения text в файл filename.
    Args:
        text - строка, заканчивающуюся символом перевода каретки '\n'
        filename - путь к файлу, в который производится запись."""
    with open(filename, "a", encoding="utf-8") as file:
        file.writelines(text)
    file.close()


def report_writer(filename: str | None = None) -> Any:
    """Логирует начало и конец выполнения функции, её результаты или возникшие ошибки."""

    def outer_wrapper(func: Any) -> Any:

        def inner_wrapper(*args: tuple, **kwargs: dict) -> Any:
            nonlocal filename
            # Если имя файла отчётов не передано в качестве параметра декоратора, то записываем отчёт в файл\
            # по умолчанию.
            if filename is None:
                filename = f"../logs/{func.__name__}_report.log"

            res = None

            try:
                res = func(*args, **kwargs)

            # Если работа декорируемой функции завершилась с исключением, то в записываем в отчёт сообщение об ошибке.
            except Exception as e:
                if e:
                    error_msg = f"Отчёт записан {datetime.now()}. {func.__name__} error: Inputs: {args}. Error: {e}"
                    _write_file(filename, error_msg + "\n")
                    raise TypeError(f"{func.__name__}. Неверный тип аргументов или количество аргументов.")

            # Если декорируемая функция завершила работу с валидным результатом, то записываем результат в отчёт.
            msg = f"Отчёт записан {datetime.now()}. {func.__name__} OK, результат: {res}"
            _write_file(filename, msg + "\n")

            return res

        return inner_wrapper

    return outer_wrapper


if __name__ == "__main__":

    # @report_writer()
    def my_func(x: int, y: int) -> int:
        return x + y

    # print(my_func(2, 3))
    print(report_writer()(my_func)(2, "3"))
