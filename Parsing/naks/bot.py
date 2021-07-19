# - *- coding: utf- 8 - *-

import config
from selenium import webdriver
import time
import telebot
from fake_useragent import UserAgent

#bot init
client = telebot.TeleBot(config.TOKEN)

def filter_naks(driver, type):
	print('Click on botton "{}"'.format(type))
	time.sleep(2)
	if type == 'set':
		# set_filter = driver.find_element_by_name('set_filter')
		set_filter = driver.find_element_by_xpath('//*[@id="mm"]/div/div[2]/div/div[2]/form/table/tbody/tr/td[1]/table/tbody/tr[5]/td/font/input[1]')
		set_filter.click()
	elif type == 'clear':
		# del_filter = driver.find_element_by_name('del_filter')
		del_filter = driver.find_element_by_xpath('//*[@id="mm"]/div/div[2]/div/div[2]/form/table/tbody/tr/td[1]/table/tbody/tr[5]/td/font/input[3]')
		del_filter.click()
	time.sleep(2)


def set_value(driver, elem_name, value):
	time.sleep(2)
	print('Set value {} on {}'.format(value, elem_name))
	elem = driver.find_element_by_name(elem_name)
	driver.execute_script("arguments[0].setAttribute('value','{}')".format(value), elem)
	time.sleep(2)


webdriver.ChromeOptions()

@client.message_handler(content_types = ['text'])
def parse(message):
	mark = message.text
	chat_id = message.chat.id
	if len(mark) < 4:
		client.send_message(chat_id,f'Пожалуйста, введите кооректное значение. (Например: 9LMH)')
	else:
		client.send_message(chat_id,f'Пожалуйста подождите, ищу информацию по "{mark}"')

		try:
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_argument("--headless")
			chrome_options.add_argument("--disable-gpu")
			chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 YaBrowser/21.5.3.742 Yowser/2.5 Safari/537.36")

			driver = webdriver.Chrome(options=chrome_options)
			driver.get("http://www.naks.ru/assp/reestrperson/")
			print("Page title was '{}'".format(driver.title))

			filter_naks(driver, type='clear')
			set_value(driver, 'arrFilter_ff[CODE]', mark)
			filter_naks(driver, type='set')

			time.sleep(2)
			all_elements = driver.find_element_by_tag_name('strong').text
			number_of_people = int(all_elements[-1])
			client.send_message(chat_id,f'Всего найдено элементов {number_of_people}')
	    
		except Exception as ex:
			print('Error: {}'.format(ex))
			client.send_message(chat_id,f'Записей по "{mark}" не найдено')
	    
		else:
			print('Website is correct')
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
				
				client.send_message(chat_id, welder)

		finally:
			driver.quit()


if __name__ == '__main__':
	print('Bot have been start')
	client.polling(none_stop = True, interval = 0)