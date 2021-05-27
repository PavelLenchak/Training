
# niftygateway.py

"""
    Парсинг сайта https://niftygateway.com/marketplace
    Используются библиотеки requests, bs4, csv
    Собираем информацию через запросы requests.get ... requests.post
"""

import sys
from time import sleep
from datetime import datetime
import requests
import csv
from fake_useragent import UserAgent
from multiprocessing import Pool
from multiprocessing import cpu_count
import logging
import traceback
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',
    level=logging.DEBUG,
    datefmt='%H:%M:%S',
    stream=sys.stderr
)
logger = logging.getLogger('niftygateway')
logging.getLogger('chardet.charsetprober').disabled =True


EDITIONS_F_CSV = 'Parsing\\nifrygateway\\editions_first.csv'
EDITIONS_S_CSV = 'Parsing\\nifrygateway\\editions_second.csv'
EVENTS_CSV = 'Parsing\\nifrygateway\\events.csv'

OPEN_REQ = 'https://api.niftygateway.com//exhibition/open/'
QUERY_REQ= 'https://api.niftygateway.com//already_minted_nifties/?searchQuery=%3Fpage%3D3%26search%3D%26onSale%3Dfalse&page=%7B%22current%22:1,%22size%22:20%7D&filters=%7B%7D&sort=%7B%22_score%22:%22desc%22%7D'
NIFTY_REQ ='https://api.niftygateway.com//market/nifty-history-by-type/'
EVENTS_REQ = 'https://api.niftygateway.com//market/nifty-history-by-type/'

#   https://api.niftygateway.com//market/nifty-history-by-type/
test = 'https://niftygateway.com/itemdetail/secondary/0x68c4dd3f302c449be39af528d56c6bd242b8cedb/23600030038'
logging.basicConfig(filename='Parsing\\nifrygateway\\logs.csv', level=logging.INFO)

HEADERS = {
    'user-agent': UserAgent().chrome
}


def get_total_pages():
    iquery= get_html(QUERY_REQ, params={'current':1})
    total_pages = iquery['data']['meta']['total_pages']
    return total_pages


def save_csv(items, path, titels):
    # a - append для возможности многопроцессорности
    with open(path, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        #writer.writerow(titels)
        #print(titels)
        for item in items:
            task = [item[titels[i]] for i in range(len(titels))]
            writer.writerow(task)


def get_html(url, params=''):
    try:
        response = requests.get(url, params=params)
        data=response.json()
        return data
    except:
        print('Loadnig ERROR: {}'.format(response))
        sys.exit()


def get_first_edition(items):
    niftys = []
    for item in items:
        for nifty in item['nifties']:
            niftys.append(
                {
                    'Artist': item['userProfile']['name'],
                    'Collection Name': item['storeName'],
                    'Collection Type': item['template'],
                    'Edition Name': nifty['niftyTitle'],
                    'Edition Type': nifty['niftyType'],
                    'Edition Total Size': nifty['niftyTotalNumOfEditions'],
                    'Contract Address': nifty['niftyContractAddress'],
                }
            )

    #проверяем данные
    # for nift in niftys:
    #     print(nift, sep='\n')
    # for item in items[0]['nifties']:
    #     print(item['niftyTitle'])
    return niftys

        
def get_sec_edition(items, page):
    datas = []
    print('Scrapping #{}'.format(page))
    try:
        for item in items['data']['results']:
            # Выдергиваем число между # и / - есть не во всех названиях
            ed_number = item['name'][item['name'].find('#'):item['name'].find('/')]
            datas.append(
                {
                    'Collection name': item['project_name'],
                    'Contract Address': item['contract_address'],
                    'Edition number': item['name'],
                    'Token id': item['token_id_or_nifty_type'],
                    'Owner_id': item['owner_profile_id'],
                }
            )
    except KeyError:
        print('KeyError {} {}'.format(page, items))
    # проверяем данные
    # for item in items['data']['results']:
    #     print(item)
    #     for i in item:
    #         print(i)
    logging.info("Done page - {}".format(page))
    return datas


def edition_first():
    print('start EDITION FIRST')
    datas = []
    items = get_html(OPEN_REQ)
    datas.extend(get_first_edition(items))
    titels = list(datas[0].keys())
    save_csv(datas, EDITIONS_F_CSV, titels)


def editions_second(page):
    datas = []
    try:
        items_query= get_html(QUERY_REQ, params={'current':page})
        datas.extend(get_sec_edition(items_query, page))
        titels = list(datas[0].keys())
        save_csv(datas, EDITIONS_S_CSV, titels)
    except IndexError:
        #print('ERROR {} - {}'.format(datas, page))
        logging.info("INDEX ERROR - {}".format(page))
    except Exception:
        detail = items_query['detail']
        if 'Request was throttled.' in detail:
            t = int(detail[-10])
            print(t)
            sleep(t)
            items_query= get_html(QUERY_REQ, params={'current':page})
            datas.extend(get_sec_edition(items_query, page))
            titels = list(datas[0].keys())
            save_csv(datas, EDITIONS_S_CSV, titels)
        
        

def events(adress_and_type):
    main_data = []
    adress = adress_and_type[0]
    nifty_type = adress_and_type[1]

    response = requests.post(EVENTS_REQ, data={
        "contractAddress": adress,
        "niftyType": nifty_type,
        "current":1,
        "size":10,
        "onlySales":"false",
    })
    data = response.json()

    try:
        total_pages = data['data']['meta']['page']['total_pages'] + 1
        print('Парсим {} {}. Всего страниц - {}'.format(adress, nifty_type, total_pages))
        for page in range(1, total_pages):
            response = requests.post(EVENTS_REQ, data={
                "contractAddress":adress,
                "niftyType":nifty_type,
                "current":page,
                "size":10,
                "onlySales":"false"})
            data = response.json()
            
            for d in data['data']['results']:
                #print(d, sep='\n')
                action = d['Type']
                time = ''
                user1 = ''
                user2 = ''
                user1_id = ''
                user2_id = ''
                price = ''

                types = {
                    'listing': 'put',
                    'birth': 'has been deposited into Nifty Gateway by',
                    'offer': 'made a global offer for',
                    'withdrawal': 'withdrew',
                    'nifty_transfer': 'sent',
                    'sale': 'bought',
                    'bid': 'put on sale',
                }

                #2013-07-12T07:00:00Z datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
                r_time = d['Timestamp'].replace('T', ' ').replace('Z', '')
                time = datetime.strptime(r_time, '%Y-%m-%d %H:%M:%S.%f')
                
                if action == 'offer':
                    id = d['id'] #d['UnmintedNiftyObj']['niftyTitle'] #'None'
                    token_id = 'None'
                    user1 = d['ListingUserProfile']['name']
                    user2 = 'None'
                    user1_id = d['ListingUserProfile']['id']
                    user2_id = 'None'
                    price = d['OfferAmountInCents'] * 0.01
                elif action == 'listing':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    user1 = d['ListingUserProfile']['name']
                    user2 = 'None'
                    user1_id = d['ListingUserProfile']['id']
                    user2_id = 'None'
                    price = d['ListingAmountInCents'] * 0.01
                elif action == 'birth':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    user1 = d['BirthingUserProfile']['name']
                    user2 = 'None'
                    user1_id = d['BirthingUserProfile']['id']
                    user2_id = 'None'
                    price = 'None'
                elif action == 'withdrawal':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    user1 = d['WithdrawingUserProfile']['name']
                    user2 = 'None'
                    user1_id = d['WithdrawingUserProfile']['id']
                    user2_id = 'None'
                    price = 'None'
                elif action == 'nifty_transfer':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    user1 = d['SendingUserProfile']['name']
                    user2 = d['ReceivingUserProfile']['name']
                    user1_id = d['SendingUserProfile']['id']
                    user2_id = d['ReceivingUserProfile']['id']
                    price = 'None'
                elif action == 'sale':
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    user1 = d['SellingUserProfile']['name']
                    user2 = d['PurchasingUserProfile']['name']
                    user1_id = d['SellingUserProfile']['id']
                    user2_id = d['PurchasingUserProfile']['id']
                    price = d['SaleAmountInCents'] * 0.01
                elif action == 'bid':
                    id = d['id']
                    token_id = 'None'
                    user1 = d['BiddingUserProfile']['name']
                    user2 = 'None'
                    user1_id = d['BiddingUserProfile']['id']
                    user2_id = 'None'
                    price = d['BidAmountInCents'] * 0.01
                else:
                    print(action)
                    #print(d['BiddingUserProfile'])
                    #print(d['NiftyObject'])
                    id = 'None'
                    token_id = 'NEW ACTION' + action + adress + nifty_type
                    user1 = 'None'
                    user2 = 'None'
                    user1_id = 'None'
                    user2_id = 'None'
                    price = 'None'
                    logging.info('NEW ACTION {} - {} {}'.format(action, adress, nifty_type))


                main_data.append({
                    'ID': id,
                    'Token ID': token_id,
                    'DateTime': time,
                    'User 1': user1,
                    'User 2': user2,
                    'User 1 ID': user1_id,
                    'User 2 ID': user2_id,
                    'Action': types[action],
                    'Price': str(price)
                })
                titels = list(main_data[0].keys())
    except Exception:
        #print(data)
        logging.info('Ошибка на странице {} - {} {}'.format(page, adress, nifty_type))

    
    save_csv(main_data, EVENTS_CSV, titels)
        
        # for i in main_data:
        #     print(i)

        # for key, value in data['data']['results'][0].items():
        #     print(f'{key}: {value}')

def parse(url):
    try:
        html = get_html(url)
    except Exception as e:
        logger.exception(
            'http exeption for %s [%s]: %s',
            url,
            getattr(e, 'status', None),
            getattr(e, 'message', None)
        )
    else:
        return html


def save_file(url, file_path):
    items = parse(url=url)
    if not items:
        return None
    else:
        titels = list(items[0].keys())
        with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            #writer.writerow(titels)
            #print(titels)
            for item in items:
                task = [item[titels[i]] for i in range(len(titels))]
                writer.writerow(task)
    


def main():
    logging.info("Program started")
    start = datetime.now()

    save_file(OPEN_REQ, EDITIONS_F_CSV)

    # editins_first.csv
    #edition_first()

    # editions_second.csv
    # tp = get_total_pages()
    # total_pages = list(range(1, tp+1))
    # logging.info("Total pages {}".format(tp))
    # #total_pages = list(range(1,11))
    # with Pool(50) as p:
    #     p.map(editions_second, total_pages)

    # events.csv
    items = get_html(OPEN_REQ)
    adress_and_type = get_first_edition(items)
    adress_and_type_to_parsing = []
    for item in adress_and_type:
        adress_and_type_to_parsing.append([item['Contract Address'], item['Edition Type']])
    
    with Pool(5) as p:
        p.map(events, adress_and_type_to_parsing)

    end = datetime.now()
    total = end - start
    print('Total time: {}'.format(str(total)))
    logging.info("Program end. Total time - {}".format(total))

if __name__ == '__main__':
    main()