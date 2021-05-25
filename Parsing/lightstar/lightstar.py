# -*- coding: utf-8 -*-

from asyncio.tasks import sleep
import os, sys, time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
import aiofiles, asyncio, httpx

global datas
datas = []

CSV_FILE = 'Parsing\\lightstar\\lightstar.csv'
URL = 'https://lightstar.ru/kupit-lustry-svetilniki-optom/'

HEADERS = {
    'user-agent': UserAgent().chrome
}
    

async def get_html(url, params=''):
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=HEADERS, params=params)
        if r.status_code == 200:
            return r
        else:
            asyncio.sleep(5)
            await get_html(url, headers=HEADERS, params=params) 

async def save_to_csv(items):
    titels = list(items[0].keys())
    async with aiofiles.open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for item in items:
            task = [str(item[titels[i]]) for i in range(len(titels))]
            await writer.writerow(task)
    print(f'Save done')


async def get_content(host, current_page):
    async with httpx.AsyncClient() as client:
        r = await client.get(host, headers=HEADERS, params={'page': current_page})
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            articles = soup.find_all('article', class_='card-product')
            to_save = []
            for arti in articles:
                header = arti.find_all('span', class_='card-product__sub-title')
                # specification = arti.find_all('dd', class_='specification__definition')
                # try:
                #     ip = specification[1].get_text()
                # except:
                #     ip = 'None'
                to_save.append({
                    'Name': header[0].get_text(),
                    'ID': header[1].get_text().replace(u'\xa0', u' '),
                    'Main Data': arti.find('dl', class_='specification specification--small').get_text(),#specification[0].get_text(),
                    #'IP': ip,
                    'URL': arti.find('a', class_='card-product__link').get('href'),
                })
                await save_to_csv(to_save)
                to_save = []
            print(f'Get_content {current_page}')
        else:
            print(r.status_code, host, current_page)
    
    #print(f'{host} - {current_page}')
        

# 10 pages per minute without asyncio
# 10 pages per 20 seconds with asyncio
async def main():
    html = requests.get(URL, headers=HEADERS)
    # html = await get_html(URL)
    soup = BeautifulSoup(html.text, 'html.parser')
    links = soup.find('ul', class_='pagination__list').find_all('a', class_='pagination__link')
    
    pages = []
    for link in links:
        pages.append({
            'url': link.get('href')
        })
    host = pages[-1]['url']
    max_pages = int(pages[-1]['url'].split('/')[-1].replace('?page=',''))

    queue = asyncio.Queue()
    tasks_list = []

    current_page = 0
    value = max_pages
    while current_page < value:
        current_page += 1
        task = asyncio.create_task(get_content(host, current_page))
        tasks_list.append(task)
        #await get_content(host, current_page)

    await queue.join()
    await asyncio.gather(*tasks_list, return_exceptions=True)
    
    print(len(datas))

    # save_to_csv(datas)
    # loop = asyncio.get_running_loop()
    # await loop.run_in_executor(None, save_to_csv, datas) 

    
if __name__ == '__main__':
    start = datetime.now()
    print(f'Start time: {start}')

    asyncio.run(main())

    end = datetime.now()
    print(f'Total time: {end-start}')
