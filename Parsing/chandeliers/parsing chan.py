import sys, os
import re
import logging
from datetime import datetime
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
import codecs
import functools

# Фото Свойтво товаров Документы
# <img src="http://www.thornlighting.ru/img/31/tlg_thumb_downlights/@@images/c47c664c-1c6f-4b2e-9622-51c23accdef6.jpeg" alt="Светильники типа downlight" title="" height="176" width="176">
# <a target="_blank" rel="nofollow" href="http://www.thornlighting.ru//object/PDF/datasheet.aspx?Lang=RU&amp;iso2=RU&amp;ArticleID=298763&amp;template=lvk_tl&amp;CompanyID=7&amp;tiltAngle=0&amp;DatasheetType=3&amp;ModeID=21&amp;ext=.pdf">Комбинированный список параметров (.pdf)</a>
HOST = 'http://www.thornlighting.ru'
URL = 'http://www.thornlighting.ru/ru-ru/produkty/vnutriennieie-osvieshchieniie'
CSV_FILE = 'Parsing\\chandeliers\\products.csv'

DOCS_PATH = 'Parsing\\chandeliers\\docs'
DOCS_FILE = 'Parsing\\chandeliers\\docs.csv'

logging.basicConfig(filename='Parsing\\chandeliers\\logs.csv', level=logging.INFO)

HEADERS = {
    'user-agent': UserAgent().chrome
}

def save_csv(items, path):
    titels = list(items[0].keys())
    # try:
    #     with open(path, 'a', newline='') as csv_file:
    #         writer = csv.writer(csv_file, delimiter=';')
    #         for item in items:
    #             task = [str(item[titels[i]]).replace('.', ',') for i in range(len(titels))]
    #             writer.writerow(task)
    # except:
    #     print('Изменение кодировки {}'.format(items[0]['Модификация']))
    with codecs.open(path, 'a', encoding='utf-32') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in items:
            task = [str(item[titels[i]]).replace('.', ',') for i in range(len(titels))]
            writer.writerow(task)
    logging.info('Парсим {} {} в категориях {} {}'.format(items[0]['Модификация'], items[0]['Серия'], items[0]['Раздел 2'], items[0]['Раздел 1']))

def save_docs(url, file_name, file_type, sap_code):
    path = f'{DOCS_PATH}\{sap_code}'
    if not os.path.exists(path):
        os.mkdir(path)

    #print(path)
    ufr = requests.get(url)
    with open(f'{path}\{file_name}{file_type}',"wb") as file: #открываем файл для записи, в режиме wb
        file.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    
    with open(DOCS_FILE, 'a', newline='') as doc_file:
        writer = csv.writer(doc_file, delimiter=';')
        items = [sap_code, f'{file_name}{file_type}']
        writer.writerow(items)
    
    print('Записан файл {} {}'.format(sap_code, file_name))
    logging.info('Записан файл {} {}'.format(sap_code, file_name))


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req


def get_modes(url, titels):
    datas = []
    html = get_html(url).text
    soup = BeautifulSoup(html, 'html.parser')
    fields = soup.find_all('ul', class_='visualNoMarker')
    span_left = []
    span_right = []
    for field in fields:
        all_span_left = field.find_all('span', class_='left')
        all_span_right = field.find_all('span', class_='right')
        for span_l in all_span_left:
            span_left.append(clean_html(str(span_l)))
        for span_r in all_span_right:
            span_right.append(clean_html(str(span_r)))

    sap_code = soup.find('div', id='article-detail').find('span', {'title': 'SAP Code'}).get_text()
    modification = soup.find('span', id='breadcrumbs-current').get_text()
    version = soup.find('span', id='breadcrumbs-5').find('a').get_text()
    main_chapter = titels[0]
    sub_chapter = titels[1]
    serial_name = titels[2]
    serial_description = titels[3]

    # Ссылки на все документы страницы
    # docs_url = []
    # options = soup.find_all('div', class_='option')
    # for option in options:
    #     docs_url.append({
    #         'url': option.find('a').get('href'),
    #         'type': option.find('a', {'target': '_blank'}).get_text()
    #         })
    
    # # Сохрагяем файлы по ссылкам
    # for dicti in docs_url:
    #     url = dicti['url']
    #     print(url)
    #     a = requests.get(url)
    #     file_name = dicti['type'][:dicti['type'].find('(')-1]
    #     print(dicti['type'])
    #     sys.exit()
    #     type = dicti['type'][dicti['type'].find('.'):dicti['type'].find(')')]
    #     save_docs(url, file_name=file_name, file_type=type, sap_code=sap_code)

    # try:
    #     img_url = soup.find('div', class_='portletImages').find('img').get('src')
    # except:
    #     print('IMG ERROR')
    #     img_url = 'IMG ERROR'

    try:
        p = list(soup.find('div', class_='wrapper').find('p'))
    except:
        try:
            p = list(soup.find('div', class_='row Spacer').find('p'))
        except:
            logging.info(f'P find ERROR {main_chapter} {sub_chapter} {serial_name} {url}')
            print(f'P find ERROR {main_chapter} {sub_chapter} {serial_name} {modification}')
            
    try:
        size = p[3][p[3].find(':')+2:]
    except:
        size = 'None'
    try:
        power = p[5][p[5].find(':')+2:]
    except:
        power = 'None'
    try:
        light = p[7][p[7].find(':')+2:]
    except:
        light = 'None'
    try:
        kpd = p[9][p[9].find(':')+2:]
    except:
        kpd = 'None'
    try:
        weight = p[11][p[11].find(':')+2:]
    except:
        weight = 'None'
    try:
        common_datas = p[0]
    except:
        common_datas = 'None'

    print(f'Парсим {main_chapter} | {sub_chapter} | {serial_name} | {modification}')
    datas.append({
        'Раздел 1': main_chapter,
        'Раздел 2': sub_chapter,
        'Серия': serial_name,
        'Описание серии': serial_description,
        'Версия': version,
        'Модификация': modification,
        'SAP CODE': sap_code,
        'Общие данные': common_datas,#p[0],
        'Размеры': size,#p[3][p[3].find(':')+2:],
        'Номинальная мощность': power,#p[5][p[5].find(':')+2:],
        'Световой поток светильника': light,#p[7][p[7].find(':')+2:],
        'КПД светильника': kpd,#p[9][p[9].find(':')+2:],
        'Вес': weight,#p[11][p[11].find(':')+2:],
    })

    for index, span in enumerate(span_left):
        datas[0][span] = span_right[index]
    datas[0]['url'] = url
    save_csv(datas, CSV_FILE)
    datas=[]


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
        
        # Кликаем на каждый товар
        for pr in products:
            serial_name = pr['name']
            html = get_html(pr['url']).text
            soup = BeautifulSoup(html, 'html.parser')
            all_tr_even = soup.find_all('tr', class_='even')
            all_tr_odds = soup.find_all('tr', class_='odd')
            #print(f'Take {serial_name}')

            serial_description = soup.find('div', class_='row rowSpacer').get_text()
            
            all_mod_urls = []
            for tr_even in all_tr_even:
                all_mod_urls.append(tr_even.find('a', class_='article_link').get('href'))
            for tr_odd in all_tr_odds:
                all_mod_urls.append(tr_odd.find('a', class_='article_link').get('href'))

            datas_to_save = [
                main_chapter,
                sub_chapter,
                serial_name,
                serial_description,
                ]

            print(f'ССЫЛОК НА МОДИФИКАЦИИ {len(all_mod_urls)}')
            for url in all_mod_urls:
                get_modes(url, datas_to_save)
            
            # with Pool(20) as p:
            #     p.map(functools.partial(get_modes, titels=datas_to_save), all_mod_urls)


def do_all(each_url):
    html = get_html(each_url)
    get_content(html.text)

def main():
    start = datetime.now()
    logging.info('Начинаем парсить. Старт - {}'.format(start))

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
    logging.info('Закончили. Время выполнения - {}'.format(end - start))
    print(end - start)

if __name__ == '__main__':
    main()