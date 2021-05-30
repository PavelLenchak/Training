# lightning.py

import os, sys, time
from socket import timeout
from datetime import datetime
import asyncio
import httpx
import csv
import logging
from fake_useragent import UserAgent
import random
import pathlib
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver


MAIN_DIR = pathlib.Path(__file__).parent
CSV = 'basic info.csv'
DIR_TO_SAVE_DOCS = 'D:\Python\__lighning docs'

print(f'{MAIN_DIR}\{CSV}')

URL_TO_PARSE = 'https://www.linealight.com/en-gb/products'
HOST = 'https://www.linealight.com'

HEADERS = {
    'user-agent': UserAgent().random,
    'origin': 'https://www.linealight.com',
    'referer': 'https://www.linealight.com/',
}

PROXIES = [
    '91.193.253.188:23500',
    '176.9.119.170:3128',
    '176.9.75.42:3128',
    '88.198.24.108:8080',
    '95.141.193.35:80',
    '176.9.75.42:8080',
    '95.141.193.14:80',
    '5.252.161.48:8080',
    '176.9.119.170:3128',
]

logging.basicConfig(filename=f'{MAIN_DIR}\logs.csv', level=logging.INFO)
lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

def save_docs(url, file_name, file_type):
    # path = f'{DOCS_PATH}\{sap_code}'
    # if not os.path.exists(path):
    #     os.mkdir(path)

    #print(path)
    ufr = requests.get(url)
    with open(f'{DIR_TO_SAVE_DOCS}\{file_name}{file_type}',"wb") as file: #открываем файл для записи, в режиме wb
        file.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    
    with open(DOCS_FILE, 'a', newline='') as doc_file:
        writer = csv.writer(doc_file, delimiter=';')
        items = [f'{file_name}{file_type}', url]
        writer.writerow(items)
    
    print('Записан файл {}'.format(file_name))
    logging.info('Записан файл {} {}'.format(file_name, url))


def save_csv(items, file_name):
    print(items)
    titels = list(items[0].keys())
    print(titels)
    with open(f'{MAIN_DIR}\{file_name}.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        #print(titels)
        for item in items:
            task = [item[titels[i]] for i in range(len(titels))]
            writer.writerow(task)



if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(URL_TO_PARSE)
    driver.fullscreen_window()
    elems = driver.find_elements_by_class_name('c-macro-category-box__link') # tag a
    links = [elem.get_attribute('href') for elem in elems]

    # перехдим по главным категориям
    for link in links[:-1]:
        driver.get(link)
        time.sleep(2)

        main_category_name = driver.find_element_by_class_name('c-common-cover__main').text
        a_elems = driver.find_elements_by_class_name('c-article-wrap')
        sub_urls = [elem.get_attribute('href') for elem in a_elems]
        # перехдим по подкатегории
        for sub_link in sub_urls:
            driver.get(sub_link)
            time.sleep(2)

            sub_category_name = driver.find_element_by_class_name('c-common-cover__main').text
            fam_elems = driver.find_elements_by_class_name('c-article-wrap')
            f_urls = [elem.get_attribute('href') for elem in fam_elems]
            # переходим по продуктовым семьям
            for f_link in f_urls:
                driver.get(f_link)
                time.sleep(2)

                family_name = driver.find_element_by_class_name('c-common-cover__main').text
                product_elems = driver.find_elements_by_class_name('c-article-wrap')
                pr_urls = [elem.get_attribute('href') for elem in product_elems]
                # переходим на каждый продукт
                for p_link in pr_urls:
                    driver.get(p_link)
                    time.sleep(2)
                    t_body = driver.find_element_by_class_name('o-table__body').text.split('\n')
                    pr_name = driver.find_element_by_class_name('c-family-description__main').text

                    # for i in range(len(t_body)):
                    data_to_save = {
                        'Main category name': main_category_name,
                        'Sub category name': sub_category_name,
                        'Family name': family_name,
                        'Product name': pr_name,
                        }
                    #     save_csv(data_to_save, 'basic info')
                    
                    docs_elems = driver.find_elements_by_class_name('o-table__link')
                    docs_urls = [elem.get_attribute('href') for elem in docs_elems]
                    for d_link in docs_urls:
                        driver.get(d_link)
                        time.sleep(2)

                        pr_specs = driver.find_element_by_class_name('c-product__specs').text.split('\n')
                        pr_abstract = driver.find_element_by_class_name('c-product-abstract').text
                        for i in range(len(pr_specs)):
                            data_to_save[f'{i}'] = pr_specs[i]
                        data_to_save['Info'] = pr_abstract

                        select_all_button = driver.find_element_by_id('select-all-attachments')
                        select_all_button.click

                        download_docs_button = driver.find_element_by_id('download-attachments')
                        download_docs_button.click
                        
                        # Сохраняем общую информацию
                        save_csv([data_to_save], 'basic info')
                        sys.exit()


                        driver.back()
                        time.sleep(2)

                    driver.back()
                    time.sleep(2)


                driver.back()
                time.sleep(2)
            

            driver.back()
            time.sleep(2)


        driver.back()
        time.sleep(2)

    
    driver.close()
    driver.quit()
