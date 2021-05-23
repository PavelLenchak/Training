# -*- coding: utf-8 -*-

from typing import Counter
from bs4 import BeautifulSoup
import requests
import csv
import os, sys, time
from datetime import datetime
import logging
import re
from fake_useragent import UserAgent
import codecs
import string, random
from multiprocessing import Pool, cpu_count
from progress.bar import IncrementalBar
import io, logging

# logging.basicConfig(filename='Parsing\\chandeliers\\saving_process_logs.csv', level=logging.INFO)
logging.basicConfig(filename='Parsing\\chandeliers\\docs_process.csv', level=logging.INFO)

HEADERS = {
    'user-agent': UserAgent().chrome}

DOCS_FILE = 'Parsing\\chandeliers\\docs.csv'

URLS = 'Parsing\\chandeliers\\files\\urls.csv'
TEST_DIR_TO_SAVE = 'D:\\Python\\docs'
MAIN_FILE = 'Parsing\\chandeliers\\to post\\MAIN FILE.csv'
SUB_FILE = 'Parsing\\chandeliers\\SUB FILE.csv'

TO_PARSING = 'Parsing\\chandeliers\\files\\to_parsing.csv'
NOT_FIND = 'Parsing\\chandeliers\\files\\not_find.csv'

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_html(url):
    try:
        time.sleep(2)
        req = requests.get(url, headers=HEADERS)
        req.encoding = 'utf8'
    except requests.exceptions.ConnectionError:
        print('EXEPTION ERROR')
        time.sleep(20)
        get_html(url)
    
    return req

#[{ }]
def save_to_csv(items, path):
    try:
        titels = list(items[0].keys())
    except IndexError as ie:
        titels = ['None']
        logging.info('INDEX ERROR', ie)
        print('INDEX ERROR', ie)
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in items:
            task = [re.sub('[^A-Z a-z А-Я а-я 0-9 .\/;:-]', '', str(item[titels[i]])) for i in range(len(titels))]
            row_to_save = [re.sub('[^A-Z a-z А-Я а-я 0-9 .\/;:-]', '', str(task))]
            writer.writerow(task)
        print(f'Saving {task[-1]}')
    #print(f'Saving process have done')

def read_csv(path):
    urls = []
    with open(path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            url = row[-1].replace(',', '.')
            urls.append(url)
            #save_to_csv('Parsing\\chandeliers\\files\\urls.csv',url)
    return urls

def save_docs(url, file_name, file_type, sap_code):
    # path = f'{DOCS_PATH}\{sap_code}'
    # if not os.path.exists(path):
    #     os.mkdir(path)

    #print(path)
    ufr = requests.get(url)
    with open(f'{TEST_DIR_TO_SAVE}\{sap_code}_{file_name}{file_type}',"wb") as file: #открываем файл для записи, в режиме wb
        file.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    
    with open(DOCS_FILE, 'a', newline='') as doc_file:
        writer = csv.writer(doc_file, delimiter=';')
        items = [sap_code, f'{sap_code}_{file_name}{file_type}', url]
        writer.writerow(items)
    
    print('Записан файл {}_{}'.format(sap_code, file_name))
    logging.info('Записан файл {}_{} {}'.format(sap_code, file_name, url))

def get_files(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    detail = soup.find('div', id='article-detail')
    try:
        sap_code = clean_html(str(detail.find('p').find('span', {'title': 'SAP Code'}).get_text()))
    except:
        sap_code = url[:-8]

    #sap_code = soup.find('div', id='article-detail').find('span', {'title': 'SAP Code'}).get_text()
    print(f'Парсим {sap_code}')
    logging.info(f'Парсим {sap_code}')
# Ссылки на все документы страницы
    docs_url = []
    options = soup.find_all('div', class_='option')
    for option in options:
        docs_url.append({
            'url': option.find('a').get('href'),
            'type': option.find('a', {'target': '_blank'}).get_text()
            })
    
    # # Сохрагяем файлы по ссылкам
    for dicti in docs_url:
        url = dicti['url']
        #a = requests.get(url)
        #file_name = dicti['type'][:dicti['type'].find('(')-1]

        file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        type = dicti['type'][dicti['type'].find('.'):dicti['type'].find(')')]
        save_docs(url, file_name=file_name, file_type=type, sap_code=sap_code)


def get_mode(url):
    html = get_html(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        all_bread_crumbs = soup.find_all('div', id='portal-breadcrumbs')
    except AttributeError:
        logging.info(f'Dont FIND ALL ERROR {url}')
        print(f'Find All ERROR {url}')
    
    try:
        wrapper = soup.find('div', id='article-data')
    except:
        logging.info(f'Dont WRAPPER ERROR {url}')
        print(f'Find WRAPPER ERROR {url}')

    try:
        # Описание серии
        p = wrapper.find('p').get_text()
    except:
        p = 'None'
        logging.info(f'Dont find P ERROR {url}')
        #print(f'Dont find P ERROR {url}')

    detail = soup.find('div', id='article-detail')
    field = soup.find('div', class_='row rowSpacer')
    try:
        # Доп описание
        span = clean_html(str(field.find_all('span')))
    except AttributeError:
        span = 'None'
        logging.info(f'Dont find SPAN ERROR {url}')
        #print(f'Dont find SPAN ERROR {url}')

    bread_crumbs = []
    for bc in all_bread_crumbs:
        bread_crumbs.append({
            'Chapter 1': bc.find('span', id='breadcrumbs-2').find('a').get_text(),
            'Chapter 2': bc.find('span', id='breadcrumbs-3').find('a').get_text(),
            'Seria': bc.find('span', id='breadcrumbs-4').find('a').get_text(),
            'Decripion of Seria': p,
            'Version': bc.find('span', id='breadcrumbs-5').find('a').get_text(),
            'Description extra': span,
            'SAP Code': clean_html(str(detail.find('p').find('span', {'title': 'SAP Code'}).get_text())),
            'URL': clean_html(url),
        })
        
    # print(bread_crumbs)
    # sys.exit()
    logging.info(f'PARSING {url}')
    save_to_csv(bread_crumbs, SUB_FILE)


def main():
    start = datetime.now()
    urls = read_csv(NOT_FIND)
    # counter = 0 
    # for url in urls:
    #     if counter < 2:
    #         get_files(url)
    #     counter += 1

    # bar = IncrementalBar('Progress', max = len(urls))
    # for url in urls:
    #     bar.next()
    #     get_mode(url)

    # with Pool(cpu_count()) as p:
    #     p.map(get_mode, urls)

    with Pool(40) as p:
        p.map(get_files, urls)
    
    end = datetime.now()
    print(f'Закончили выгрузку {end - start}')
if __name__ == '__main__':
    main()