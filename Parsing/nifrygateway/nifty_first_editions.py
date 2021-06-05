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


def get_events(adress_and_type):
    proxy = random.choice(PROXIES)
    main_data = []
    adress = adress_and_type[0]
    nifty_type = adress_and_type[1]

    response = requests.post(EVENTS_REQ, proxies={'http': 'http://' + proxy}, data={
        "contractAddress": adress,
        "niftyType": nifty_type,
        "current":1,
        "size":10,
        "onlySales":"false",
    })
    data = response.json()

    # try:
    total_pages = data['data']['meta']['page']['total_pages'] + 1
    print('Парсим {} {}. Всего страниц - {}'.format(adress, nifty_type, total_pages))
    for page in range(1, total_pages):
        response = requests.post(EVENTS_REQ, data={
            "contractAddress":adress,
            "niftyType":nifty_type,
            "current":page,
            "size":10,
            "onlySales":"false"})
        data = response.json()

        try:
            data_results = data['data']['results']
        except Exception as e:
            print(data['detail'][-10])
            t = data['detail'][-10]
            print(f'Засыпаем на {t} секунд')
            sleep(t)
            get_events([adress, nifty_type])
            # print(f'Dont find data results {data} {adress} {nifty_type} {page}')
            # logging.info(f'ERROR Dont find data results {data} {adress} {nifty_type} {page}')
        else:
            for d in data_results:
                #print(d, sep='\n')
                action = d['Type']
                id = d['id']
                time = ''
                # user1 = ''
                # user2 = ''
                user1_id = ''
                user2_id = ''
                price = ''

                types = {
                    'listing': 'put',
                    'birth': 'has been deposited into Nifty Gateway by',
                    'offer': 'made a global offer for',
                    'withdrawal': 'withdrew',
                    'nifty_transfer': 'sent',
                    'sale': 'bought',
                    'bid': 'put on sale',
                }

                #2013-07-12T07:00:00Z datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
                r_time = d['Timestamp'].replace('T', ' ').replace('Z', '')
                time = datetime.strptime(r_time, '%Y-%m-%d %H:%M:%S.%f')
                
                if action == 'offer':
                    #user1 = d['ListingUserProfile']['name']
                    #user2 = 'None'
                    user1_id = d['ListingUserProfile']['id']
                    price = d['OfferAmountInCents'] * 0.01
                elif action == 'listing':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    #user1 = d['ListingUserProfile']['name']
                    #user2 = 'None'
                    user1_id = d['ListingUserProfile']['id']
                    price = d['ListingAmountInCents'] * 0.01
                elif action == 'birth':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    #user1 = d['BirthingUserProfile']['name']
                    #user2 = 'None'
                    user1_id = d['BirthingUserProfile']['id']
                elif action == 'withdrawal':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    #user1 = d['WithdrawingUserProfile']['name']
                    #user2 = 'None'
                    user1_id = d['WithdrawingUserProfile']['id']
                elif action == 'nifty_transfer':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    #user1 = d['SendingUserProfile']['name']
                    #user2 = d['ReceivingUserProfile']['name']
                    user1_id = d['SendingUserProfile']['id']
                    user2_id = d['ReceivingUserProfile']['id']
                elif action == 'sale':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    #user1 = d['SellingUserProfile']['name']
                    #user2 = d['PurchasingUserProfile']['name']
                    user1_id = d['SellingUserProfile']['id']
                    user2_id = d['PurchasingUserProfile']['id']
                    price = d['SaleAmountInCents'] * 0.01
                elif action == 'bid':
                    #user1 = d['BiddingUserProfile']['name']
                    #user2 = 'None'
                    user1_id = d['BiddingUserProfile']['id']
                    price = d['BidAmountInCents'] * 0.01
                else:
                    print(f'New action: {action}')
                    #print(d['BiddingUserProfile'])
                    #print(d['NiftyObject'])
                    id = 'None'
                    token_id = 'NEW ACTION' + action + adress + nifty_type
                    #user1 = 'None'
                    #user2 = 'None'
                    user1_id = 'None'
                    user2_id = 'None'
                    price = 'None'
                    logging.info('NEW ACTION {} - {} {}'.format(action, adress, nifty_type))


                main_data.append({
                    'ID': id,
                    'Token ID': token_id,
                    'DateTime': time,
                    # 'User 1': user1,
                    # 'User 2': user2,
                    'User 1 ID': user1_id,
                    'User 2 ID': user2_id,
                    'Action': types[action],
                    'Price': str(price)
                })
                titels = list(main_data[0].keys())

    save_csv(main_data, EVENTS_CSV, titels)
        
        # for i in main_data:
        #     print(i)

        # for key, value in data['data']['results'][0].items():
        #     print(f'{key}: {value}')


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

    # Парсим информацию по историям покупок - продаж
    # items = get_html(OPEN_REQ)
    # adress_and_type = get_first_edition(items)
    # adress_and_type_to_parsing = []
    # for item in adress_and_type:
    #     adress_and_type_to_parsing.append([item['Contract Address'], item['Nifty Type']])
    
    # with Pool(cpu_count()) as p:
    #     p.map(get_events, adress_and_type_to_parsing)

    end = datetime.now()
    total = end - start
    print('Total time: {}'.format(str(total)))
    logging.info("Program end. Total time - {}".format(total))


if __name__ == '__main__':
    main()