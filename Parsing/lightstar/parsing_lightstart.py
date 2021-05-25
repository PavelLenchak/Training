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
            task = []
            for i in range(len(titels)):
                if type(item[titels[i]]) == list:
                    task.append('; '.join(item[titels[i]]))
                else:
                    task.append(item[titels[i]])
            #task = ['; '.join(item[titels[i]]) for i in range(len(titels)) if type(item[titels[i]]) == list else item[titels[i]]
            print(task)
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

        try:
            name = header[0].get_text()
        except:
            name = 'None'

        try:
            id = header[1].get_text().replace(u'\xa0', u' ')
        except:
            id = 'None'

        try:
            main_data = [i.get_text() for i in arti.find('div', class_='card-product__content').find_all('div')]
        except:
            main_data = 'None'

        try:
            url = arti.find('a', class_='card-product__link').get('href')
        except:
            url = 'None'
        # specification = arti.find_all('dd', class_='specification__definition')
        # try:
        #     ip = specification[1].get_text()
        # except:
        #     ip = 'None'
        to_save.append({
            'Name': name,
            'ID': id,
            'Main Data': main_data,#specification[0].get_text(),
            #'IP': ip, specification specification--small
            'URL': url,
        })
        #print(to_save)
        save_to_csv(to_save)
        to_save = []

    #print(f'Parse {url} - {page}')

def do_all(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    try:
        links = soup.find('ul', class_='pagination__list').find_all('a', class_='pagination__link')
    except AttributeError:
        max_pages=1
        host = url
        print(f'DONT FIND LINKS {url}')
    else:
        pages = []
        for link in links:
            pages.append({
                'url': link.get('href')
            })
        host = pages[-1]['url']
        max_pages = int(pages[-1]['url'].split('/')[-1].replace('?page=',''))
    finally:
        for current_page in range(1, max_pages+1):
            if not current_page > max_pages:
                print(f'Parsing {host} {current_page}')
                get_content(host, current_page)


def main():
    start = datetime.now()
    # Переходим по группам
    html = get_html('https://lightstar.ru')
    soup = BeautifulSoup(html.text, 'html.parser')
    group_links = soup.find_all('li', class_='menu__content-item')
    urls = []
    
    for i in group_links:
        urls.append(
            i.find('a', class_='menu__content-link').get('href')
        )
    print(len(urls))
    
    # Переходим по страницам
    with Pool(multiprocessing.cpu_count()) as p:
        p.map(do_all, urls)

    end = datetime.now()
    print(f'FINISH: {end-start}')


if __name__ == '__main__':
    main()