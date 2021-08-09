import requests
from bs4 import BeautifulSoup
from time import sleep

from requests.api import head

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.135 Safari/537.36',

}

def try_request(url, retry=5):
    try:
        response = requests.get(url,  headers=HEADERS)
        print(f'[+] {url} {response.status_code}')
    except Exception as ex:
        if retry:
            print(f'[INFO]: retry -> {retry} --- {url}')
            return try_request(url, retry = retry-1)
        else:
            raise
    else:
        return response
    
def main():
    with open('Parsing\\books_urls.txt', 'r') as file:
            urls = file.read().splitlines()

    for url in urls:
        r = try_request(url)
        

        sleep(1)


if __name__ == '__main__':
    main()