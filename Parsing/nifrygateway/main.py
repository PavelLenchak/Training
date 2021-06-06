# -*- mode: python ; file: main.py ; encoding: utf-8 -*-

"""
    Парсинг сайта https://niftygateway.com/marketplace

    1. edition first - данные по каждому nifty (его принадлежность к художнику (коллекции), niftytype и т.д.)
    2. edition second - данные по каждому nifty (token id, owner id и т.д.)
    3. events - все транзакции по каждому токену
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
import nifty_events
import nifty_second_editions

# Директория файла
MAIN_PATH = pathlib.Path(__file__).parent

# Идентифицирем дебаггер
logging.basicConfig(filename=f'{MAIN_PATH}\logs.csv', level=logging.INFO)

# Файлы для сохранения данных
EDITIONS_F_CSV = f'{MAIN_PATH}\editions_first.csv'

# OPEN_REQ - запрос на сервер для получения информации о художниках и их коллекций (GET запрос)
# QUERY_REQ - запрос для получения информации по каждому nifty (GET запрос)
# EVENTS_REQ - запрос для получения данных по истории событий (POST запрос)
OPEN_REQ = 'https://api.niftygateway.com//exhibition/open/'
QUERY_REQ= 'https://api.niftygateway.com//already_minted_nifties/?searchQuery=%3Fpage%3D3%26search%3D%26onSale%3Dfalse&page=%7B%22current%22:1,%22size%22:20%7D&filters=%7B%7D&sort=%7B%22_score%22:%22desc%22%7D'
EVENTS_REQ = 'https://api.niftygateway.com//market/nifty-history-by-type/'

# Заголовки - для идентификации как живой человек
HEADERS = {
    'user-agent': UserAgent().chrome
}


# Получем данные по запросу 
def get_html(url, params=''):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data=response.json()
        return data
    except:
        print('Loadnig ERROR: {}'.format(response))

# Сохраняем данные в csv формате
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
    print('start FIRST PART')
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
    nifty_events.parse_events()

    end = datetime.now()
    total = end - start
    print('Total time: {}'.format(str(total)))
    logging.info("Program end. Total time - {}".format(total))


if __name__ == '__main__':
    main()