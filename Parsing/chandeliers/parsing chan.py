import sys
import re
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import csv

# Фото Свойтво товаров Документы
# <img src="http://www.thornlighting.ru/img/31/tlg_thumb_downlights/@@images/c47c664c-1c6f-4b2e-9622-51c23accdef6.jpeg" alt="Светильники типа downlight" title="" height="176" width="176">


HOST = 'http://www.thornlighting.ru'
URL = 'http://www.thornlighting.ru/ru-ru/produkty/vnutriennieie-osvieshchieniie'

HEADERS = {
    'user-agent': UserAgent().chrome
}

def save_csv(itens, path):
    pass

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def get_html(url, params=''):
    req = requests.get(url, params=params)
    return req

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='pbf width-1:4')

    # получаем ссылки ВНУТРЕННЕЕ ОСВЕЩЕНИЕ
    project_urls = []
    for item in items:
        project_urls.append(item.find('a', class_='discreet').get('href'))

    all_datas = []
    for p_u in project_urls:
        html = get_html(p_u).text
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('div', class_='pbf width-1:4')

        products = []
        for item in items:
            products.append(item.find('a', class_='discreet').get('href'))
        
        datas = []
        for pr in products:
            html = get_html(pr).text
            soup = BeautifulSoup(html, 'html.parser')
            all_tr_even = soup.find_all('tr', class_='even')
            all_tr_odds = soup.find_all('tr', class_='odd')

            # <td class="weight">0.91</td>
            #<a class="article_link" href="http://www.thornlighting.ru/ru-ru/produkty/vnutriennieie-osvieshchieniie/svietilniki-tipa-downlight/Chalice/chalice-200/96629019">CHAL 200 LED1400-830 HF RSB</a>
            for tr_even in all_tr_even:
                all_td = tr_even.find_all('td')
                datas.append({
                    'Описание': tr_even.find('a', class_='article_link').get_text(),
                    'Мощность W': clean_html(str(all_td[1])),
                    'Световой поток': clean_html(str(all_td[2])),
                    'Type': clean_html(str(all_td[6])),
                    'Вес': tr_even.find('td', class_='weight').get_text(),
                    'SAP CODE': clean_html(str(all_td[9])),
                })

            for tr_odd in all_tr_odds:
                all_td = tr_odd.find_all('td')
                datas.append({
                    'Описание': tr_odd.find('a', class_='article_link').get_text(),
                    'Мощность W': clean_html(str(all_td[1])),
                    'Световой поток': clean_html(str(all_td[2])),
                    'Type': clean_html(str(all_td[6])),
                    'Вес': tr_odd.find('td', class_='weight').get_text(),
                    'SAP CODE': clean_html(str(all_td[9])),
                })
        
        all_datas.append(datas)
    
    for i in all_datas:
        print(i, sep='\n')
    sys.exit()


def main():
    html = get_html(URL)
    get_content(html.text)

if __name__ == '__main__':
    main()