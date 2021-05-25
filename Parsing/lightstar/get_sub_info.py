import csv, sys
import fake_useragent
import requests
from bs4 import BeautifulSoup
import fake_useragent

PATH = 'Parsing\\lightstar\\lightstar.csv'
CSV_FILE = 'Parsing\\lightstar\\sub_info.csv'

HEADERS = {
    'user-agent': fake_useragent.UserAgent().chrome,
}

def save_to_csv(items):
    #print(f'Start saving process')
    titels = list(items[0].keys())
    with open(CSV_FILE, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in items:
            task = [str(item[titels[i]]) for i in range(len(titels))]
            writer.writerow(task)
            print(f'Saving {task[0]}')
    print('Saving process have done')

def read_csv(path):
    urls = []
    with open(path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            url = row[-1].replace(',', '.')
            urls.append(url)
            #save_to_csv('Parsing\\chandeliers\\files\\urls.csv',url)
    return urls

def get_html(url, params=''):
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response
    else:
        print(f'Connection ERROR {response.status_code}')
        print(url)


def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    li = soup.find_all('li', class_='breadcrumb__item')
    div = soup.find_all('div', class_='specification__wrapper')
    a = soup.find_all('section', class_='tab__panel tab__panel--icon')

    datas = []
    chapters = [i.get_text() for i in li]
    details = [i.get_text() for i in div]
    files = ''
    for i in a:
        files = i.find('a').get('href')
    print(files)
    datas.append({
        'Chapters': chapters,
        'Detail': details,
        'URL': url,
        'Files': files,
    })
    save_to_csv(datas)
    

def main():
    urls = read_csv(PATH)
    for url in urls:
        get_content(url)


if __name__ == '__main__':
    main()