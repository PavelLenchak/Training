from bs4 import BeautifulSoup
import requests
import csv
import os, sys
import logging
import re
from fake_useragent import UserAgent
import codecs
import string, random
from multiprocessing import Pool

HEADERS = {
    'user-agent': UserAgent().chrome}

DOCS_PATH = 'Parsing\\chandeliers\\docs'
DOCS_FILE = 'Parsing\\chandeliers\\docs.csv'

PRODICTS_FILE = 'Parsing\\chandeliers\\files\\products.csv'

FIRST_PART = 'Parsing\\chandeliers\\files\\first_urls.csv'
SECOND_PART = 'Parsing\\chandeliers\\files\\second_urls.csv'
URLS = 'Parsing\\chandeliers\\files\\urls.csv'
LAST_URLS = 'Parsing\\chandeliers\\files\\last_urls.csv'
TEST_URL_TO_SAVE = 'D:\\Python\\docs'

logging.basicConfig(filename='Parsing\\chandeliers\\download docs.csv', level=logging.INFO)

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req

# def save_to_csv(path, item):
#     with open('Parsing\\chandeliers\\files\\urls.csv', 'a', newline='') as csv_file:
#             writer = csv.writer(csv_file, delimiter=';')
#             writer.writerow([item])

def read_csv(path):
    urls = []
    with open(path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            url = row[0].replace(',', '.')
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
    
    # # Сохрагяем файлы по ссылкам
    for dicti in docs_url:
        url = dicti['url']
        #a = requests.get(url)
        #file_name = dicti['type'][:dicti['type'].find('(')-1]

        file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        type = dicti['type'][dicti['type'].find('.'):dicti['type'].find(')')]
        save_docs(url, file_name=file_name, file_type=type, sap_code=sap_code)


def main():
    urls = read_csv(URLS)
    # counter = 0 
    # for url in urls:
    #     if counter < 2:
    #         get_files(url)
    #     counter += 1

    with Pool(40) as p:
        p.map(get_files, urls)
    
if __name__ == '__main__':
    main()