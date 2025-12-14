from datetime import datetime
import calendar
import locale
import file as fc


try: #Установка локализации для русского языка
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8") #Установка локализации для русского языка
except locale.Error:
    try: #Установка локализации для русского языка  
        locale.setlocale(locale.LC_TIME, "Russian_Russia.1251") #Установка локализации для русского языка
    except locale.Error:
        print("Не удалось установить локализацию для русского языка.") #Ошибка если не удалось установить локализацию для русского языка

shifts_objects = []#Смены
rate_per_shifts_list = []#Ставка за смену
incomes = []#Доходы
expenses = []#Расходы
work_yes = ['yes','y','да','го','д','н','lf','l']
another_incomes = []#иные доходы(чай и тп)

class Expenses:#Класс для трат
    def __init__(self,for_what,how_much):
        self.for_what = for_what
        self.how_much = how_much
    def __str__(self):
        return f'{self.for_what} - {self.how_much}'

class Shifts:#Класс для смен
    def __init__(self,shifts_val,rps,expenses,total_expenses,income):
        self.shifts_val = shifts_val
        self.rps = rps
        self.expenses = expenses
        self.total_expenses = total_expenses
        self.income = income
    def __str__(self):
        return f'{self.shifts_val} - {self.rps} - {self.expenses} - {self.total_expenses} - {self.income}'

month_data = datetime.now().month #Месяц в виде числа
month_name = calendar.month_name[month_data].lower() #Месяц в виде строки

#Функция для получения списка трат
def get_expenses():
    shif_expenses = []
    while True:
        for_what = input('Введите название траты(Enter для пропуска): ').strip()

        if not for_what:
            break

        how_much = input('Сколько потратили на эту трату вы(Enter для пропуска): ').strip()
        try:
            amount = float(how_much)
            shif_expenses.append(Expenses(for_what,amount))
            print(f'Расход - "{for_what}" добавлен: {amount}')

            add_more = input('Хотите добавить расходы еще?(Y/N)')
            if add_more not in work_yes:
                break
        except ValueError:
            print('Неправильное значение, запишите правильно все!')
    return shif_expenses

def adding_income():#Функция для добавления стороннего дохода
    add_income = input('Может хотитите добавить стороний зароботок, например чаевые или тп: (y/n)').strip().lower()
    if add_income in work_yes:
        try:
            another_how = input('Какую сумму: ').strip()
            another_where = input('Откуда получили: ').strip()
            add_income_val = float(another_how)
            another_incomes.append((another_how,another_where))
            print(f'Ваш добавочный доход {another_where} - {add_income_val}')
            print(f'Ваш доход увеличился на {sum(incomes) + add_income_val}')       
        except ValueError:
            print('Ошибка значения!')
    else:
        return
#Функция ввод данных
def input_data():
    shifts = input('Смен:').strip()
    rate_per_shifts = input('Ставка:').strip()
    try:
        shifts_val = float(shifts)
        rps = float(rate_per_shifts)
        income = shifts_val * rps
        shifts_expenses = get_expenses()
        total_expenses = sum(expense.how_much for expense in shifts_expenses)
        shift_obj = Shifts(shifts_val,rps,shifts_expenses,total_expenses,income)
        shifts_objects.append(shift_obj)
        rate_per_shifts_list.append(rps)          # добавляем ставку в список
        incomes.append(income)                    # добавляем сумму/доход в список
        for expense in shifts_expenses:
            fc.expenses_create(expenses,expense.for_what, expense.how_much)
        print(f'Ваш доходик, без расходов {income}')
        print(f'Ваши расходы {expenses}')
        print(f'Ваш доход с учетом расходов {income - total_expenses}')
        print(f'Всего расходов в списке: {len(expenses)}\n')
    except ValueError:
        print('Ошибка значения!')
    adding_income()
    continue_work = input('Хотите продолжить и перейти к файлам? (Y/N) ').lower().strip()
    if continue_work in work_yes:
        fc.files_create(month_name, shifts_objects, rate_per_shifts_list, incomes, expenses)
    else:
        return
input_data()