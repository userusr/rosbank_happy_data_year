# -*- coding: utf-8 -*-

"""Tools module."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def missing_values_table(df: pd.DataFrame) -> pd.DataFrame:
    """Количество не заполненных значений в DataFrame.

    https://habr.com/post/414613/

    :param df: pd.DataFrame:

    """
    # Всего недостает
    mis_val = df.isnull().sum()
    # Процент недостающих данных
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    # Таблица с результатами
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
    # Переименование столбцов
    mis_val_table_ren_columns = \
        mis_val_table.rename(
            columns={0: 'Missing Values', 1: '% of Total Values'}
        )
    # Сортировка про процентажу
    mis_val_table_ren_columns = \
        mis_val_table_ren_columns[mis_val_table_ren_columns.iloc[:, 1] != 0]\
        .sort_values('% of Total Values', ascending=False)\
        .round(6)
    # Инфо
    print("В выбранном датафрейме " + str(df.shape[1]) + " столбцов.\n"
          "Всего " + str(mis_val_table_ren_columns.shape[0]) +
          " столбцов с неполными данными.")
    # Возврат таблицы с данными
    return mis_val_table_ren_columns


def missing_values_plot(data_train, data_test):
    """График недостающих данных по колонкам.

    https://habr.com/post/414613/

    :param data_train:
    :param data_test:

    """
    fig = plt.figure(figsize=(18, 6))
    miss_train = pd.DataFrame((data_train.isnull().sum())*100/data_train.shape[0]).reset_index()
    miss_test = pd.DataFrame((data_test.isnull().sum())*100/data_test.shape[0]).reset_index()
    miss_train["type"] = "тренировочная"
    miss_test["type"] = "тестовая"
    missing = pd.concat([miss_train, miss_test], axis=0)
    ax = sns.pointplot("index", 0, data=missing, hue="type")
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Доля отсуствующих значений в данных")
    plt.ylabel("Доля в %")
    plt.xlabel("Столбцы")
    return fig, ax


def unique_values_in_object_categry_columns(data):
    """Список ктегориальных колонок с количеством уникальных значений в каждой.

    https://habr.com/post/414613/

    :param data:

    """
    return data.select_dtypes(include=[object, 'category']).apply(pd.Series.nunique, axis=0)
