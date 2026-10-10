import pandas as pd
import re
from openpyxl.utils import get_column_letter # 

df = pd.read_excel('analyze.xlsx')
df.columns = df.columns.str.strip()

df['Вендор'] = df['Товар'].str.extract(r'(Dell|DELL|dell)')
df_d = df[df['Модель'] == 'PE R740'].copy()

df_d['Количество'] = pd.to_numeric(df_d['Количество'], errors='coerce')
df_d['Стоимость закупки оборудования RUB'] = pd.to_numeric(df_d['Стоимость закупки оборудования RUB'], errors='coerce')

df_d['Затраты'] = df_d['Количество'] * df_d['Стоимость закупки оборудования RUB']

# Отображение нужных столбцов
df_final = df_d[['Товар', "Вендор", 'Количество', 'Стоимость закупки оборудования RUB', 'Затраты']]

# ----
with pd.ExcelWriter('to_ex.xlsx', engine='openpyxl') as writer:
    # Записываем данные на нужный лист
    df_final.to_excel(writer, sheet_name='dell', index=False)

    # Получение доступа к объектам openpyxl 
    workbook = writer.book
    worksheet = writer.sheets['dell']

    # Включаем автофильтр
    # Указываем диапазон от ячейки
    max_row = worksheet.max_row
    max_col = worksheet.max_column
    worksheet.auto_filter.ref = f'A1:{get_column_letter(max_col)}{max_row}'
    
    # Закрепление верхнюю строку
    # команда freeze_panes указывает на ячейку, Перед которой нужно зафиксировать строки\столбцы
    # A2 означает все что выше 2й строки (т.е. 1я строка), будет закреплено
    worksheet.freeze_panes = 'A2'

    # Форматируем столбцы и настраиваем их ширину
    # в openpyxl нумерация столбцов идет с 1
    # 1. Товар ...
    for col_idx in range(1, max_col + 1):
        col_letter = get_column_letter(col_idx)

        #Проходим циклом по каждой ячейке в текущем столбце (пропуская шапку)
        for row_idx in range(2, max_row + 1):
            cell = worksheet.cell(row=row_idx, column=col_idx)

            if cell.value is not None:
                # столбец 3 ( количество) - делаем целым числом
                if col_idx == 3:
                    cell.number_format = '#,##0'
                # столбцы 4 и 5 (стоимость и затраты) - делаем 2 знака после запятой
                else:
                    cell.number_format = '#,##0.00'
        # автоподбор ширины столбцов под размер текста
        max_len = max(len(str(worksheet.cell(row=r, column=col_idx).value or '')) for r in range(1, max_row + 1))
        worksheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

print('Done')