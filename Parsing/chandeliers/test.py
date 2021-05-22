from os import listdir
from os.path import isfile
from os.path import join as joinpath
import csv
from progress.bar import IncrementalBar

CSV_FILE = 'Parsing\\chandeliers\\files_name.csv'
def save_to_scv(item):
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(item)

mypath = "D:\\Python\\docs"
bar = IncrementalBar('Progress', max = len(listdir(mypath)))
for i in listdir(mypath):
    if isfile(joinpath(mypath,i)):
        bar.next()
        save_to_scv([i])