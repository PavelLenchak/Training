import sys
import re
import logging
from datetime import datetime
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import csv

# Фото Свойтво товаров Документы
# <img src="http://www.thornlighting.ru/img/31/tlg_thumb_downlights/@@images/c47c664c-1c6f-4b2e-9622-51c23accdef6.jpeg" alt="Светильники типа downlight" title="" height="176" width="176">

HOST = 'http://www.thornlighting.ru'
URL = 'http://www.thornlighting.ru/ru-ru/produkty/vnutriennieie-osvieshchieniie'
CSV_FILE = 'Parsing\\chandeliers\\products.csv'

logging.basicConfig(filename='Parsing\\chandeliers\\logs.csv', level=logging.INFO)

HEADERS = {
    'user-agent': UserAgent().chrome
}

def save_csv(items, path):
    titels = list(items[0].keys())
    with open(path, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in items:
            task = [str(item[titels[i]]).replace('.', ',') for i in range(len(titels))]
            writer.writerow(task)

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_html(url, params=''):
    req = requests.get(url, params=params)
    return req

def get_():
    pass

def get_():
    pass

def get_mod_content():
    pass

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='discreet')
    main_chapter = soup.find('h1', class_='documentFirstHeading').get_text()

    # получаем ссылки ВНУТРЕННЕЕ ОСВЕЩЕНИЕ
    project_urls = []
    for item in items:
        project_urls.append({
            'sub_chapter_name': item.get_text(),
            'url': item.get('href')
            })

    # Кликаем на каждую категорию 1/8
    for p_u in project_urls:
        sub_chapter = p_u['sub_chapter_name']
        html = get_html(p_u['url']).text
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('a', class_='discreet')

        # Определяем каждый продукт внутри категории 
        products = []
        for item in items:
            products.append({
                'name': item.get_text(),
                'url': item.get('href'),
                })
        
        datas = []
        # Кликаем на каждый товар
        for pr in products:
            serial_name = pr['name']
            html = get_html(pr['url']).text
            soup = BeautifulSoup(html, 'html.parser')
            all_tr_even = soup.find_all('tr', class_='even')
            all_tr_odds = soup.find_all('tr', class_='odd')

            serial_description = soup.find('div', class_='row rowSpacer').get_text()
            
            all_mod_urls = []
            for tr_even in all_tr_even:
                all_mod_urls.append(tr_even.find('a', class_='article_link').get('href'))
            for tr_odd in all_tr_odds:
                all_mod_urls.append(tr_odd.find('a', class_='article_link').get('href'))

            #<div class="wrapper" style="display: block;"><p>Встраиваемый светодиодный светильник.
            for url in all_mod_urls:
                html = get_html(url).text
                soup = BeautifulSoup(html, 'html.parser')

                sap_code = soup.find('div', id='article-detail').find('span').get_text()
                modification = soup.find('span', id='breadcrumbs-current').get_text()
                version = soup.find('span', id='breadcrumbs-5').find('a').get_text()
                p = list(soup.find('div', class_='wrapper').find('p'))
                # for i in p:
                #     print(i)

                logging.info('Парсим {} в категории {}'.format(tr_even.find('a', class_='article_link').get_text(), pr))
                datas.append({
                    'Раздел 1': main_chapter,
                    'Раздел 2': sub_chapter,
                    'Серия': serial_name,
                    'Описание серии': serial_description,
                    'Версия': version,
                    'Модификация': modification,
                    'SAP CODE': sap_code,
                    'Общие данные': p[0],
                    'Размеры': p[3][p[3].find(':')+2:],
                    'Номинальная мощность': p[5][p[5].find(':')+2:],
                    'Световой поток светильника': p[7][p[7].find(':')+2:],
                    'КПД светильника': p[9][p[9].find(':')+2:],
                    'Вес': p[11][p[11].find(':')+2:],
                })

            # Узнаём url каждой модификации
            # for tr_even in all_tr_even:
            #     logging.info('Парсим {} в категории {}'.format(tr_even.find('a', class_='article_link').get_text(), pr))
            #     all_td = tr_even.find_all('td')
            #     datas.append({
            #         'Раздел 1': '',
            #         'Раздел 2': chapter_name,
            #         'Серия': serial_name,
            #         'Описание': tr_even.find('a', class_='article_link').get_text(),
            #         'Мощность W': clean_html(str(all_td[1])),
            #         'Световой поток': clean_html(str(all_td[2])),
            #         'Type': clean_html(str(all_td[6])),
            #         'Вес': tr_even.find('td', class_='weight').get_text(),
            #         'SAP CODE': clean_html(str(all_td[9])),
            #     })

            # for tr_odd in all_tr_odds:
            #     logging.info('Парсим {} в категории {}'.format(tr_odd.find('a', class_='article_link').get_text(), pr))
            #     all_td = tr_odd.find_all('td')
            #     datas.append({
            #         'Раздел 1': '',
            #         'Раздел 2': chapter_name,
            #         'Серия': serial_name,
            #         'Описание': tr_odd.find('a', class_='article_link').get_text(),
            #         'Мощность W': clean_html(str(all_td[1])),
            #         'Световой поток': clean_html(str(all_td[2])),
            #         'Type': clean_html(str(all_td[6])),
            #         'Вес': tr_odd.find('td', class_='weight').get_text(),
            #         'SAP CODE': clean_html(str(all_td[9])),
            #     })
        
        print(datas[0])
        save_csv(datas, CSV_FILE)


def main():
    start = datetime.now()
    html = get_html(URL)
    get_content(html.text)
    end = datetime.now()
    print(end - start)

if __name__ == '__main__':
    main()