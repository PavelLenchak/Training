from bs4.element import ProcessingInstruction
import requests
import csv
from bs4 import BeautifulSoup


CSV = 'xbox prices.csv'
HOST = 'https://www.eldorado.ru'
URL = 'https://www.eldorado.ru/search/catalog.php?q=xbox'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36',
}


def get_html(url, params=''):
    response = requests.get(url, HEADERS)
    print(response)

    for k,v in response.request.headers.items():
        print (k + ': ' + v)

get_html(URL)

def get_content(html):
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='xu')
    prices = []

    for item in items:
        prices.append(
            {
                'status': item.find('div', class_='tB').get_text(),
                'price': item.find('span', class_='hF lF').get_text(),
            }
        )
    
    print(prices)

def main():
    html = get_html(URL)
    get_content(html)
