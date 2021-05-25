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

TEST_DIR_TO_SAVE = 'Parsing\\lightstar\\test'
DOCS_FILE = 'Parsing\\lightstar\\docs.csv'

def read_csv(path):
    urls = []
    with open(path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            url = row[-1].replace(',', '.')
            urls.append(url)
            #save_to_csv('Parsing\\chandeliers\\files\\urls.csv',url)
    return urls

def save_docs(url, file_name, file_type):
    # path = f'{DOCS_PATH}\{sap_code}'
    # if not os.path.exists(path):
    #     os.mkdir(path)

    #print(path)
    ufr = requests.get(url)
    with open(f'{TEST_DIR_TO_SAVE}\{file_name}{file_type}',"wb") as file: #открываем файл для записи, в режиме wb
        file.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    
    with open(DOCS_FILE, 'a', newline='') as doc_file:
        writer = csv.writer(doc_file, delimiter=';')
        items = [f'{file_name}{file_type}', url]
        writer.writerow(items)
    
    print('Записан файл {}'.format(file_name))
    logging.info('Записан файл {} {}'.format(file_name, url))


def get_file(url):
    file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    type = '.' + url.split('.')[-1]
    f = url.split('/')[-2]
    save_docs(url, file_name=f+file_name, file_type=type)

def main():
    start = datetime.now()
    urls = read_csv('Parsing\\lightstar\\sub_info.csv')
    # counter = 0 
    # for url in urls:
    #     if counter < 2:
    #         get_files(url)
    #     counter += 1

    # bar = IncrementalBar('Progress', max = len(urls))
    for url in urls:
        # bar.next()
        get_file(url)

    # with Pool(cpu_count()) as p:
    #     p.map(get_mode, urls)

    # with Pool(40) as p:
    #     p.map(get_files, urls)
    
    end = datetime.now()
    print(f'Закончили выгрузку {end - start}')
if __name__ == '__main__':
    main()