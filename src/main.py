from reports import spending_by_category, spending_by_weekday, spending_by_workday
from services import get_increased_cashback_criteria
from utils import read_file
from views import get_response

if __name__ == "__main__":

    print("Привет!")

    print("Задание по категории 'Веб-страницы - Главная'")
    input_date = "2021-12-15 20:00:00"
    json_result = get_response(input_date)
    print("Результат:")
    print(json_result)

    print()
    print("Задание по категории 'Сервисы - Выгодные категории повышенного кешбэка'")
    # Считываем из файла с транзакциями датафрейм
    transactions_data = read_file("../data/operations.csv")
    cashback_json = get_increased_cashback_criteria(transactions_data, "2021", "11")
    print("Результат:")
    print(cashback_json)

    print()
    print("Задание по категории 'Отчёты - все задания'")
    print("Расчёт трат по категории, по дням недели и по выходным и рабочим дням за три месяца от начальной даты.")
    print("Введите начальную дату в формате 'dd.mm.yyyy' (например, 01.12.2021) для начала расчётов.")
    date_from_userinput = input(">>>$: ").strip()
    print("Вы ввели дату:", date_from_userinput)
    print("Траты по категории:")
    print("Введите название категории для фильтрации данных.")
    category_from_userinput = input(">>>$: ").strip()
    print("Вы ввели название категории:", category_from_userinput)
    transactions_data = read_file("../data/operations.csv")
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
