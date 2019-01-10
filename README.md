# Happy Data Year

## Описание

[Happy Data Year](https://boosters.pro/champ_21) - новогодний чемпионат по
анализу данных от Росбанка.

Вам предстоит предсказать индекс популярности геолокации для размещения
устройства банкоматной сети.

В обучающей выборке находятся данные о геопозиции шести тысяч банкоматов
Росбанка и его партнеров, а также целевая переменная — индекс популярности
банкомата. В тестовой выборке еще две с половиной тысячи банкоматов, разделенных
поровну на публичную и приватную часть.

## Подсказки от организоторов

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

## Подготовка

### Виртуальное окружение

    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip install --upgrade -e .[dev]

### Jupyter Notebook

    $ jupyter-notebook

### Редактор

    $ PYTHONPATH=$PYTHONPATH:.venv/lib/python3.6/site-packages/ vim

### Драйвер для `selenium`

Скачать [geckodriver](https://github.com/mozilla/geckodriver/releases)
 или [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).

    $ tar xf ./resource/geckodriver-v0.23.0-linux64.tar.gz -C .venv/bin/
    $ unzip ./resource/chromedriver_linux64.zip -d .venv/bin

## Данные

### Географические объекты

Первое очевидное предположение - популярность места размещения банкомата зависит
от объектов инфраструктуры, находящихся неподалеку.

Из [OpenStreetMap](https://www.openstreetmap.org) с помощью
[API Overpass](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_API_by_Example)
([ru](https://wiki.openstreetmap.org/wiki/RU:Overpass_API/Language_Guide))
выгружаем интересующие объекты (например, [bank](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dbank),
[atm](https://wiki.openstreetmap.org/wiki/RU:Tag:amenity%3Datm), [place](https://wiki.openstreetmap.org/wiki/RU:Key:place)).

    $ ./scripts/10-places.sh

Протестировать запросы можно в [Overpass-Turbo](https://overpass-turbo.eu/).

    // Все большие магазины в выделенной области
    [out:json];
    (
        node[shop=mall]({{bbox}});
        way[shop=mall]({{bbox}});
        relation[shop=mall]({{bbox}});
    );
    out center;

    // Все объекты в радиусе определенной точки
    [out:json];
    (
        node (around:20, 48.118297, 132.475292);
        way (around:20, 48.118297, 132.475292);
    );
    out center;

Хорошая [статья](https://janakiev.com/blog/openstreetmap-with-python-and-overpass-api/), в которой автор объясняет основы работы с OpenStreetMap.

### Reverse geocoding

Адреса банкоматов в их русской трансляции представлены как строки.

    'улица А.О. Емельянова, 34, Южно-Сахалинск, Сахалинская область, Россия'
    'Коммунистический проспект, Южно-Сахалинск, Сахалинская область, Россия'
    'Ленинградский проспект, 76А, Москва, Россия, 125315'
    'деревня Веледниково, городской округ Истра, Московская область, Россия'

Чтобы уточнить адреса и привести их к одному формату, можно попробовать узнать
адреса для каждой отдельной точки с помощью [reverse geocoding](https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=47.88559199&lon=134.961981).
Бонусом идет описание места.

```json5
{
    "8526.0": {
        "place_id": "93735343",
        "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
        "osm_type": "way",
        "osm_id": "83099400",
        "lat": "46.9409981",
        "lon": "142.738146694431",
        "place_rank": "30",
        "category": "shop",
        "type": "supermarket",
        "importance": "0",
        "addresstype": "shop",
        "name": "Островной",
        "display_name": "Островной, 34, улица Емельянова, Большая Елань, Южно-Сахалинск, городской округ Южно-Сахалинск, Сахалинская область, ДФО, 693006, РФ",
        "address": {
            "supermarket": "Островной",
            "house_number": "34",
            "road": "улица Емельянова",
            "suburb": "Большая Елань",
            "city": "Южно-Сахалинск",
            "county": "городской округ Южно-Сахалинск",
            "state": "Сахалинская область",
            "postcode": "693006",
            "country": "РФ",
            "country_code": "ru"
        },
        "boundingbox": [
            "46.9408939",
            "46.9411021",
            "142.7377913",
            "142.7385021"
        ],
        "record_id": 8526.0
    }
}
```

## Банки

- [Банкоматы | Росбанк](https://www.rosbank.ru/ru/dbo/dbo-personal/atms/)

## Python

- [Visualizing named colors — Matplotlib 3.0.2 documentation](https://matplotlib.org/gallery/color/named_colors.html)
- [DinoTools/python-overpy: Python Wrapper to access the Overpass API](https://github.com/DinoTools/python-overpy)
- [ipyleaflet: Interactive maps in the Jupyter notebook — ipyleaflet documentation](https://ipyleaflet.readthedocs.io/en/latest/index.html)
- [mocnik-science/osm-python-tools: A library to access OpenStreetMap related services](https://github.com/mocnik-science/osm-python-tools)

## Kaggle

- [House Prices: Advanced Regression Techniques | Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/kernels)
- [New York City Taxi Fare Prediction | Kaggle](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/kernels)
