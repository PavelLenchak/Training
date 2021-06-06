# -*- coding: utf-8 -*-
# niftygateway.py

"""
    Парсинг сайта https://niftygateway.com/marketplace
    Используются библиотеки requests, bs4, csv
    Собираем информацию через запросы requests.get ... requests.post
"""

import os, sys
import pathlib
from pathlib import Path
from time import sleep
from datetime import datetime
import requests
import csv
from fake_useragent import UserAgent
from multiprocessing import Pool
from multiprocessing import cpu_count
import logging
import random
from . import nifty_second_editions
from . import nifty_events

logging.basicConfig(filename='Parsing\\nifrygateway\\logs.csv', level=logging.INFO)

# Файлы для сохранения данных
EDITIONS_F_CSV = 'Parsing\\nifrygateway\\editions_first.csv'
EDITIONS_S_CSV = 'Parsing\\nifrygateway\\editions_second.csv'
EVENTS_CSV = 'Parsing\\nifrygateway\\events.csv'

# OPEN_REQ - запрос на сервер для получения информации о художниках и их коллекций (GET запрос)
# QUERY_REQ - запрос для получения информации по каждому nifty (GET запрос)
# EVENTS_REQ - запрос для получения данных по истории событий (POST запрос)
OPEN_REQ = 'https://api.niftygateway.com//exhibition/open/'
QUERY_REQ= 'https://api.niftygateway.com//already_minted_nifties/?searchQuery=%3Fpage%3D3%26search%3D%26onSale%3Dfalse&page=%7B%22current%22:1,%22size%22:20%7D&filters=%7B%7D&sort=%7B%22_score%22:%22desc%22%7D'
EVENTS_REQ = 'https://api.niftygateway.com//market/nifty-history-by-type/'

test = 'https://niftygateway.com/itemdetail/secondary/0x68c4dd3f302c449be39af528d56c6bd242b8cedb/23600030038'

# Заголовки - для идентификации как живой человек
HEADERS = {
    'user-agent': UserAgent().chrome
}

PROXIES = [
    '91.193.253.188:23500',
    '176.9.119.170:3128',
    '176.9.75.42:3128',
    '88.198.24.108:8080',
    '95.141.193.35:80',
    '176.9.75.42:8080',
    '95.141.193.14:80',
    '5.252.161.48:8080',
    '176.9.119.170:3128',
]

# Получем данные по запросу 
def get_html(url, params=''):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data=response.json()
        return data
    except:
        print('Loadnig ERROR: {}'.format(response))


def save_csv(items, path, titels, encoding='utf-8'):
    with open(path, 'a', newline='', encoding=encoding) as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        #writer.writerow(titels)
        #print(titels)
        for item in items:
            task = [item[titels[i]] for i in range(len(titels))]
            writer.writerow(task)


def get_first_edition(items):
    niftys = []
    for item in items:
        for nifty in item['nifties']:
            niftys.append(
                {
                    'Artist': item['userProfile']['name'],
                    'Collection Name': item['storeName'],
                    'Collection Type': item['template'],
                    'Edition Name': nifty['niftyTitle'],
                    'Edition Type': nifty['niftyDisplayImage'].split('.')[-1],
                    'Nifty Type': nifty['niftyType'],
                    'Edition Total Size': nifty['niftyTotalNumOfEditions'],
                    'Contract Address': nifty['niftyContractAddress'],
                }
            )
    #проверяем данные
    # for nift in niftys:
    #     print(nift, sep='\n')
    # for item in items[0]['nifties']:
    #     print(item['niftyTitle'])
    return niftys


def edition_first():
    print('start EDITION FIRST')
    datas = []
    items = get_html(OPEN_REQ)
    datas.extend(get_first_edition(items))
    titels = list(datas[0].keys())
    save_csv(datas, EDITIONS_F_CSV, titels, encoding='utf-16')
    

def main():
    start = datetime.now()
    logging.info(f"Program started at {start}")

    # Парсим данные по каждому artist
    edition_first()
    
    # Парсим вторые данные (по каждому nifty)
    nifty_second_editions.parse_second_part()

    # Парсим мероприятия по каждому nifty
    nifty_events.main()

    end = datetime.now()
    total = end - start
    print('Total time: {}'.format(str(total)))
    logging.info("Program end. Total time - {}".format(total))


if __name__ == '__main__':
    main()