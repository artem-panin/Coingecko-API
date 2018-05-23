#Code to add a path to System path in order to import other files from the coingecko folder.
import sys
sys.path.append(r'H:/Data_Science/Python/coingecko')

import coingecko_api as coin #Import API call code.
import json
import datetime


def main():
	coinList = coin.CoingeckoAPI('https://api.coingecko.com/api/v3/coins/list')
	#Getting a JSOn with the data requested.
	list = coinList.get_coingecko_data()
	#Calculate the number of days from 1/1/2016 till today.
	day_count = (datetime.date.today() - datetime.date(2016, 1, 1)).days

	#For every coin id available.
	for i in range(len(list)):
		jdata = {}
		coinID = list[i]['id']
		for date in (datetime.date(2016, 1, 1) + datetime.timedelta(n) for n in range(day_count)):
			print(str(date))
			coinHistory = coin.CoingeckoAPI('https://api.coingecko.com/api/v3/coins/' + coinID + '/history?date='+ date.strftime("%d-%m-%Y"))
			data = coinHistory.get_coingecko_data()
			jdata[str(date)] = []
			jdata[str(date)].append(data)
		with open(coinID + '.json', 'w', encoding='utf8') as outputfile:
			json.dump(jdata, outputfile, ensure_ascii=False)

if __name__ == '__main__':
	main()