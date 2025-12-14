import os
from datetime import datetime
import calendar
import locale
try: #Установка локализации для русского языка
    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8") #Установка локализации для русского языка
except locale.Error:
    try: #Установка локализации для русского языка  
        locale.setlocale(locale.LC_TIME, "Russian_Russia.1251") #Установка локализации для русского языка
    except locale.Error:
        print("Не удалось установить локализацию для русского языка.") #Ошибка если не удалось установить локализацию для русского языка

#Функция для создания файла
def files_create(month_name, shifts_objects, rate_per_shifts_list, incomes, expenses): 
    format_file = input("Введите желаемый формат файла:(через точку, например .txt,.log): ")
    name_file = input("Какое будет название файла: ").strip()
    files = f'{name_file}-{month_name}{format_file}'
    print(f"Попытка сохранить файл: {files}")
    print(f"Текущая рабочая директория: {os.getcwd()}")
    try:    
        with open(files, 'w', encoding='utf-8') as file:
            # Записываем отдельно списки
            file.write('Смены:\n')
            # записи по сменам (значения)
            file.write(', '.join(str(shift.shifts_val) for shift in shifts_objects) + '\n\n')

            file.write('Ставки:\n')
            file.write(', '.join(str(r) for r in rate_per_shifts_list) + '\n\n')

            file.write('Суммы (доходы):\n')
            file.write(', '.join(str(i) for i in incomes) + '\n\n')

            file.write('Расходы (общий список):\n')
            for exp in expenses:
                file.write(f'{exp}\n')

            # опционально — подробная информация по каждой смене
            file.write('\nПодробно по сменам:\n')
            for shift in shifts_objects:
                file.write(str(shift) + '\n')
        print(f"Данные успешно сохранены в файл: {files}")
    except PermissionError:
        print("Ошибка: Отказано в доступе. Попробуйте сохранить файл в другую папку.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
def expenses_create(expenses_list,for_what,how_much):
    expenses_list.append(f'{for_what} - {how_much}')
    return expenses_list
