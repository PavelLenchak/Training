import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
from selenium import webdriver

FIRST_CSV = 'editions.csv'
SEC_CSV = 'events.csv'
HOST = 'https://niftygateway.com'
URL = 'https://niftygateway.com/marketplace'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36',
    #'user-agent': UserAgent().chrome
}

# <div class="MuiCollapse-wrapperInner"><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">The Array Collection by SSX3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">Gunky's Uprising by SSX3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">Throwing Shapes Open Edition by SSX3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">Throwing Shapes by SSX3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">Everything Canvas by 3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">Everything by 3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">Everything Audio by 3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">IRIDESCENT Open Edition by SSX3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">IRIDESCENT by SSX3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">Glass by SSX3LAU<span class="MuiTouchRipple-root"></span></div><div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">The Next Album by 3LAU<span class="MuiTouchRipple-root"></span></div></div>


def save_csv(items, path):
    pass

def get_html(url, params=''):
    driver = webdriver.PhantomJS()
    driver.get(url)
    p_element = driver.find_element_by_class_name(id_='MuiCollapse-wrapperInner')
    print(p_element.text)
    # response = requests.get(url, headers=HEADERS, params=params)
    # return response

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='MuiCollapse-wrapperInner')
    print(html)
    print(items)

def main():
    pass

html = get_html(URL)
# print(html)
# get_content(html.text)