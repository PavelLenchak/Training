import sys

test = 'https://api.niftygateway.com//already_minted_nifties/?searchQuery=%3Fpage%3D3%26search%3D%26onSale%3Dfalse&page=%7B%22current%22:{i},%22size%22:20%7D&filters=%7B%7D&sort=%7B%22_score%22:%22desc%22%7D'
print(test[test.find(':',test.find('current')):test.find(',%22size')])
print(test.split('%'))
