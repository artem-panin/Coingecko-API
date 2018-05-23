#Code to add a path to System path in order to import other files from the coingecko folder.
import sys
sys.path.append(r'H:/Data_Science/Python/coingecko')

import coingecko_api as coin #Import API call code.
import json, datetime, os.path


def main():
	coinList = coin.CoingeckoAPI('https://api.coingecko.com/api/v3/coins/list')
	#Getting a JSOn with the data requested.
	list = coinList.get_coingecko_data()
	#Calculate the number of days from 1/1/2016 till today.
	day_count = (datetime.date.today() - datetime.date(2016, 1, 1)).days

	#For every coin id available.
	for i in range(len(list)):
		#Dictionary containing data per date.
		jdata = {}
		coinID = list[i]['id']
		#Skip this cryptocurrency if its JSON file already exists.
		if os.path.exists('H:/Data_Science/Python/data/' + coinID + '.json'): continue
		#For every day since 1/1/2016 till today.
		for date in (datetime.date(2016, 1, 1) + datetime.timedelta(n) for n in range(day_count)):
			print(coinID, str(date))
			coinHistory = coin.CoingeckoAPI('https://api.coingecko.com/api/v3/coins/' + coinID + '/history?date='+ date.strftime("%d-%m-%Y"))
			data = coinHistory.get_coingecko_data()
			jdata[str(date)] = []
			jdata[str(date)].append(data)
		#Writing data for each currency to a json file with its name.
		with open('H:/Data_Science/Python/data/' + coinID + '.json', 'w', encoding='utf8') as outputfile:
			json.dump(jdata, outputfile, ensure_ascii=False)

if __name__ == '__main__':
	main()
