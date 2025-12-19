from datetime import datetime
import calendar
import locale
import file as fc


try:  # Установка локализации для русского языка
    locale.setlocale(
        locale.LC_TIME, "ru_RU.UTF-8"
    )  # Установка локализации для русского языка
except locale.Error:
    try:  # Установка локализации для русского языка
        locale.setlocale(
            locale.LC_TIME, "Russian_Russia.1251"
        )  # Установка локализации для русского языка
    except locale.Error:
        print(
            "Не удалось установить локализацию для русского языка."
        )  # Ошибка если не удалось установить локализацию для русского языка

shifts_objects = []  # Смены
rate_per_shifts_list = []  # Ставка за смену
incomes = []  # Доходы
expenses = []  # Расходы
work_yes = ["yes", "y", "да", "го", "д", "н", "lf", "l"]
another_incomes = []  # иные доходы(чай и тп)


class Expenses:  # Класс для трат
    """Представляет одну запись расхода.

    Атрибуты
    ----------
    for_what : str
        Краткое описание или категория расхода (например: 'аренда', 'кофе').
    how_much : int | float
        Потраченная сумма. Ожидается числовой тип (int или float). Для денежных значений
        можно рассмотреть использование decimal.Decimal, чтобы избежать ошибок округления.

    Методы
    -------
    __str__():
        Возвращает человекочитаемое представление расхода в формате 'for_what - how_much'.

    Примечания
    -------
    Этот класс является лёгким контейнером и не выполняет валидацию переданных значений
    (например, на неотрицательность суммы или непустую строку описания).
    """
    def __init__(self, for_what, how_much):
        self.for_what = for_what
        self.how_much = how_much

    def __str__(self):
        """Строковое представление расхода: 'название - сумма'."""
        return f"{self.for_what} - {self.how_much}"


class Shifts:  # Класс для смен
    """
    Представляет рабочую смену с её доходами и расходами.

    Параметры
    ----------
    shifts_val : Any
        Идентификатор или метка смены (например: дата, номер смены или описательная строка).
    rps : float | int
        Доход за смену (или другой числовой показатель дохода), связанный со сменой.
    shift_expenses : Sequence[Expenses] | None
        Итерация объектов Expenses, описывающих отдельные статьи расходов для смены.
        Каждый элемент ожидается с реализацией __str__ для читаемого представления.
    total_expenses : float | int
        Суммарная сумма расходов за смену.
    income : float | int
        Доход за смену (например, выручка до вычета расходов или итоговый доход).

    Примечания
    -------
    - Класс сохраняет переданные значения в атрибутах с теми же именами.
    - Реализация __str__ формирует однострочное, человеко-читаемое сводное представление:
      "<shifts_val> - <rps> - [<expense1>, <expense2>, ...] - <total_expenses> - <income>",
      где каждое expense преобразуется с помощью собственного __str__.
    """
    def __init__(self, shifts_val, rps, shift_expenses, total_expenses, income):
        self.shifts_val = shifts_val
        self.rps = rps
        self.shift_expenses = shift_expenses
        self.total_expenses = total_expenses
        self.income = income

month_data = datetime.now().month  # Месяц в виде числа
month_name = calendar.month_name[month_data].lower()  # Месяц в виде строки


# Функция для получения списка трат
def get_expenses():
    shif_expenses = []
    while True:
        for_what = input("Введите название траты(Enter для пропуска): ").strip()

        if not for_what:
            break

        how_much = input(
            "Сколько потратили на эту трату вы(Enter для пропуска): "
        ).strip()
        try:
            amount = float(how_much)
            shif_expenses.append(Expenses(for_what, amount))
            print(f'Расход - "{for_what}" добавлен: {amount}')

            add_more = input("Хотите добавить расходы еще?(Y/N)")
            if add_more not in work_yes:
                break
        except ValueError:
            print("Неправильное значение, запишите правильно все!")
    return shif_expenses


def adding_income():
    """
    Добавляет сторонний доход через интерактивный ввод пользователя.

    Функция:
    - Спрашивает у пользователя, хочет ли он добавить сторонний доход (например, чаевые).
    - При положительном ответе (значение содержится в глобальной коллекции `work_yes`)
        запрашивает у пользователя сумму и источник дохода.
    - Пытается привести введённую сумму к float; при успешном преобразовании:
        - добавляет запись в глобальный список `another_incomes`
            в виде кортежа (исходная_строка_суммы, источник),
        - выводит информацию о добавленном доходе и обновлённом общем доходе 
            (используя сумму глобального списка `incomes` + добавленная сумма).
    - При ошибке преобразования суммы (ValueError) выводит сообщение об ошибке.
    - При отрицательном ответе ничего не делает.

    Побочные эффекты:
    - Взаимодействие с пользователем через input() и print().
    - Изменение глобальной переменной `another_incomes`.
    - Чтение глобальных переменных `work_yes` и `incomes`.

    Возвращаемое значение: None.
    """
    add_income = (
        input(
            "Может хотитите добавить стороний зароботок, например чаевые или тп: (y/n)"
        )
        .strip()
        .lower()
    )
    if add_income in work_yes:
        try:
            another_how = input("Какую сумму: ").strip()
            another_where = input("Откуда получили: ").strip()
            add_income_val = float(another_how)
            another_incomes.append((another_how, another_where))
            print(f"Ваш добавочный доход {another_where} - {add_income_val}")
            print(f"Ваш доход увеличился на {sum(incomes) + add_income_val}")
        except ValueError:
            print("Ошибка значения!")
    else:
        return


# Функция ввод данных
def input_data():
    """
    Prompt the user for shift data and record a shift with its expenses.

    This function interacts with the user via input() to collect:
    - number of shifts ('Смен:')
    - rate per shift ('Ставка:')

    It converts these inputs to floats, computes the income for the entered shifts,
    then obtains a list of expense objects by calling get_expenses(). It computes the
    total expenses for the current shift, creates a Shifts object and appends it to
    the global shifts_objects list, and also records the rate and income.
    """
    shifts = input("Смен:").strip()
    rate_per_shifts = input("Ставка:").strip()
    try:
        shifts_val = float(shifts)
        rps = float(rate_per_shifts)
        income = shifts_val * rps
        shifts_expenses = get_expenses()
        total_expenses = sum(expense.how_much for expense in shifts_expenses)
        shift_obj = Shifts(shifts_val, rps, shifts_expenses, total_expenses, income)
        shifts_objects.append(shift_obj)
        rate_per_shifts_list.append(rps)
        incomes.append(income)
        for expense in shifts_expenses:
            fc.expenses_create(expenses, expense.for_what, expense.how_much)
        print(f"Ваш доходик, без расходов {income}")
        print(f"Ваши расходы {expenses}")
        print(f"Ваш доход с учетом расходов {income - total_expenses}")
        print(f"Всего расходов в списке: {len(expenses)}\n")
    except ValueError:
        print("Ошибка значения!")
    adding_income()
    continue_work = (
        input("Хотите продолжить и перейти к файлам? (Y/N) ").lower().strip()
    )
    if continue_work in work_yes:
        fc.files_create(
            month_name, shifts_objects, rate_per_shifts_list, incomes, expenses
        )
    else:
        return


if __name__ == "__main__":
    input_data()
