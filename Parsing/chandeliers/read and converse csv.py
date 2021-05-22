import csv
import codecs
from datetime import date, datetime

FILE_TO_READ = 'Parsing\\chandeliers\\files\\products.csv'

def save_to_csv(path, item):
    with open('Parsing\\chandeliers\\files\\urls.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow([item])

def read_csv(path):
    urls = []
    with codecs.open(path, 'r', encoding='utf-32') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for row in csv_reader:
            print(len(row))
            # url = row[0].replace(',', '.')
            # urls.append(url)
            # save_to_csv('Parsing\\chandeliers\\files\\urls.csv',url)
    # return urls


def main():
    print('Script starting')
    start = datetime.now()
    read_csv(FILE_TO_READ)
    end = datetime.now()
    print(f'Script have done. Time passed:{end-start}')

if __name__ == '__main__':
    main()