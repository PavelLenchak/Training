import multiprocessing
import re
import requests
from bs4 import BeautifulSoup
import csv
import os, sys, time, io
from datetime import datetime
import fake_useragent
from multiprocessing import Pool

HEADERS = {
    'user-agent': fake_useragent.UserAgent().chrome,
}

CSV_FILE = 'Parsing\\lightstar\\lightstar.csv'
URL = 'https://lightstar.ru/kupit-lustry-svetilniki-optom/'


def save_to_csv(items):
    #print(f'Start saving process')
    titels = list(items[0].keys())
    with open(CSV_FILE, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in items:
            task = [str(item[titels[i]]).replace('.', ',') for i in range(len(titels))]
            writer.writerow(task)
            # print(f'Saving {task[0]}')
    # print('Saving process have done')

def get_html(url, params=''):
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response
    else:
        print(f'Connection ERROR {response.status_code}')
        print(url)


def get_content(url, page):
    html = get_html(url, {'page': page})
    soup = BeautifulSoup(html.text, 'html.parser')
    articles = soup.find_all('article', class_='card-product')
    to_save = []
    for arti in articles:
        header = arti.find_all('span', class_='card-product__sub-title')
        # specification = arti.find_all('dd', class_='specification__definition')
        # try:
        #     ip = specification[1].get_text()
        # except:
        #     ip = 'None'
        to_save.append({
            'Name': header[0].get_text(),
            'ID': header[1].get_text().replace(u'\xa0', u' '),
            'Main Data': arti.find('dl', class_='specification specification--small').get_text(),#specification[0].get_text(),
            #'IP': ip,
            'URL': arti.find('a', class_='card-product__link').get('href'),
        })
        save_to_csv(to_save)
        to_save = []

    print(f'Parse {url} - {page}')

def do_all(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    links = soup.find('ul', class_='pagination__list').find_all('a', class_='pagination__link')
    
    pages = []
    for link in links:
        pages.append({
            'url': link.get('href')
        })
    host = pages[-1]['url']
    max_pages = int(pages[-1]['url'].split('/')[-1].replace('?page=',''))

    current_page = 0
    value = max_pages
    while current_page <= value:
        current_page += 1
        get_content(host, current_page)


def main():
    start = datetime.now()
    # Переходим по группам
    html = get_html('https://lightstar.ru')
    soup = BeautifulSoup(html.text, 'html.parser')
    group_limks = soup.find_all('li', class_='menu__content-item')
    urls = []
    for i in group_limks:
        urls.append(
            i.find('a', class_='menu__content-link').get('href')
        )
    
    # Переходим по страницам
    with Pool(multiprocessing.cpu_count()) as p:
        p.map(do_all, urls)
    # for url in urls:
    #     html = get_html(url)
    #     soup = BeautifulSoup(html.text, 'html.parser')
    #     links = soup.find('ul', class_='pagination__list').find_all('a', class_='pagination__link')
        
    #     pages = []
    #     for link in links:
    #         pages.append({
    #             'url': link.get('href')
    #         })
    #     host = pages[-1]['url']
    #     max_pages = int(pages[-1]['url'].split('/')[-1].replace('?page=',''))

    #     current_page = 0
    #     value = max_pages
    #     while current_page < value:
    #         current_page += 1
    #         get_content(host, current_page)

    end = datetime.now()
    print(f'FINISH: {end-start}')


if __name__ == '__main__':
    main()