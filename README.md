## Описание

[Happy Data Year](https://boosters.pro/champ_21) - новогодний чемпионат по
анализу данных от Росбанка.

## Подготовка

### Виртуальное окружение

    $ python3 -m venv .venv
    $ source .venv/bin/activate
    (.venv) $ pip install --upgrade -e .[dev]

### Jupyter Notebook

    (.venv) $ jupyter-notebook

### Редактор

    (.venv) $ PYTHONPATH=$PYTHONPATH:.venv/lib/python3.6/site-packages/ vim

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

    (.venv) $ ./scripts/10-places.sh

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
адреса для каждой отдельной точки с помощью [reverse geocoding](https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=46.9409981&lon=142.738146694431).
Бонусом идет описание места.

    (.venv) $ ./scripts/20-reverce-addresses.py

Пример полученных данных:

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

### Адреса банкоматов Росбанка и партнеров

На сайте Росбанка есть [список](https://www.rosbank.ru/ru/atms/) банкоматов
самого Росбанка и его партнеров.

![Местоположение банкоматов](docs/figures/rosbank.png?raw=true "Местоположение банкоматов")

Для получения этой информации используем библиотеку `selenium`.

    (.venv) $ ./scripts/30-rosbank-atm.py

Пример полученных данных:

```json5
[
    {
        "region": "Алтайский край",
        "city": "Барнаул",
        "bank": "Росбанк",
        "address_title": "Тракт Павловский 192А",
        "address_type": "Гипермаркет \"Леруа Мерлен\"",
        "working_time": "Пн-Вс:08:00-22:00",
        "currency": "Выдача (₽)\nЧасть операций недоступна",
        "address_metro": "",
        "address_map": "https://www.rosbank.ru/ru/atms/?showonmap=82712",
        "script_text": " ... "
        "long": "83.632452",
        "lat": "53.350284"
    }
]
```

