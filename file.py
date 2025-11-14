import os
from datetime import datetime
import calendar

#Функция для создания файла
def files_create(month_name, shifts_list, rate_per_shifts_list, incomes, expenses): 
    format_file = input("Введите желаемый формат файла:(через точку, например .txt,.log): ")
    name_file = input("Какое будет название файла: ").strip()
    files = f'{name_file}-{month_name}{format_file}'
    print(f"Попытка сохранить файл: {files}")
    print(f"Текущая рабочая директория: {os.getcwd()}")
    try:    
        with open(files, 'w', encoding='utf-8') as file:
            file.write(f'Смен - {shifts_list}\n')
            file.write(f'Ставка - {rate_per_shifts_list}\n')
            file.write(f'Сумма - {incomes}\n')
            file.write(f'Расходы - {expenses}\n')
        print(f"Данные успешно сохранены в файл: {files}")
    except PermissionError:
        print("Ошибка: Отказано в доступе. Попробуйте сохранить файл в другую папку.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
def expenses_create(expenses_list,for_what,how_much):
    expenses_list.append(f'{for_what} - {how_much}')
    return expenses_list
