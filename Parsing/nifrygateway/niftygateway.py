import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

FIRST_CSV = 'editions.csv'
SEC_CSV = 'events.csv'

OPEN_REQ = 'https://api.niftygateway.com//exhibition/open/'
QUERY_REQ='https://api.niftygateway.com//already_minted_nifties/'

HEADERS = {
    'user-agent': UserAgent().chrome
}


def save_csv(items, path):
    pass
# Request URL: https://api.niftygateway.com//exhibition/open/
def get_html(url, params=''):
    response = requests.get(url, params=params)
    data=response.json()
    return data

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

        for item in items:
            datas.append(
                {
                    'Name': '',
                    'Description': '',
                    'Token_id_or_nifty_type': '',
                    'Contract_address': '',
                    'Name': '',
                }
            )
        print(items['data']['results'][1])

    #3LAU
    #print(datas, sep='\n')


#editions.csv
items_open = get_html(OPEN_REQ)
get_content(items_open, type='OPEN')

#events.csv
# items_query= get_html(QUERY_REQ)
# get_content(items_query, type='QUERY')