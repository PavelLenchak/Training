# 

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
DIR_TO_SAVE_DOCS = 'D:\Python\__gidini docs'

URL_TO_PARSE = 'https://www.ghidini.it/ProductsList.aspx?lang=en&q=brand,brand_103113'
HOST = 'https://www.ghidini.it'

HEADERS = {
    'user-agent': UserAgent().random,
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


def get_html_text(url, params=''):
    pass

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(URL_TO_PARSE)
    categories = driver.find_elements_by_class_name('dlab-box dlab-gallery-box fly-box')
    print(categories)
# <div class="dlab-box dlab-gallery-box fly-box">
#         <div class="dlab-media dlab-img-effect">
#             <a href="ProjectDs.aspx?lang=en&amp;iid=45518" title="University campus">
#                 <img src="https://www.ghidini.it/catalog/materials/ghidini/pictures/projects/renderings/images/york-university-2.jpg?width=600&amp;height=400&amp;mode=crop" alt="University campus">
#             </a>
#         </div>
#         <div class="dez-info p-a20 bg-white">
#             <p class="dez-title m-t0"><a href="ProjectDs.aspx?lang=en&amp;iid=45518" style="white-space:nowrap;text-overflow:ellipsis;width:100%;display:block;overflow:hidden;">University campus</a></p>
#             <p class="hide-if-empty small">United Kingdom</p>
#             <p><small>Public Buildings</small></p>
#         </div>
#     </div>
    
    pass
