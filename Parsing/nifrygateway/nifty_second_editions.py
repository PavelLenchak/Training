# -*- mode: python ; file: nifty_second_editions.py ; encoding: utf-8 -*-

'''
    Парсинг сайта niftygateway.com
    Данные выгружаются по запросу QUERY_REQ (request.get)
    Используется метод asyncio
'''

import pathlib, sys
import random
import asyncio
import logging
import csv
import requests
from fake_useragent import UserAgent

import aiofiles
import aiohttp
from aiohttp import ClientSession

# Количество параллельных запросов за единицу времени
LIMIT = 5

HEADERS = {
    'user-agent': UserAgent().chrome
}

MAIN_PATH = pathlib.Path(__file__).parent

QUERY_REQ= 'https://api.niftygateway.com//already_minted_nifties/?searchQuery=%3Fpage%3D3%26search%3D%26onSale%3Dfalse&page=%7B%22current%22:1,%22size%22:20%7D&filters=%7B%7D&sort=%7B%22_score%22:%22desc%22%7D'
CSV_FILE = f'{MAIN_PATH}\editions_second.csv'

logging.basicConfig(filename=f'{MAIN_PATH}\logs.csv', level=logging.INFO)


async def fetch_html(url, session: ClientSession, **kwargs):
    resp = await session.request(method='GET', url=url, headers=HEADERS, **kwargs)
    
    resp.raise_for_status()
    logging.info(f'Get response {resp.status} for URL: {url}')
    html = await resp.json()
    return html


async def parse(url, session: ClientSession, **kwargs):
    items = []
    try:
        # await asyncio.sleep(random.randint(0, 10))
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
    ) as e:
        print('{} {}'.format(e, url[url.find(':',url.find('current')):url.find(',%22size')]))
        logging.error(f'aiohttp exeption for {url} {e}')
    except Exception as ex:
        logging.exception(
            f'Неизвестная ошибка парсинга {ex}'
        )
        return items
    else:
        for item in html['data']['results']:
            # Если нужно получить число между # и / в item['name'] - есть не во всех названиях
            ed_number = item['name'][item['name'].find('#'):item['name'].find('/')]
            items.append(
                {
                    'Collection name': item['project_name'],
                    'Contract Address': item['contract_address'],
                    'Edition number': item['name'],
                    'Token id': item['token_id_or_nifty_type'],
                    'Owner_id': item['owner_profile_id'],
                }
            )
        return items


async def write_one(url, file, sem, **kwargs):
    # print(f'Parse {url}')
    async with sem:
        datas = await parse(url=url, **kwargs)
    # logging.info(datas)
    if not datas:
        return None
    titels = list(datas[0].keys())
    async with aiofiles.open(file, 'a', newline='', encoding='utf-16') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in datas:
            task = [item[titels[i]] for i in range(len(titels))]
            await writer.writerow(task)
        print('Записан результат для {}'.format(url[url.find(':',url.find('current')):url.find(',%22size')]))
        # logging.info(f'Записан результат для {url}')


async def parse_and_write(urls, **kwargs):
    # Количество одновременных запросов
    sem = asyncio.Semaphore(LIMIT)
    async with ClientSession() as session:
        tasks = []
        # Формируем задания для 
        for url in urls:
            tasks.append(
                write_one(url=url, file= CSV_FILE, session=session, sem=sem, **kwargs)
            )
        await asyncio.gather(*tasks)


def _get_html(url, params=''):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data=response.json()
        return data
    except:
        print('Loadnig ERROR: {}'.format(response))

# Для определения общего колиичеста страниц
def _get_total_pages():
    iquery= _get_html(QUERY_REQ, params={'current':1})
    total_pages = iquery['data']['meta']['total_pages']
    return total_pages


def parse_second_part():
    print('Start SECOND part')
    urls = []
    tp = _get_total_pages()
    print("Total pages {}".format(tp))
    logging.info("Total pages {}".format(tp))

    for i in range(1, tp+1):
        urls.append(
            f'https://api.niftygateway.com// \
            already_minted_nifties/?searchQuery=%3F \
            page%3D3%26search%3D%26onSale%3Dfalse&page=%7B%22current%22:{i}, \
            %22size%22:20%7D&filters=%7B%7D&sort=%7B%22_score%22:%22desc%22%7D'
        )
    asyncio.run(parse_and_write(urls=urls))


if __name__ == '__main__':
    parse_second_part()

