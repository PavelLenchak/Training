import csv, sys
import fake_useragent
import requests
from bs4 import BeautifulSoup
import fake_useragent
import random, string
from multiprocessing import Pool, cpu_count


PATH = 'Parsing\\lightstar\\to post\\lightstar.csv'
CSV_FILE = 'Parsing\\lightstar\\sub_info.csv'
TO_SAVE_DOCS = 'D:\\Python\\lightstart docs'
DOCS_FILE = 'Parsing\\lightstar\\docs.csv'
TO_URLS = 'Parsing\\lightstar\\to post\\urls.csv'

HEADERS = {
    'user-agent': fake_useragent.UserAgent().chrome,
}

def save_url(url, file_name):
    print(f'Saving {file_name}')
    ufr = requests.get(url)
    type = '.' + url.split('.')[-1]
    #print(type)
    # print(type)
    # print(file_name)
    # sys.exit()
    try:
        with open(f'{TO_SAVE_DOCS}\{file_name}{type}',"wb") as file: #открываем файл для записи, в режиме wb
            file.write(ufr.content) #записываем содержимое в файл; как видите - content запроса
    except FileNotFoundError:
        print(f'ERROR SAVING')
        with open(DOCS_FILE, 'a', newline='') as doc_file:
            writer = csv.writer(doc_file, delimiter=';')
            items = [file_name.split('_')[0], f'{file_name}{type}', url, "3D Model"]
            writer.writerow(items)
        pass
    else:
        with open(DOCS_FILE, 'a', newline='') as doc_file:
            writer = csv.writer(doc_file, delimiter=';')
            items = [file_name.split('_')[0], f'{file_name}{type}', url]
            writer.writerow(items)
    
    print('Записан файл {}'.format(file_name))
    #logging.info('Записан файл {}_{} {}'.format(sap_code, file_name, url))

def save_to_csv(items):
    #print(f'Start saving process')
    titels = list(items[0].keys())
    with open(CSV_FILE, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for item in items:
            task =[]
            for i in range(len(titels)):
                if type(item[titels[i]]) == list:
                    task.append('; '.join(item[titels[i]]))
                else:
                    task.append(item[titels[i]])
            #task = [str(item[titels[i]]) for i in range(len(titels))]
            writer.writerow(task)
            #print(f'Saving {task[0]}')
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
    # try:
    #     a = soup.find('section', class_='tab__panel tab__panel--icon').find_all('a', class_='tab__icon')
    # except AttributeError:
    #     print(f'{url} dont have documents')
    #     pass
    # else:
    datas = []
    chapters = [i.get_text() for i in li]
    details = [i.get_text() for i in div]
    
    # print(files)
    datas.append({
        'Chapters': chapters,
        'Detail': details,
        'URL': url,
        #'Files': files,
    })
    save_to_csv(datas)

        # files = []
        # for i in a:
        #     files.append(
        #         i.get('href')
        #     )

        
        # for url in files:
        #     f_n = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        #     id = datas[0]['Chapters'][-1]
        #     file_name = id + '_' + f_n
        #     save_url(url, file_name)


def main():
    urls = read_csv(TO_URLS)
    for url in urls:
        get_content(url)

    # with Pool(cpu_count()) as p:
    #     p.map(get_content, urls)


if __name__ == '__main__':
    main()