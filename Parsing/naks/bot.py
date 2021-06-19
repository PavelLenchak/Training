import config
import naks_parser
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode


#bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


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


@dp.message_handler()
async def parse(message: types.Message):
	mark = message.text
	await message.answer(f'Пожалуйста подождите, ищу информацию по "{mark}"')

	chrome_options = Options()
	chrome_options.add_argument("--headless")

	driver = webdriver.Chrome(options=chrome_options)
	driver.get("http://www.naks.ru/assp/reestrperson/")

	filter_naks(driver, type='clear')
	set_value(driver, 'arrFilter_ff[CODE]', mark)
	filter_naks(driver, type='set')

	try:
		all_elements = driver.find_element_by_tag_name('strong').text
		number_of_people = int(all_elements[-1])
		await message.answer(f'Всего найдено элементов {number_of_people}')
    
	except ValueError as ve:
		await message.answer(f'Записей по "{mark}" не найдено')
		driver.close()
		driver.quit()
    
	else:
		table = driver.find_element_by_class_name('tabl').find_element_by_tag_name('tbody')
		elems = table.find_elements_by_tag_name('tr')

		welders = {}

		count = 1
		for e in elems[2:]:
			items = e.text.split('   ')
			name = f'{count}. {str(items[0].split("  ")[0])}'
			mark = str(items[0].split('  ')[-1])

			welders[name] = {
				'fio': items[0].split("  ")[0],
				'mark': mark,
				'org': items[1],
				'post': items[2],
				'number_of_card': items[3],
				'add_att': items[4],
				'AЦ': items[5],
				'AП': items[6],
				'date_arr': items[7],
				'deadline': items[8],
				'extend_date': items[9],
				'type_of_activity': items[10],
				'are_att': items[11].replace('  подробнее', ''),
			}
			count += 1

		for key, v in welders.items():
			welder = f'{key} \n\n' \
					f'Место работы: {v["org"]} \n' \
					f'Должность (Специальность): {v["post"]} \n' \
					f'Номер удостоверения: {v["number_of_card"]} \n\n' \
					f'Дата аттестации: {v["date_arr"]} \n' \
					f'Окончание срока действия удостоверения: {v["deadline"]} \n' \
					f'Cрок продления: {v["extend_date"]} \n\n' \
					f'Вид деятельности: {v["type_of_activity"]} \n' \
					f'Область аттестации: {v["are_att"]} \n' \
			
			await message.answer(welder)
		driver.close()
		driver.quit()


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)