from bs4.element import ProcessingInstruction
import requests
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


CSV = 'Parsing\\xbox price\\xbox prices.csv'
HOST = 'https://www.eldorado.ru'
URL = 'https://www.eldorado.ru/search/catalog.php?q=xbox&offset=0&utf'
HEADERS = {
    'user-agent': UserAgent().chrome
}

def get_html(url, params=''):
    response = requests.get(url, headers=HEADERS, params=params)
    return response

def save_csv(items, path):
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in items:
            writer.writerow([item['name'], item['price']])


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='xu')
    prices = []

    for item in items:
        prices.append(
            {
                'name': item.find('a', class_='Ju').get_text(),
                'price': item.find('span', class_='hF lF').get_text(strip=True),
                #'link': HOST + item.find('a', class_='vu').get('href')
            }
        )
        
    # for price in prices:
    #     print(price)
    return prices

def main():
    html = get_html(URL)
    if html.status_code == 200:
        STEP = 36
        PAGENATION = STEP * int(input('Сколько страниц спарсить? --> '))
        products = []   

        for page in range(0, PAGENATION, STEP):
            print(f'Парсим страницу {int(page / STEP) + 1}')
            html = get_html(URL, params={'offset': page})
            products.extend(get_content(html.text))
            save_csv(products, CSV)

        print('SUCSESS')
    else:
        print(f'ERROR - {html.status_code}')

if __name__ == '__main__':
    main()