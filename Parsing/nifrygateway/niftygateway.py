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
    'user-agent': UserAgent().chrome
}

# <div class="MuiButtonBase-root MuiListItem-root MuiListItem-gutters MuiListItem-button" tabindex="0" role="button" aria-disabled="false">The Array Collection by SSX3LAU<span class="MuiTouchRipple-root"></span></div>
def save_csv(items, path):
    pass
# MuiCollapse-container MuiCollapse-entered
def get_html(url, params=''):
    driver = webdriver.PhantomJS()
    driver.get(url)
    p_element = driver.find_elements_by_class_name("MuiCollapse-container")
    print(p_element)
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