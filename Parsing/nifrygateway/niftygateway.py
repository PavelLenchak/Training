import sys
import datetime
import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

EDITIONS_F_CSV = 'Parsing\\nifrygateway\\editions_first.csv'
EDITIONS_S_CSV = 'Parsing\\nifrygateway\\editions_second.csv'
EVENTS_CSV = 'Parsing\\nifrygateway\\events.csv'

OPEN_REQ = 'https://api.niftygateway.com//exhibition/open/'
QUERY_REQ= 'https://api.niftygateway.com//already_minted_nifties/?searchQuery=%3Fpage%3D3%26search%3D%26onSale%3Dfalse&page=%7B%22current%22:1,%22size%22:20%7D&filters=%7B%7D&sort=%7B%22_score%22:%22desc%22%7D'
NIFTY_REQ ='https://api.niftygateway.com//market/nifty-history-by-type/'

#   https://api.niftygateway.com//market/nifty-history-by-type/
test = 'https://niftygateway.com/itemdetail/secondary/0x68c4dd3f302c449be39af528d56c6bd242b8cedb/23600030038'

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

        
def get_sec_edition(items):
    datas = []
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
    # проверяем данные
    # for item in items['data']['results']:
    #     print(item)
    #     for i in item:
    #         print(i)

    return datas

def save_csv(items, path, titels):
    with open(path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(titels)
        for item in items:
            task = [item[titels[i]] for i in range(len(titels))]
            writer.writerow(task)


def edition_first():
    print('start EDITION FIRST')
    datas = []
    items = get_html(OPEN_REQ)
    datas.extend(get_first_edition(items))
    titels = list(datas[0].keys())
    save_csv(datas, EDITIONS_F_CSV, titels)


#editions.csv
def editions_second():
    print('start EDITION SECOND')
    datas = []
    total_pages = get_total_pages()
    print(f'Всего страниц {total_pages}')
    for page in range(1, total_pages+1):
        print(f'Парсим страницу {page}')
        items_query= get_html(QUERY_REQ, params={'current':page})
        datas.extend(get_sec_edition(items_query))
        titels = list(datas[0].keys())
        save_csv(datas, EDITIONS_S_CSV, titels)

def events():
    print('start EVENTS')
    events_request = 'https://api.niftygateway.com//market/nifty-history-by-type/'
    main_data = []

    items = get_html(OPEN_REQ)
    adress_and_type = get_first_edition(items)
    print(adress_and_type[0])

    for at in adress_and_type:
        print('Парсим {}'.format(at['Contract Address']))
        response = requests.post(events_request, data={
            "contractAddress": at['Contract Address'],
            "niftyType": at['Edition Type'],
            "current":1,
            "size":10,
            "onlySales":"false",
        })
        data = response.json()

        total_pages = data['data']['meta']['page']['total_pages']
        print(f'Всего страниц {total_pages}')
        for page in range(1, total_pages+1):
            print(f'Парсим {page} страницу')
            response = requests.post(events_request, data={
                "contractAddress":"0x68c4dd3f302c449be39af528d56c6bd242b8cedb",
                "niftyType":3,
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
                }
                
                # TYPES
                # listing - put
                # birth - has been deposited into Nifty Gateway by
                # offer - made a global offer for
                # withdrawal - withdrew
                # nifty_transfer - sent
                # sale - bought

                #2013-07-12T07:00:00Z datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
                r_time = d['Timestamp'].replace('T', ' ').replace('Z', '')
                time = datetime.datetime.strptime(r_time, '%Y-%m-%d %H:%M:%S.%f')
                
                if action == 'offer':
                    id = d['id']
                    token_id = d['UnmintedNiftyObj']['niftyTitle']
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
                else:
                    print(action)
                    id = d['NiftyObject']['id']
                    token_id = d['NiftyObject']['tokenId']
                    user1 = d['ListingUserProfile']['name']
                    user2 = 'None'
                    user1_id = d['ListingUserProfile']['id']
                    user2_id = 'None'
                    price = d['ListingAmountInCents'] * 0.01

                main_data.append({
                    'ID': id,
                    'Token ID': token_id,
                    'DateTime': time,
                    'User 1': user1,
                    'User 2': user2,
                    'User 1 ID': user1_id,
                    'User 2 ID': user2_id,
                    'Action': types[action],
                    'Price': price
                })
                titels = list(main_data[0].keys())
                save_csv(main_data, EVENTS_CSV, titels)
        
        # for i in main_data:
        #     print(i)

        # for key, value in data['data']['results'][0].items():
        #     print(f'{key}: {value}')

def main():
    edition_first()
    editions_second()
    events()
    print('END')

if __name__ == '__main__':
    main()