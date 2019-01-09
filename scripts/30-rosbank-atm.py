# -*- coding: utf-8 -*-
"""Адреса банкоматов Росбанка и партнеров.

На сайте Росбанка есть список банкоматов включая партнеров.
Наиболее ценная информация, содержащаяся в этом списке - доступные операции и
режим работы каждого банкомата. Также по ссылке "показать на карте"
можно вытащить координаты.
"""
import json
import logging
import os
import re
from random import randint
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm


def dump_json(file_name, data):
    """Записываем структуру данных data на диск в формате JSON."""
    with open(file_name, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        os.fsync(f.fileno())
        f.flush()


def get_regions(driver: webdriver):
    """Получаем список регионов.

    :param driver: selenium.webdriver
    :returns: [{'region_id': str, 'region_name': str}]

    """
    regions = list()
    driver.get("https://www.rosbank.ru/ru/system/regions.php")
    for elem in driver.find_elements_by_xpath("//a[@href]"):
        href = elem.get_attribute("href")
        region_name = elem.text
        if 'region=' in href:
            region_id = re.sub(r'^.*region=(\d+)$', r'\1', href)
            regions.append({'region_id': region_id, 'region_name': region_name})
    return regions


def get_atms(driver: webdriver, city_name: str, region_name: str):
    """Проходим по всем страницам, и получаем список банкоматов.

    :driver: selenium.webdriver
    :returns: [{ ... }]

    """
    pages = 0
    rows = list()
    has_next_page = True

    while has_next_page:
        pages = pages + 1
        for row in driver.find_elements_by_class_name('page-atm__table_row'):
            rows.append({
                'region': region_name,
                'city': city_name,
                'bank': row.find_element_by_class_name('address-logo').text,
                'address_title': row.find_element_by_class_name('address-title').text,
                'address_type': row.find_element_by_class_name('address-type').text,
                'working_time': row.find_element_by_class_name('page-atm__table_col--time').text,
                'currency': row.find_element_by_class_name('page-atm__table_col--currency').text,
                'address_metro': row.find_element_by_class_name('address-metro').text,
                'address_map': (
                    row
                    .find_element_by_class_name('address-map')
                    .find_element_by_link_text('Показать на карте')
                    .get_attribute("href")
                )
            })

        try:
            sleep(randint(1, 3))
            driver.find_element_by_class_name('pagination-arrow--next').click()
        except NoSuchElementException:
            has_next_page = False

    logging.info('{}: {} (pages: {}; atms: {})'.format(region_name, city_name, pages, len(rows)))
    return rows


def main(driver):
    """Получаем адреса с сайта https://www.rosbank.ru/ru/.

    На сайте Росбанка можно увидеть список всех банкоматов, часы их работы и
    возможные операции. Чтобы получить эту информацию будем последовательно
    перебирать все города и регионы.
    """
    rows = list()
    re_long = re.compile(r'var\slong=([\d\.]+);')
    re_lati = re.compile(r'var\slati=([\d\.]+);')
    base_url = 'https://www.rosbank.ru/ru/'
    region_page_tpl = base_url + 'atms/list.php?region={}'
    city_page_tpl = (
        base_url +
        'atms/list.php?p_f_2_11={}&metrocity=-1&p_f_2_22=0&street=&p_f_2_temp_id=459&p_f_2_all=1'
    )

    regions = get_regions(driver)
    for i, region in enumerate(regions):
        region_page = region_page_tpl.format(region['region_id'])
        logging.info('{} ({})'.format(region['region_name'], region['region_id']))
        driver.get(region_page)

        cities = list()
        city_drop_down = driver.find_element_by_class_name('dropdown-box__inner')
        for city in city_drop_down.find_elements_by_xpath(".//a[@data-value]"):
            cities.append({
                'city_name': city.get_attribute('data-value'),
                'city_href': city_page_tpl.format(city.get_attribute('data-value'))
            })

        for city in cities:
            driver.get(city['city_href'])
            city_atms = get_atms(driver, city['city_name'], region['region_name'])

            for atm in city_atms:
                address_map = atm.get('address_map')
                if address_map is None:
                    continue

                driver.get(address_map)
                script_tag = driver.find_element_by_xpath("//div[@class='container']//script[@type='text/javascript']")

                script_text = re.sub(r'\s+', ' ', script_tag.get_attribute('innerHTML'))
                atm['script_text'] = script_text
                atm['long'] = ''
                atm['lat'] = ''

                search_long = re_long.search(script_text)
                search_lati = re_lati.search(script_text)
                if search_long is not None:
                    atm['long'] = search_long.group(1)
                if search_lati is not None:
                    atm['lat'] = search_lati.group(1)

            rows.extend(city_atms)
            dump_json('../workspace/rosbank_atm.json', rows)
            sleep(randint(1, 10))

    dump_json('../workspace/rosbank_atm.json', rows)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    main(driver)
