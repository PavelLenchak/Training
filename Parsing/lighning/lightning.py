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
from multiprocessing import Pool, cpu_count


MAIN_DIR = pathlib.Path(__file__).parent
CSV = 'basic info.csv'
DIR_TO_SAVE_DOCS = 'D:\Python\__lighning docs'

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

def save_csv(items, file_name):
    titels = list(items[0].keys())
    with open(f'{MAIN_DIR}\{file_name}.csv', 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        #print(titels)
        for item in items:
            task = [item[titels[i]] for i in range(len(titels))]
            writer.writerow(task)


def parse_info(urls):
    pass


def main(urls):
    # перехдим по главным категориям
    for link in urls[:-1]:
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

                    data_to_save = {
                        'Main category name': main_category_name,
                        'Sub category name': sub_category_name,
                        'Family name': family_name,
                        'Product name': pr_name,
                        }
                    
                    docs_elems = driver.find_elements_by_class_name('o-table__link')
                    docs_urls = [elem.get_attribute('href') for elem in docs_elems]
                    docs_code = [elem.text for elem in docs_elems]
                    for index, d_link in enumerate(docs_urls):
                        code = docs_code[index]
                        driver.get(d_link)
                        time.sleep(2)

                        pr_specs = driver.find_element_by_class_name('c-product__specs').text.split('\n')
                        pr_abstract = driver.find_element_by_class_name('c-product-abstract').text
                        for i in range(len(pr_specs)):
                            data_to_save[f'{i}'] = pr_specs[i]
                        data_to_save['Code'] = code
                        data_to_save['Info'] = pr_abstract

                        print(f'Saving {code}')
                        try:
                            select_all_button = driver.find_element_by_id('select-all-attachments')
                            select_all_button.send_keys(selenium.webdriver.common.keys.Keys.SPACE)
                            #select_all_button.click()

                            download_docs_button = driver.find_element_by_id('download-attachments')
                            download_docs_button.click()
                            time.sleep(10)
                        except Exception as ex:
                            print(f'Не могу скачать файлы {pr_name} {code}')
                            logging.info(f'Файлы не загружены {pr_name} {code}')
                        finally:
                            logging.info(f'Save the element {sub_category_name} {code}')
                            # Сохраняем общую информацию
                            save_csv([data_to_save], 'basic info')

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


if __name__ == '__main__':
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : "D:\Python\__lighning docs"}
    chromeOptions.add_experimental_option("prefs",prefs)

    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.get(URL_TO_PARSE)
    elems = driver.find_elements_by_class_name('c-macro-category-box__link')
    links = [elem.get_attribute('href') for elem in elems]

    # with Pool(cpu_count()) as p:
    #     p.map(main, links)
    try:
        main(links)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
