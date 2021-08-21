import requests
from bs4 import BeautifulSoup
from requests.api import head

URL_TO_PARSE = 'https://www.landingfolio.com/?offset=12'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaBrowser/21.6.4.693 Yowser/2.5 Safari/537.36'
}

def get_html(url):
    try:
        response = requests.get(url=url, headers=HEADERS)
        return response
    except Exception as ex:
        print('[ERROR]: no access to the site')


def main():
    r = get_html(URL_TO_PARSE).text
    print(r)


if __name__ == '__main__':
    main()