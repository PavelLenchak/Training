import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

EDITIONS_F_CSV = 'editions_first.csv'
EDITIONS_S_CSV = 'editions_second.csv'
NIFTY = 'nifty.csv'
EVENTS_CSV = 'events.csv'

OPEN_REQ = 'https://api.niftygateway.com//exhibition/open/'
QUERY_REQ= 'https://api.niftygateway.com//already_minted_nifties/?searchQuery=%3Fpage%3D3%26search%3D%26onSale%3Dfalse&page=%7B%22current%22:1,%22size%22:20%7D&filters=%7B%7D&sort=%7B%22_score%22:%22desc%22%7D'
NIFTY_REQ ='https://api.niftygateway.com//market/nifty-history-by-type/'
HEADERS = {
    'user-agent': UserAgent().chrome
}


def get_html(url, params=''):
    response = requests.get(url, params=params)
    data=response.json()
    return data


def get_total_pages():
    iquery= get_html(QUERY_REQ, params={'current':1})
    total_pages = iquery['data']['meta']['total_pages']
    return total_pages


def get_first_edition(items):
    main_datas = []
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
    return main_datas


def get_niftys(items):
    niftys = []
    for item in items[0]['nifties']:
        niftys.append(
            {
                'Edition Name': item['niftyTitle'],
                'Edition Type': item['niftyType'],
                'Edition Total Size': item['niftyTotalNumOfEditions'],
                'Contract Address': item['niftyContractAddress'],
            }
        )
    #проверяем данные
    for nift in niftys:
        print(nift, sep='\n')
    # for item in items[0]['nifties']:
    #     print(item['niftyTitle'])
    #print(items[0]['nifties'])
    #return niftys

        
def get_sec_edition(items):
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
    # проверяем данные
    # for item in items['data']['results']:
    #     print(item)
    #     for i in item:
    #         print(i)

    # for item in sub_datas:
    #     print(item)
    return datas

def save_csv(items, path, titels):
    with open(path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(titels)
        for item in items:
            writer.writerow([
                item[titels[0]], 
                item[titels[1]], 
                item[titels[2]], 
                item[titels[3]]
                ])

def edition_first():
    titels = [
        'Artist', 
        'Collection Name', 
        'Collection Type', 
        'Contract Address']
    datas = []
    items = get_html(OPEN_REQ)
    datas.extend(get_first_edition(items))
    save_csv(datas, EDITIONS_F_CSV, titels)


def niftys():
    titels = [
        'Edition Name', 
        'Edition Type', 
        'Edition Total Size', 
        'Contract Address']
    datas = []
    items = get_html(OPEN_REQ)
    datas.extend(get_niftys(items))
    save_csv(datas, NIFTY, titels)


#editions.csv
def editions_second():
    # Заголовки столбцов
    titels = [
        'Contract Address', 
        'Edition number', 
        'Token id', 
        'Owner_id']

    datas = []
    total_pages = get_total_pages()
    print(f'Всего страниц {total_pages}')
    for page in range(1, 4):
        print(f'Парсим страницу {page}')
        items_query= get_html(QUERY_REQ, params={'current':page})
        datas.extend(get_sec_edition(items_query))
        save_csv(datas, EDITIONS_S_CSV, titels)

def main():
    # print('start EDITION FIRST')
    # edition_first()

    print('start EVENTS')
    niftys()

    # print('start EDITION SECOND')
    # editions_second()
    # print('END')

main()