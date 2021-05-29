# lightning.py

import os, sys, time
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

async def get_html():
    pass


async def parse():
    pass


async def write_scv():
    pass


async def parse_and_write():
    pass


def get_html_text(url, proxy='91.193.253.188:23500', params=''):
    pass

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(URL_TO_PARSE)
    links = driver.find_elements_by_class_name('c-macro-category-box') # tag article
    print(len(links))
    
    for main_url in links[:-1]:
        new_page = main_url.find_element_by_class_name('c-macro-category-box__link').get_attribute('href')
        driver.get(new_page)

        # ссылки на каждую категории внутри главных категорий
        li_elems = driver.find_elements_by_class_name('c-category-list__item')
        for sub_url in li_elems:
            new_product = sub_url.find_element_by_class_name('c-article-wrap').get_attribute('href')
            print(new_product)
            driver.get(new_product)

            time.sleep(2)
            driver.back()

    driver.close()
    pass
