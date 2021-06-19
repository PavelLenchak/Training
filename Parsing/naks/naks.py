import selenium
from selenium import webdriver
import pathlib
import time



MAIN_PATH = pathlib.Path(__file__).parent
URL_TO_PARSE = 'http://www.naks.ru/assp/reestrperson/'
HOST = 'http://www.naks.ru'

TEST_MARK = '9LMH'

def filter_naks(driver, type):
    time.sleep(2)
    if type == 'set':
        set_filter = driver.find_element_by_name('set_filter')
        set_filter.click()
    elif type == 'clear':
        del_filter = driver.find_element_by_name('del_filter')
        del_filter.click()
    time.sleep(2)


def set_value(driver, elem_name, value):
    elem = driver.find_element_by_name(elem_name)
    driver.execute_script("arguments[0].setAttribute('value','{}')".format(value), elem)


def main():
    pass


if __name__ == '__main__':
    driver = webdriver.Ie()
    driver.get(URL_TO_PARSE)

    filter_naks(driver, type='clear')
    set_value(driver, 'arrFilter_ff[CODE]', TEST_MARK)
    filter_naks(driver, type='set')

    all_elements = driver.find_element_by_tag_name('strong').text
    number_of_people = int(all_elements[-1])
    print(f'Всего найдено элементов {number_of_people}')

    table_headers = (
        'Фамилия, имя, отчество',
        'Шифр клейма',
        'Место работы (Организация)',
        'Должность (Специальность)',
        'Номер удостоверения',
        'Доп. Aтт.',
        'Место аттестации',
        'Дата аттестации',
        'Окончание срока действия удостоверения',
        'Cрок продления',
        'Вид деятельности',
        'Область аттестации',
        'Шифр АЦ - Уровень - Номер',
        'AЦ',
        'AП',
    )

    table = driver.find_element_by_class_name('tabl').find_element_by_tag_name('tbody')
    # elems = table.find_elements_by_tag_name('td')
    elems = table.find_elements_by_tag_name('tr')

    welders = {}

    count = 1
    for e in elems[2:]:
        items = e.text.split('   ')
        name = str(items[0].split('  ')[:-1])
        mark = str(items[0].split('  ')[-1])

        welders[name] = {
            'Шифр клейма': mark,
            'Место работы (Организация)': items[1],
            'Должность (Специальность)': items[2],
            'Номер удостоверения': items[3],
            'Доп. Aтт.': items[4],
            'AЦ': items[5],
            'AП': items[6],
            'Дата аттестации': items[7],
            'Окончание срока действия удостоверения': items[8],
            'Cрок продления': items[9],
            'Вид деятельности': items[10],
            'Область аттестации': items[11].replae('  подробнее', ''),
        }
    print(welders)