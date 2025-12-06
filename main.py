from datetime import datetime
import calendar
import os
import locale
import file as fc


try: #Установка локализации для русского языка
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8") #Установка локализации для русского языка
except locale.Error:
    try: #Установка локализации для русского языка  
        locale.setlocale(locale.LC_TIME, "Russian_Russia.1251") #Установка локализации для русского языка
    except locale.Error:
        print("Не удалось установить локализацию для русского языка.") #Ошибка если не удалось установить локализацию для русского языка

shifts_list = []#Смены
rate_per_shifts_list = []#Ставка за смену
incomes = []#Доходы
expenses = []#Расходы
work_yes = ['yes','y','да','го','д','н','lf','l']
another_incomes = []#иные доходы(чай и тп)


month_data = datetime.now().month #Месяц в виде числа
month_name = calendar.month_name[month_data].lower() #Месяц в виде строки

#Функция для получения списка трат
def get_expenses():
    shif_expenses = []
    while True: 
        for_what = input(f'Введите название траты(Enter для пропуска): ').strip()

        if not for_what:
            break

        how_much = input(f'Сколько потратили на эту трату вы(Enter для пропуска): ').strip()
        try:
            amount = float(how_much)
            shif_expenses.append((for_what,amount))
            print(f'Расход - "{for_what}" добавлен: {amount}')

            add_more = input(f'Хотите добавить расходы еще?(Y/N)')
            if add_more not in work_yes:
                break
        except ValueError:
            print('Неправильное значение, запишите правильно все!')
    return shif_expenses

# Функция для добавления доходов, также вызывается в конце всех операций 
def adding_income():
    add_income = input(f'Может хотитите добавить стороний зароботок, например чаевые или тп: (y/n)').strip().lower() 
    if add_income in work_yes:
        try:
            another_how = input(f'Какую сумму: ').strip()
            another_where = input(f'Откуда получили: ').strip() 
            add_income_val = float(another_how)       
            another_incomes.append((another_how,another_where))
            print(f'Ваш добавочный доход {another_where} - {add_income_val}')
            print(f'Ваш доход увеличился на {sum(incomes) + add_income_val}')
        
        except ValueError:
            print(f'Ошибка значения!')
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
        total_expenses = sum(expense[1] for expense in shifts_expenses)
        shifts_list.append(shifts_val)
        rate_per_shifts_list.append(rps)
        incomes.append(income)
        for expense in shifts_expenses:
            fc.expenses_create(expenses,expense[0], expense[1])
        print(f'Ваш доходик, без расходов {income}')
        print(f'Ваши расходы {expenses}')
        print(f'Ваш доход с учетом расходов {income - total_expenses}')
        print(f'Всего расходов в списке: {len(expenses)}\n')
    except ValueError:
        print(f'Ошибка значения!')
    adding_income()
    continue_work = input(f'Хотите продолжить и перейти к файлам? (Y/N) ').lower().strip()
    if continue_work in work_yes:
        fc.files_create(month_name, shifts_list, rate_per_shifts_list, incomes, expenses)
    else:
        return
input_data()