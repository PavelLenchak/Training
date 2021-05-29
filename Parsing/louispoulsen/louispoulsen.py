# 

import os, sys, time
from datetime import datetime
import asyncio
from fake_useragent.utils import get
import httpx
import csv
import logging
from fake_useragent import UserAgent
import random
import pathlib
import requests
from bs4 import BeautifulSoup

MAIN_DIR = pathlib.Path(__file__).parent

URL_TO_PARSE = 'https://www.louispoulsen.com/en/catalog/professional/find-spare-part'
HOST = 'https://www.louispoulsen.com'

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
    # time.sleep(2)
    response = requests.post(url, 
                            headers=HEADERS, 
                            proxies={'http': 'http://' + random.choice(PROXIES)},
                            params=params)
    print(url, response)
    return response.text

if __name__ == '__main__':
    html_text = get_html_text(URL_TO_PARSE)
    soup = BeautifulSoup(html_text, 'html.parser')
    
    for item in soup:
        print(item)

    pass
