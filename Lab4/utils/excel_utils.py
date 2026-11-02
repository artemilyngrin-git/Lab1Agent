import typing

import pandas as pd


def get_excel_data(filename, sheet_name) -> typing.List:
    """
    Возвращает данные из Excel-файла
    """
    df = pd.read_excel(filename, sheet_name=sheet_name)
    df_index = df.to_dict('index')
    resulted_list = list(df_index.values())
    return resulted_list


def _normalize(text):
    return str(text).lower().replace('ё', 'е').strip()


def find_value(data, *needles):
    needles = [_normalize(n) for n in needles]
    for column, value in data.items():
        name = _normalize(column)
        if all(n in name for n in needles):
            return value
    raise KeyError(f'В данных нет столбца с фрагментами {needles}, есть столбцы: {list(data)}')


def find_coordinate(data, axis):
    twins = {'x': ('x', 'х'), 'y': ('y', 'у')}[axis.lower()]
    for column, value in data.items():
        name = _normalize(column)
        if name.split()[-1] in twins:
            return value
    raise KeyError(f'В данных нет столбца координаты {axis}, есть столбцы: {list(data)}')
