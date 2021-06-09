import json
import os, pathlib
from datetime import datetime as dt
import sys, operator

MAIN_PATH = pathlib.Path(__file__).parent

file_name = os.path.join(MAIN_PATH, 'operations.json')

with open(file_name, encoding='utf-8') as f:
    datas = json.load(f)

datas[:] = [d for d in datas if d.get('date')]
datas.sort(key = lambda x: dt.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'))

def mask(s, type = 'card'):
    if type == 'card':
        return s[:4] + ' **** **** ' + s[-4:]
    else:
        return '**' + s[-4:]

datas_to_print = []
for item in datas[::-1]:
    try:
        state = item['state']
        if state == 'EXECUTED' and len(datas_to_print) < 5:
            d = dt.strptime(item['date'], '%Y-%m-%dT%H:%M:%S.%f').date()
            date = dt.strftime(d, '%d.%m.%Y')

            item_to = item["to"].split(' ')
            if item_to[0] != 'Счет':
                item_to = ' '.join(item_to[:-1]) + ' ' + mask(item_to[-1])
            else:
                item_to = ' '.join(item_to[:-1]) + ' ' + mask(item_to[-1], type='account')
            
            try:
                item_from = item['from'].split(' ')
                if item_from[0] != 'Счет':
                    item_from = ' '.join(item_from[:-1]) + ' ' + mask(item_from[-1])
                else:
                    item_from = ' '.join(item_from[:-1]) + ' ' + mask(item_from[-1], type='account')
            except Exception as ex:
                datas_to_print.append({
                    'Date - Description': f'{date} {item["description"]}',
                    'To - From': f'{item_to}',
                    'Amount': f'{item["operationAmount"]["amount"]} {item["operationAmount"]["currency"]["name"]}'
                })
            else:
                datas_to_print.append({
                    'Date - Description': f'{date} {item["description"]}',
                    'To - From': f'{item_from} -> {item_to}',
                    'Amount': f'{item["operationAmount"]["amount"]} {item["operationAmount"]["currency"]["name"]}'
                })
    except Exception as exept:
        pass

for data in datas_to_print:
    print(data['Date - Description'], data['To - From'], data['Amount'], sep='\n', end='\n\n')

