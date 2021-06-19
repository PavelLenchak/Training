import selenium
from selenium import webdriver
import pathlib
import time



MAIN_PATH = pathlib.Path(__file__).parent
URL_TO_PARSE = 'http://www.naks.ru/assp/reestrperson/'
HOST = 'http://www.naks.ru'

TEST_MARK = 'Привет'

def filter_naks(driver, type):
    time.sleep(2)
    if type == 'set':
        set_filter = driver.find_element_by_name('set_filter')
        set_filter.send_keys(selenium.webdriver.common.keys.Keys.SPACE)
    elif type == 'clear':
        del_filter = driver.find_element_by_name('del_filter')
        del_filter.send_keys(selenium.webdriver.common.keys.Keys.SPACE)
    time.sleep(2)


def main():
    pass


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(URL_TO_PARSE)

    filter_naks(driver, type='clear')

    mark_filter = driver.find_element_by_name('arrFilter_ff[CODE]')
    mark_filter.send_keys = 'TEST_MARK'

    filter_naks(driver, type='set')