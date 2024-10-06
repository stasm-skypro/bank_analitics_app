from src.utils import read_file
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


if __name__ == "__main__":
    transactions_data = read_file("../data/operations.csv")

    print("Привет!")
    print("Расчёт трат по категории, по дням недели и по выходным и рабочим дням за три месяца от начальной даты.")
    print("Введите начальную дату в формате 'dd.mm.yyyy' (например, 01.12.2021) для начала расчётов.")
    date_from_userinput = input(">>>$: ").strip()
    print("Вы ввели дату:", date_from_userinput)

    print("Траты по категории:")
    print("Введите название категории для фильтрации данных.")
    category_from_userinput = input(">>>$: ").strip()
    print("Вы ввели название категории:", category_from_userinput)
    result = spending_by_category(transactions_data, category_from_userinput, "01.12.2021")
    print(result)

    print()
    print("Траты по дням недели:")
    transactions_data = read_file("../data/operations.csv")
    result = spending_by_weekday(transactions_data, "01.12.2021")
    print(result)

    print()
    print("Траты в рабочий/выходной день:")
    transactions_data = read_file("../data/operations.csv")
    result = spending_by_workday(transactions_data, "01.12.2021")
    print(result)
