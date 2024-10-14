# Финальная работа к модулю 3 
 -- (версия 10.10.2024) --
# Проект 1. Приложение для анализа банковских операций
## Решаемые задачи
Приложение для анализа транзакций, которые находятся в Excel-файле. Приложение генерирует JSON-данные для веб-страниц, формирует Excel-отчеты, а также предоставляет другие сервисы.

### Категория - Веб-страницы: Страница «Главная»
Реализован набор функций и главная функция, принимающую на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
 и возвращающую JSON-ответ со следующими данными:
1. Приветствие в формате "???", где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
2. По каждой карте:
* последние 4 цифры карты;
* общая сумма расходов;
* кешбэк (1 рубль на каждые 100 рублей).
3. Топ-5 транзакций по сумме платежа.
4. Курс валют.
5. Стоимость акций из S&P500.

### Категория - Сервисы: Выгодные категории повышенного кешбэка
Сервис позволяет проанализировать, какие категории были наиболее выгодными для выбора в качестве категорий повышенного кешбэка.
Напишите функцию для анализа выгодности категорий повышенного кешбэка.
На вход функции поступают данные для анализа, год и месяц.
#### Входные параметры:
data — данные с транзакциями;
year — год, за который проводится анализ;
month — месяц, за который проводится анализ.
На выходе — JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года.
#### Выходные параметры
JSON с анализом, сколько на каждой категории можно заработать кешбэка.

### Категория - Отчеты: Траты по категории
Функция принимает на вход:
* датафрейм с транзакциями,
* название категории,
* опциональную дату.
Если дата не передана, то берется текущая дата.
Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).

### Категория - Отчеты:Траты по дням недели
Функция принимает на вход:
* датафрейм с транзакциями,
* опциональную дату.
Если дата не передана, то берется текущая дата.
Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты).

### Категория - Отчеты: Траты в рабочий/выходной день
Функция принимает на вход:
* датафрейм с транзакциями
* опциональную дату.
Если дата не передана, то берется текущая дата.
Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты).

### Проверка работы приложения
Клонируем репозиторий:

        git@github.com:stasm-skypro/bank_analitics_app.git

Запускаем main.py

## Документация и ссылки.
Полное описание задания и ТЗ к функциям находятся по [ссылке](https://my.sky.pro/student-cabinet/stream-module/19727/course-final-work/materials).

## Лицензия.
Скрипты из данного модуля распространяются в познавательных целях, интеллектуальной ценности не имеют и предназначены для свободного копирования кем угодно.
