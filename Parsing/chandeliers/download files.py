from typing import Counter
from bs4 import BeautifulSoup
import requests
import csv
import os, sys
from datetime import datetime
import logging
import re
from fake_useragent import UserAgent
import codecs
import string, random
from multiprocessing import Pool
from progress.bar import IncrementalBar
import io

HEADERS = {
    'user-agent': UserAgent().chrome}

DOCS_FILE = 'Parsing\\chandeliers\\docs.csv'

URLS = 'Parsing\\chandeliers\\files\\urls.csv'
TEST_URL_TO_SAVE = 'D:\\Python\\docs'
MAIN_FILE = 'Parsing\\chandeliers\\files\MAIN FILE.csv'
SUB_FILE = 'Parsing\\chandeliers\\files\SUB FILE.csv'

logging.basicConfig(filename='Parsing\\chandeliers\\download docs.csv', level=logging.INFO)

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req

#[{ }]
def save_to_csv(items, path):
    titels = list(items[0].keys())
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in items:
            task = [str(item[titels[i]]).replace('.', ',') for i in range(len(titels))]
            writer.writerow(task)
            print(f'Saving {task[-1]}')
    print('Saving process have done')

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
    with open(f'{TEST_URL_TO_SAVE}\{sap_code}_{file_name}{file_type}',"wb") as file: #открываем файл для записи, в режиме wb
        file.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    
    with open(DOCS_FILE, 'a', newline='') as doc_file:
        writer = csv.writer(doc_file, delimiter=';')
        items = [sap_code, f'{sap_code}_{file_name}{file_type}']
        writer.writerow(items)
    
    print('Записан файл {}_{}'.format(sap_code, file_name))
    logging.info('Записан файл {}_{} {}'.format(sap_code, file_name, url))

def get_files(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    sap_code = soup.find('div', id='article-detail').find('span', {'title': 'SAP Code'}).get_text()
    #print(f'Парсим {sap_code}')
# Ссылки на все документы страницы
    docs_url = []
    options = soup.find_all('div', class_='option')
    for option in options:
        docs_url.append({
            'url': option.find('a').get('href'),
            'type': option.find('a', {'target': '_blank'}).get_text()
            })
    
    bar = IncrementalBar('Progress', max = len(docs_url))
    # # Сохрагяем файлы по ссылкам
    for dicti in docs_url:
        bar.next()
        url = dicti['url']
        #a = requests.get(url)
        #file_name = dicti['type'][:dicti['type'].find('(')-1]

        file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        type = dicti['type'][dicti['type'].find('.'):dicti['type'].find(')')]
        save_docs(url, file_name=file_name, file_type=type, sap_code=sap_code)
    bar.finish()


def get_mode(url):
    html = get_html(url).text
    soup = BeautifulSoup(html, 'html.parser')
    all_bread_crumbs = soup.find_all('div', id='portal-breadcrumbs')
    wrapper = soup.find('div', id='article-data')
    detail = soup.find('div', id='article-detail')
    field = soup.find('div', class_='row rowSpacer')
    span = clean_html(str(field.find_all('span')))

    bread_crumbs = []
    for bc in all_bread_crumbs:
        bread_crumbs.append({
            'Chapter 1': bc.find('span', id='breadcrumbs-2').find('a').get_text(),
            'Chapter 2': bc.find('span', id='breadcrumbs-3').find('a').get_text(),
            'Seria': bc.find('span', id='breadcrumbs-4').find('a').get_text(),
            'Decripion of Seria': wrapper.find('p').get_text(),
            'Version': bc.find('span', id='breadcrumbs-5').find('a').get_text(),
            'Description extra': span,
            'SAP Code': clean_html(str(detail.find('p').find('span', {'title': 'SAP Code'}).get_text()))
        })
        
    # print(bread_crumbs)
    # sys.exit()

    save_to_csv(bread_crumbs, SUB_FILE)


def main():
    start = datetime.now()
    urls = read_csv(MAIN_FILE)
    # counter = 0 
    # for url in urls:
    #     if counter < 2:
    #         get_files(url)
    #     counter += 1

    for url in urls:
        get_mode(url)

    # with Pool(40) as p:
    #     p.map(get_files, urls)
    
    end = datetime.now()
    print(f'Закончили выгрузку {end - start}')
if __name__ == '__main__':
    main()