import requests
from bs4 import BeautifulSoup
import csv

FILE_NAME = 'Parsing\\forecast\\weather.csv'
HOST = 'https://yandex.ru'
URL = 'https://yandex.ru/pogoda/?lat=55.03307&lon=73.251633'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36'
}

def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='forecast-briefly__day')
    days = []

    for item in items:
        days.append(
            {
                'name': item.find('div', class_='forecast-briefly__name').get_text(),
                'date': item.find('time', class_='time forecast-briefly__date').get_text(),
                'daytime': item.find('div', class_='forecast-briefly__temp_day').find('span', class_='temp__value').get_text(),
                'condition': item.find('div', class_='forecast-briefly__condition').get_text(),
            }
        )
    return days

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['День недели','Дата','Температура','Состояние'])
        for item in items:
            writer.writerow([item['name'], item['date'], item['daytime'], item['condition']])

def main():
    html = get_html(URL)
    if html.status_code == 200:
        forecast = get_content(html.text)
        save_file(forecast, FILE_NAME)
        print('SUCSESS')
    else:
        print('Error: ' + html.status_code)
    
if __name__ == '__main__':
    main()