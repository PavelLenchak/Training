import sys
import requests

OPEN_REQ = 'https://api.niftygateway.com//exhibition/open/'
EVENTS_REQ = 'https://api.niftygateway.com//market/nifty-history-by-type/'

response = requests.post(EVENTS_REQ, data={
            "contractAddress": '0x3f133816f8178b93ac991a2c3eeddb8f947af0cb',
            "niftyType": 12,
            "current": 1,
            "size":10,
            "onlySales":"false"})
print(response.status_code)
data = response.json()
print(data)

total_pages = data['data']['meta']['page']['total_pages'] + 1
print(total_pages)
