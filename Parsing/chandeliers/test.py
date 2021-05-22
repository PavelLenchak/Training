import sys
import re
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
from datetime import datetime
import codecs, io

# Фото Свойтво товаров Документы
# <img src="http://www.thornlighting.ru/img/31/tlg_thumb_downlights/@@images/c47c664c-1c6f-4b2e-9622-51c23accdef6.jpeg" alt="Светильники типа downlight" title="" height="176" width="176">


HOST = 'http://www.thornlighting.ru'
URL = 'http://www.thornlighting.ru/ru-ru/produkty/vnutriennieie-osvieshchieniie'

CSV_FILE = 'Parsing\\chandeliers\\test.csv'

HEADERS = {
    'user-agent': UserAgent().chrome
}

def save_csv(items, path):
    print(f'Start saving process')
    titels = list(items[0].keys())
    with io.open(path, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in items:
            task = [str(item[titels[i]]).replace('.', ',') for i in range(len(titels))]
            writer.writerow(task)
            print(f'Saving {task[0]}')
    print('Saving process have done')


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_html(url, params=''):
    req = requests.get(url, params=params)
    return req

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='pbf width-1:4')

    # получаем ссылки ВНУТРЕННЕЕ ОСВЕЩЕНИЕ
    project_urls = []
    for item in items:
        project_urls.append(item.find('a', class_='discreet').get('href'))

    all_datas = []
    for p_u in project_urls:
        html = get_html(p_u).text
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='pbf width-1:4')

        products = []
        for item in items:
            products.append(item.find('a', class_='discreet').get('href'))
        
        datas = []
        for pr in products:
            html = get_html(pr).text
            soup = BeautifulSoup(html, 'html.parser')
            all_tr_even = soup.find_all('tr', class_='even')
            all_tr_odds = soup.find_all('tr', class_='odd')

            
            for tr_even in all_tr_even:
                all_td = tr_even.find_all('td')
                serial = tr_even.find('a', class_='article_link').get_text()
                print(f'Парсим {serial}')
                datas.append({
                    'Серия': serial,
                    'Мощность W': clean_html(str(all_td[1])),
                    'Световой поток': clean_html(str(all_td[2])),
                    'Type': clean_html(str(all_td[6])),
                    'Вес': tr_even.find('td', class_='weight').get_text(),
                    'SAP CODE': clean_html(str(all_td[9])),
                    'URL': tr_even.find('a', class_='article_link').get('href'),
                })

            for tr_odd in all_tr_odds:
                all_td = tr_odd.find_all('td')
                serial = tr_odd.find('a', class_='article_link').get_text()
                print(f'Парсим {serial}')
                datas.append({
                    'Серия': serial,
                    'Мощность W': clean_html(str(all_td[1])),
                    'Световой поток': clean_html(str(all_td[2])),
                    'Type': clean_html(str(all_td[6])),
                    'Вес': tr_odd.find('td', class_='weight').get_text(),
                    'SAP CODE': clean_html(str(all_td[9])),
                    'URL': tr_odd.find('a', class_='article_link').get('href'),
                })
        
        all_datas.append(datas)
    
    for data in all_datas:
        save_csv(data, CSV_FILE)


def do_all(url):
    html = get_html(url)
    get_content(html.text)

def main():
    start = datetime.now()
    main_url = [
        'http://www.thornlighting.ru/ru-ru/produkty/vnutriennieie-osvieshchieniie',
        'http://www.thornlighting.ru/ru-ru/produkty/naruzhnoie-osvieshchieniie',
        'http://www.thornlighting.ru/ru-ru/produkty/sistiemy-upravlieniia-osvieshchieniiem-i-avariinoie-osvieshchieniie'
    ]

    # for url in main_url:
    #     do_all(url)
    with Pool(40) as p:
        p.map(do_all, main_url)

    end = datetime.now()
    print(f'Parsing have done {end-start}')
    
if __name__ == '__main__':
    main()