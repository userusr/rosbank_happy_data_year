#!/bin/bash

cd "$(dirname "$0")"
source 00-functions.sh

# По не понятной причине, API не выдает результаты для node и way
# одновременно. Хотя в WEB интерфейсе https://overpass-turbo.eu/
# подобный запрос работает.
# [out:json];
# (
#     node[shop=mall]({{bbox}});
#     way[shop=mall]({{bbox}});
#     relation[shop=mall]({{bbox}});
# );
# out center;

# Крупные торговые центры, супермаркеты и магазины алкоголя
for i in mall supermarket department_store alcohol; do
    query="
        [out:json];
        area['ISO3166-1'=RU][admin_level=2];
        (
            node[shop=$i](area);
        );
        out center;"
    get_overpass ../workspace/osm_node_$i.json "$query"

    query="
        [out:json];
        area['ISO3166-1'=RU][admin_level=2];
        (
            way[shop=$i](area);
            relation[shop=$i](area);
        );
        out center;"
    get_overpass ../workspace/osm_way_$i.json "$query"
done;

# Офисы банков, банкоматы, почтовые отделения, университеты и
# участки полиции
for i in bank atm post_office university police; do
    query="
        [out:json];
        area['ISO3166-1'=RU][admin_level=2];
        (
            node[amenity=$i](area);
        );
        out center;"
    get_overpass ../workspace/osm_node_$i.json "$query"

    query="
        [out:json];
        area['ISO3166-1'=RU][admin_level=2];
        (
            way[amenity=$i](area);
            relation[amenity=$i](area);
        );
        out center;"
    get_overpass ../workspace/osm_way_$i.json "$query"
done;

# Города
for i in city town; do
    query="
        [out:json];
        area['ISO3166-1'=RU][admin_level=2];
        (
            node[place=$i](area);
        );
        out center;"
    get_overpass ../workspace/osm_node_$i.json "$query"
done;

# Станции метро
name=station
query="
    [out:json];
    area['ISO3166-1'=RU][admin_level=2];
        ( node[railway=station][station=subway](area););
    out center;"
get_overpass ../workspace/osm_node_$name.json "$query"

query="
    [out:json];
    area['ISO3166-1'=RU][admin_level=2];
    (
        way[railway=station][station=subway](area);
        relation[railway=station][station=subway](area);
    );
    out center;"
get_overpass ../workspace/osm_way_$name.json "$query"

# Другие железнодорожные станции
name=railway_station
query="
    [out:json];
    area['ISO3166-1'=RU][admin_level=2];
    ( node[railway=station][station!=subway](area););
    out center;"
get_overpass ../workspace/osm_node_$name.json "$query"

query="
    [out:json];
    area['ISO3166-1'=RU][admin_level=2];
    (
        way[railway=station][station!=subway](area);
        relation[railway=station][station!=subway](area);
    );
    out center;"
get_overpass ../workspace/osm_way_$name.json "$query"

# Аэропорты
name=aeroway_terminal
query="
    [out:json];
    area['ISO3166-1'=RU][admin_level=2];
    ( node[aeroway=terminal](area););
    out center;"
get_overpass ../workspace/osm_node_$name.json "$query"

query="
    [out:json];
    area['ISO3166-1'=RU][admin_level=2];
    (
        way[aeroway=terminal](area);
        relation[aeroway=terminal](area);
    );
    out center;"
get_overpass ../workspace/osm_way_$name.json "$query"
