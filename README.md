# Happy Data Year

[Happy Data Year](https://boosters.pro/champ_21) - новогодний чемпионат по
анализу данных от Росбанка.

Вам предстоит предсказать индекс популярности геолокации для размещения
устройства банкоматной сети.

В обучающей выборке находятся данные о геопозиции шести тысяч банкоматов
Росбанка и его партнеров, а также целевая переменная — индекс популярности
банкомата. В тестовой выборке еще две с половиной тысячи банкоматов, разделенных
поровну на публичную и приватную часть.

## Подсказки и разъяснения от организоторов

    Александр Мамаев
    Все ответы одним постом:
    1.  Все банкоматы из одного временного интервала, находились в одной геопозиции
        на протяжении всего времени сбора исходных данных необходимых для расчета
        таргета.
    2.  В системах банка адрес банкомата хранится в виде поля address. Поля
        address_rus, lat, long - восстанавливались на основе поля address. Для части
        банкоматов адрес и местоположение с точностью до дома установить не удалось.
        Но если взять поисковик на букву 'Г' (или любой другой до  'Я' включительно)
        и ввести в него значения поля address можно получить представление о той
        технологии с помощью которой поля заполнялись.  Облегчить процесс
        представления может помочь  "import selenium".
    3.  Id формировался на основе atm_group и уникального внутри каждой группы id
        банкомата. X.sort_values('id') даст Вам понимание его структуры. Самыми
        высокими индексами популярности обладает  группа банкоматов "Росбанка".
        Остальные группы - банкоматы банков партнёров.
    4.  Таргет - функция от объективных показателей связанных с количеством операций
        совершаемых на устройстве в единицу времени.
    5.  PSI таргета между train/test/private во всех попарных комбинациях меньше
        0.05. 
    6.  Статистические тесты Манна-Уитни о равенстве средних не отвергают нулевые
        гипотезы для всех попарных комбинаций  train/test/private.
    7.  Таргет обрезан сверху для удаления из выборки банкоматов, чья популярность не
        объясняется геолокацией банкомата.  
    8.  Разделение train/test/private. Если посмотреть на индексы популярности
        банкоматов стоящих по одному адресу, то можно увидеть, что они очень близки.
        Пересечение множетсв адресов в private  и traine привело бы к лику.  Можно
        конечно было бы сгруппировать все банкоматы стоящие по одному адресу в один
        объект обучающей выборки и уйти от проблемы.  Ничто не мешает Вам и сейчас
        поступить подобным образом, после некоторых преобразований на targete.
    9.  Визуализация карт. https://pypi.org/project/folium/
    10. По поводу точности определения адресов.  Я думаю масштаб проблемы несколько
        преувеличен. Если воспользоваться примером кода по ссылке, случайно
        найденным мной в интернете, и дописать к нему еще несколько эвристик, можно
        значительно повысить точность определения адресов.
        https://github.com/aamamaev/machine-learning/tree/master/parsing
    11. По поводу адресов на латинице.  Для банкоматов банков партнёров есть только
        латынь, содержащаяся в транзакционных данных.  Адреса на латыни никто
        специально не обрезал.  Если не хочется восстанавливать адреса, можно
        заняться написанием эффективного парсера или генерацией  оригинальных
        геопризнаков. Номинации в контесте на любой вкус.

## Необходимые компоненты

https://github.com/mozilla/geckodriver/releases
https://sites.google.com/a/chromium.org/chromedriver/downloads

tar xf resource/geckodriver-v0.23.0-linux64.tar.gz -C .venv/bin/


## Банки

- [Банкоматы | Росбанк](https://www.rosbank.ru/ru/dbo/dbo-personal/atms/)

## Python

- [Visualizing named colors — Matplotlib 3.0.2 documentation](https://matplotlib.org/gallery/color/named_colors.html)
- [DinoTools/python-overpy: Python Wrapper to access the Overpass API](https://github.com/DinoTools/python-overpy)
- [ipyleaflet: Interactive maps in the Jupyter notebook — ipyleaflet documentation](https://ipyleaflet.readthedocs.io/en/latest/index.html)
- [mocnik-science/osm-python-tools: A library to access OpenStreetMap related services](https://github.com/mocnik-science/osm-python-tools)

## OverpassQL

- [Overpass API/Overpass QL - OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL)
- [Overpass API/Overpass API by Example - OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_API_by_Example)
- [RU:Overpass API/Language Guide - OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/RU:Overpass_API/Language_Guide)

## OpenStreetMap

- [Tag:amenity=bank - OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dbank)
- [RU:Tag:amenity=atm - OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/RU:Tag:amenity%3Datm)
- [RU:Key:place - OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/RU:Key:place)

## Kaggle

- [House Prices: Advanced Regression Techniques | Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/kernels)
- [New York City Taxi Fare Prediction | Kaggle](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/kernels)

## Links

- [Loading Data from OpenStreetMap with Python and the Overpass API - Parametric Thoughts](https://janakiev.com/blog/openstreetmap-with-python-and-overpass-api/)
