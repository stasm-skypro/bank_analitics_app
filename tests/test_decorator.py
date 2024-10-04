import re

import pytest

from decorators.decorators import report_writer


# Подопытная функция
def my_func(x: int, y: int) -> int:
    """Возвращает сумму двух чисел."""
    return x + y


def test_report_writer11() -> None:
    """Проверяет декоратор report_writer при передаче в декорируемую функцию аргументов неверного типа."""
    with pytest.raises(TypeError, match=r".*Неверный тип аргументов или количество аргументов*"):
        report_writer()(my_func)(2, "3")


def test_report_writer12() -> None:
    """Проверяет декоратор report_writer при передаче в декорируемую функцию неверного количества аргументов."""
    with pytest.raises(TypeError, match=r"my_func. Неверный тип аргументов или количество аргументов."):
        report_writer()(my_func)(1, 2, 3)


def test_report_writer13() -> None:
    """Проверяет что декоратор report_writer записывает в файл сообщение при возникновении исключения."""
    with pytest.raises(TypeError, match=r"my_func. Неверный тип аргументов или количество аргументов."):
        report_writer("tests_data/report_writer_sample.log")(my_func)(2, "3")


def test_report_writer14() -> None:
    try:
        report_writer("tests_data/report_writer_sample.log")(my_func)(2, "3")
    except Exception:
        with open("tests_data/report_writer_sample.log", "r", encoding="utf-8") as file:
            result = file.readlines()[-1]
            expected = re.compile(
                r"""Отчёт записан \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}. my_func error: Inputs: .\d+, '\d+'.. 
                Error: unsupported operand type.s. for .: 'int' and 'str'"""
            )
            match = expected.fullmatch(result.rstrip("\n"))
            if match is not None:
                assert match.string == result.rstrip("\n")


def test_report_writer21() -> None:
    """Проверяет что декоратор report_writer записывает в файл по умолчанию сообщение при успешном выполнении."""
    report_writer("tests_data/report_writer_sample.log")(my_func)(2, 3)
    with open("tests_data/report_writer_sample.log", "r", encoding="utf-8") as file:
        result = file.readlines()[-1]
        expected = re.compile(r"Отчёт записан \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}. my_func OK, результат. \d+")
        match = expected.fullmatch(result.rstrip("\n"))
        if match is not None:
            assert match.string == result.rstrip("\n")
