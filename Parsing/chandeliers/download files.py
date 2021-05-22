from bs4 import BeautifulSoup
import requests
import csv
import os, sys
import logging
import re
from fake_useragent import UserAgent
import codecs

HEADERS = {
    'user-agent': UserAgent().chrome}

DOCS_PATH = 'Parsing\\chandeliers\\docs'
DOCS_FILE = 'Parsing\\chandeliers\\docs.csv'

PRODICTS_FILE = 'Parsing\\chandeliers\\files\\products.csv'

logging.basicConfig(filename='Parsing\\chandeliers\\download docs.csv', level=logging.INFO)

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req

def read_csv(path):
    urls = []
    with codecs.open(path, 'r', 'utf-32') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            urls.append(row[-1].replace(',', '.'))
    print(len(urls))
    sys.exit()
        

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

def get_files(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    sap_code = soup.find('div', id='article-detail').find('span', {'title': 'SAP Code'}).get_text()
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
        print(url)
        a = requests.get(url)
        file_name = dicti['type'][:dicti['type'].find('(')-1]
        print(dicti['type'])

        type = dicti['type'][dicti['type'].find('.'):dicti['type'].find(')')]
        save_docs(url, file_name=file_name, file_type=type, sap_code=sap_code)



def main():
    read_csv(PRODICTS_FILE)
    

if __name__ == '__main__':
    main()