# -*- coding: utf-8 -*-
"""Получаем адреса по координатам."""
import json
import logging
import math
import os
from pathlib import Path
from random import randint
from time import sleep

import pandas as pd
from tqdm import tqdm

import requests


def dump_json(file_name, data):
    """Записываем структуру данных data на диск в формате JSON."""
    with open(file_name, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        os.fsync(f.fileno())
        f.flush()


def main():
    """Получаем адреса по координатам."""
    url = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2'
    reverce_address_file = '../workspace/reverce_addresses.json'
    result = dict()
    (skipped, seen, fethed) = (0, 0, 0)

    train = pd.read_csv('../data/train.csv', index_col=0)
    test = pd.read_csv('../data/test.csv', index_col=0)

    train['isTrain'] = True
    test['isTrain'] = False

    X = train.append(test, sort=False)

    if Path(reverce_address_file).is_file():
        with open(reverce_address_file) as f:
            result = json.load(f)

    for index, row in tqdm(X.iterrows()):
        if (row['lat'] is None or row['long'] is None or math.isnan(row['lat']) or math.isnan(row['long'])):
            skipped = skipped + 1
        elif str(row['id']) in result:
            seen = seen + 1
        else:
            r = requests.get(url, params={'lat': row['lat'], 'lon': row['long']})
            result[row['id']] = r.json()
            result[row['id']]['record_id'] = row['id']
            fethed = fethed + 1
            sleep(randint(1, 2))
            if index % 10 == 0:
                dump_json(reverce_address_file, result)

    dump_json(reverce_address_file, result)
    print("skipped: {}; seen: {}; fetched: {};".format(skipped, seen, fethed))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
