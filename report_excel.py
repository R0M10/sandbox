import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
import os
import io

# Внутренние константы
to_day = datetime.now().strftime('%Y-%m-%d')
rcost = 'equipment_procurement_cost_rub'

# Загрузка и очистка оглавления
df = pd.read_excel('analyze.xlsx')
df.columns = df.columns.str.strip()


df['vendor'] = df['code_name'].str.extract(r'(Dell|DELL|dell)')
df_list = df[df['som']=="INT"]

df_server = df_list[df_list['category'] == 'СЕРВЕР']
df_storage = df_list[df_list['category'] == 'СИСТЕМА ХРАНЕНИЯ ДАННЫХ']
df_notebook = df_list[df_list['category'] == 'ПОРТАТИВНЫЙ КОМПЬЮТЕР']

df_d = df[df['model'] == 'PE R740'].copy()

df_d['qty'] = pd.to_numeric(df_d['qty'], errors='coerce')
df_d[rcost] = pd.to_numeric(df_d[rcost], errors='coerce')

df_pivot = df_list.groupby('category')[rcost].agg(['sum', 'count']).reset_index().sort_values(by=('sum'), ascending=False)
df_pivot = df_pivot.rename(columns={'sum':"Total cost", 'count':"Number of purchases"})

df_d['cost'] = df_d['qty'] * df_d[rcost]

### Формирование графика
plt.figure(figsize=(10,6))
plt.bar(df_pivot['category'], df_pivot['Total cost'], color='skyblue')
plt.title('Сумма закупок по категориям')
plt.xlabel('Категория')
plt.ylabel('Сумма руб.')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
img_buffer = io.BytesIO()
plt.savefig(img_buffer,format='png', dpi=100)
img_buffer.seek(0)
plt.close()

img = Image(img_buffer)

# Отображение нужных столбцов
df_final = df_d[['code_name', "vendor", 'qty', rcost, 'cost']]

# Отчет № 1
with pd.ExcelWriter(f'to_ex_{to_day}.xlsx', engine='openpyxl') as writer:
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
    #A2 означает все что выше 2й строки (т.е. 1я строка), будет закреплено
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

# Отчет № 2
with pd.ExcelWriter(f'report_{to_day}.xlsx') as writer:
    # Записываем данные на нужный листы
    df_list.to_excel(writer, sheet_name='parts', index=False)
    df_server.to_excel(writer, sheet_name='servers', index=False)
    df_storage.to_excel(writer, sheet_name='storages', index=False)
    df_notebook.to_excel(writer, sheet_name='notebook', index=False)
    df_pivot.to_excel(writer, sheet_name='pivot', index=False)

    workbook = writer.book
    worksheet = writer.sheets['pivot']
    img = Image(img_buffer)
    worksheet.add_image(img, 'E2')
    
print('Done')