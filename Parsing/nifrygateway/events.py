import sys
import requests
import random
from time import sleep
from datetime import datetime
import csv
import logging
from fake_useragent import UserAgent
from multiprocessing import Pool, cpu_count

logging.basicConfig(filename='Parsing\\nifrygateway\\logs_events.csv', level=logging.INFO)

OPEN_REQ = 'https://api.niftygateway.com//exhibition/open/'
EVENTS_REQ = 'https://api.niftygateway.com//market/nifty-history-by-type/'

EVENTS_CSV = 'Parsing\\nifrygateway\\events.csv'

HEADERS = {
    'user-agent': UserAgent().chrome
}

PROXIES = [
    '91.193.253.188:23500',
    '176.9.119.170:3128',
    '176.9.75.42:3128',
    '88.198.24.108:8080',
    '95.141.193.35:80',
    '176.9.75.42:8080',
    '95.141.193.14:80',
    '5.252.161.48:8080',
    '176.9.119.170:3128',
]


def save_csv(items, path, titels, encoding='utf-8'):
    with open(path, 'a', newline='', encoding=encoding) as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        #writer.writerow(titels)
        #print(titels)
        for item in items:
            task = [item[titels[i]] for i in range(len(titels))]
            writer.writerow(task)


def get_events(adress_and_type, start_page=1):
    proxy = random.choice(PROXIES)
    main_data = []
    adress = adress_and_type[0]
    nifty_type = adress_and_type[1]

    response = requests.post(EVENTS_REQ, proxies={'http': 'http://' + proxy}, data={
        "contractAddress": adress,
        "niftyType": nifty_type,
        "current":1,
        "size":10,
        "onlySales":"false",
    })
    if response.status_code != 200:
        data = response.json()
        t = int(data['detail'][-10]) + 1
        print(f'Засыпаем на {t} секунд')
        sleep(t)
        get_events([adress, nifty_type])
    else:
        data = response.json()

        total_pages = int(data['data']['meta']['page']['total_pages']) + 1
        print('Парсим {} {}. Всего страниц - {}'.format(adress, nifty_type, total_pages))
        logging.info('Парсим {} {}. Всего страниц - {}'.format(adress, nifty_type, total_pages))
        
        for page in range(start_page, total_pages):
            response = requests.post(EVENTS_REQ, data={
                "contractAddress":adress,
                "niftyType":nifty_type,
                "current":page,
                "size":10,
                "onlySales":"false"})
            logging.info(f'Response status: {response.status_code} for contractAddress: {adress} niftyType: {nifty_type} page: {page}')
            data = response.json()

            try:
                data_results = data['data']['results']
            except Exception as ex:
                t = int(data['detail'][-10]) + 1
                print(f'Засыпаем на {t} секунд')
                sleep(t)
                get_events([adress, nifty_type], start_page=page)
            else:
                for d in data_results:
                    #print(d, sep='\n')
                    action = d['Type']
                    id = d['id']
                    token_id = 'None'
                    time = 'None'
                    # user1 = 'None'
                    # user2 = 'None'
                    user1_id = 'None'
                    user2_id = 'None'
                    price = 'None'

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
                        #user1 = d['ListingUserProfile']['name']
                        #user2 = 'None'
                        user1_id = d['ListingUserProfile']['id']
                        price = d['OfferAmountInCents'] * 0.01
                    elif action == 'listing':
                        id = d['NiftyObject']['id']
                        token_id = d['NiftyObject']['tokenId']
                        #user1 = d['ListingUserProfile']['name']
                        #user2 = 'None'
                        user1_id = d['ListingUserProfile']['id']
                        price = d['ListingAmountInCents'] * 0.01
                    elif action == 'birth':
                        id = d['NiftyObject']['id']
                        token_id = d['NiftyObject']['tokenId']
                        #user1 = d['BirthingUserProfile']['name']
                        #user2 = 'None'
                        user1_id = d['BirthingUserProfile']['id']
                    elif action == 'withdrawal':
                        id = d['NiftyObject']['id']
                        token_id = d['NiftyObject']['tokenId']
                        #user1 = d['WithdrawingUserProfile']['name']
                        #user2 = 'None'
                        user1_id = d['WithdrawingUserProfile']['id']
                    elif action == 'nifty_transfer':
                        id = d['NiftyObject']['id']
                        token_id = d['NiftyObject']['tokenId']
                        #user1 = d['SendingUserProfile']['name']
                        #user2 = d['ReceivingUserProfile']['name']
                        user1_id = d['SendingUserProfile']['id']
                        user2_id = d['ReceivingUserProfile']['id']
                    elif action == 'sale':
                        id = d['NiftyObject']['id']
                        token_id = d['NiftyObject']['tokenId']
                        #user1 = d['SellingUserProfile']['name']
                        #user2 = d['PurchasingUserProfile']['name']
                        user1_id = d['SellingUserProfile']['id']
                        user2_id = d['PurchasingUserProfile']['id']
                        price = d['SaleAmountInCents'] * 0.01
                    elif action == 'bid':
                        #user1 = d['BiddingUserProfile']['name']
                        #user2 = 'None'
                        user1_id = d['BiddingUserProfile']['id']
                        price = d['BidAmountInCents'] * 0.01
                    else:
                        print(f'New action: {action}')
                        #print(d['BiddingUserProfile'])
                        #print(d['NiftyObject'])
                        id = 'None'
                        token_id = 'NEW ACTION' + action + adress + nifty_type
                        #user1 = 'None'
                        #user2 = 'None'
                        user1_id = 'None'
                        user2_id = 'None'
                        price = 'None'
                        logging.info('NEW ACTION {} - {} {}'.format(action, adress, nifty_type))


                    main_data.append({
                        'ID': id,
                        'Token ID': token_id,
                        'DateTime': time,
                        # 'User 1': user1,
                        # 'User 2': user2,
                        'User 1 ID': user1_id,
                        'User 2 ID': user2_id,
                        'Action': types[action],
                        'Price': str(price)
                    })
                    titels = list(main_data[0].keys())

        save_csv(main_data, EVENTS_CSV, titels)


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
                    'Edition Type': nifty['niftyDisplayImage'].split('.')[-1],
                    'Nifty Type': nifty['niftyType'],
                    'Edition Total Size': nifty['niftyTotalNumOfEditions'],
                    'Contract Address': nifty['niftyContractAddress'],
                }
            )
    return niftys

def get_html(url, params=''):
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data=response.json()
        return data
    except:
        print('Loadnig ERROR: {}'.format(response))

def main():
    start = datetime.now()
    logging.info(f'Start parsing events: {start}')

    # Парсим информацию по историям покупок - продаж
    items = get_html(OPEN_REQ)
    adress_and_type = get_first_edition(items)
    adress_and_type_to_parsing = []
    for item in adress_and_type:
        adress_and_type_to_parsing.append([item['Contract Address'], item['Nifty Type']])
    
    with Pool(cpu_count()) as p:
        p.map(get_events, adress_and_type_to_parsing)

    end = datetime.now()
    logging.info(f'Start parsing events: {end}')
    logging.info(f'Total execute time: {end - start}')


if __name__ == '__main__':
    main()