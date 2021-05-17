import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

EDITIONS_CSV = 'editions.csv'
EVENTS_CSV = 'events.csv'

OPEN_REQ = 'https://api.niftygateway.com//exhibition/open/'
QUERY_REQ= 'https://api.niftygateway.com//already_minted_nifties/?searchQuery=%3Fpage%3D3%26search%3D%26onSale%3Dfalse&page=%7B%22current%22:1,%22size%22:20%7D&filters=%7B%7D&sort=%7B%22_score%22:%22desc%22%7D'
HEADERS = {
    'user-agent': UserAgent().chrome
}


def save_csv(items, path):
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['Contract Address', 'Edition number', 'Token id', 'Owner_id'])
        for item in items:
            writer.writerow([item['Contract Address'], item['Edition number'], item['Token id'], item['Owner_id']])


def get_html(url, params=''):
    response = requests.get(url, params=params)
    data=response.json()
    return data

def get_total_pages():
    iquery= get_html(QUERY_REQ, params={'current':1})
    total_pages = iquery['data']['meta']['total_pages']
    return total_pages

def get_content(items, type=''):
    if type == 'OPEN':
        main_datas = []
        niftys = []
        for item in items:
            main_datas.append(
                {
                    'Artist': item['userProfile']['name'],
                    'Collection Name': item['storeName'],
                    'Collection Type': item['template'],
                    'Contract Address': item['contractAddress'],
                }
            )
        # проверяем данные
        # for data in main_datas:
        #     print(data, sep='\n')

        for item in items[0]['nifties']:
            niftys.append(
                {
                    'Edition Name': item['niftyTitle'],
                    'Edition Type': item['niftyType'],
                    'Edition Total Size': item['niftyTotalNumOfEditions'],
                    'Contract Address': item['niftyContractAddress'],
                }
            )

        # проверяем данные
        # for nift in niftys:
        #     print(nift, sep='\n')
        # for item in items[0]['nifties']:
        #     print(item['niftyTitle'])
        #print(items[0]['nifties'])

    elif type == 'QUERY':
        datas = []
        for item in items['data']['results']:
            # Выдергиваем число между # и / - есть не во всех названиях
            ed_number = item['name'][item['name'].find('#'):item['name'].find('/')]
            datas.append(
                {
                    'Contract Address': item['contract_address'],
                    'Edition number': item['name'],
                    'Token id': item['token_id_or_nifty_type'],
                    'Owner_id': item['owner_profile_id'],
                }
            )
    return datas

        # проверяем данные
        # for item in items['data']['results']:
        #     print(item)
        #     for i in item:
        #         print(i)

        # for item in sub_datas:
        #     print(item)

    #print(datas, sep='\n')


# items_open = get_html(OPEN_REQ)
# get_content(items_open, type='OPEN')

#editions.csv
def editions():
    datas = []
    total_pages = get_total_pages()
    print(f'Всего страниц {total_pages}')
    for page in range(1, total_pages):
        print(f'Парсим страницу {page}')
        items_query= get_html(QUERY_REQ, params={'current':page})
        datas.extend(get_content(items_query, type='QUERY'))
        save_csv(datas, EDITIONS_CSV)

editions()