import os
os.getcwd()

import warnings
warnings.filterwarnings("ignore")

import coingecko_api as coin #Import API call code.
import datetime
from tqdm import tqdm
import pandas as pd
from config import cryptocompare_data_path

def main():
   
    coinList = coin.CoingeckoAPI('https://api.coingecko.com/api/v3/coins/list')
    #Getting a JSON with the data requested.
    coin_list = coinList.get_coingecko_data()
    
    cryptocompare_tickers = [x.split('.')[0] for x in os.listdir(cryptocompare_data_path)]
    cryptocompare_tickers.remove('')
    cryptocompare_tickers.remove('update_label')
    tickers = [coin for coin in coin_list if coin['symbol'].upper() in cryptocompare_tickers]

    #Calculate the number of days from 1/1/2017 till today.
    day_count = (datetime.date.today() - datetime.date(2017, 1, 1)).days
    #Create directory with data
    if not os.path.exists(os.getcwd() + '/data/'):
        os.makedirs(os.getcwd() + '/data/')

    #For every coin id available.
    for i in tqdm(range(len(tickers))):
        #Dataframe containing data per date.
        df = pd.DataFrame(columns = ['market_cap', 'total_volume', 'facebook_likes', 'twitter_followers', 'reddit_average_posts_48h', 'reddit_average_comments_48h', 'reddit_subscribers', 'reddit_accounts_active_48h', 'forks', 'stars', 'subscribers', 'total_issues', 'closed_issues', 'pull_requests_merged', 'pull_request_contributors', 'commit_count_4_weeks', 'alexa_rank', 'bing_matches'], 
                          index=(datetime.date(2017, 1, 1) + datetime.timedelta(n) for n in range(day_count)))
        coinID = tickers[i]['id']
        print(tickers[i]['name'].upper())
        #Skip this cryptocurrency if its JSON file already exists.
        if os.path.exists(os.getcwd() + '/data/' + tickers[i]['symbol'].upper() + '.csv'): continue
        #For every day since 1/1/2017 till today.
        for date in tqdm((datetime.date(2017, 1, 1) + datetime.timedelta(n) for n in range(day_count)), total=day_count, unit="days"):
            coinHistory = coin.CoingeckoAPI('https://api.coingecko.com/api/v3/coins/' + coinID + '/history?date='+ date.strftime("%d-%m-%Y"))
            data = coinHistory.get_coingecko_data()
            try:
                #Save market data
                for column in ['market_cap', 'total_volume']:
                    df[column].loc[date] = data['market_data'][column]['usd']
                #Save community data
                for column in ['facebook_likes', 'twitter_followers', 'reddit_average_posts_48h', 'reddit_average_comments_48h', 'reddit_subscribers', 'reddit_accounts_active_48h']:
                    df[column].loc[date] = data['community_data'][column]
                #Save developer data
                for column in ['forks', 'stars', 'subscribers', 'total_issues', 'closed_issues', 'pull_requests_merged', 'pull_request_contributors', 'commit_count_4_weeks']:
                    df[column].loc[date] = data['developer_data'][column]  
                #Save public interest data
                for column in ['alexa_rank', 'bing_matches']:
                    df[column].loc[date] = data['public_interest_stats'][column]
            except Exception as e:
                print(e)
        #Writing data for each currency to a csv file with its name.
        df.to_csv(os.getcwd() + '/data/' + tickers[i]['symbol'].upper() + '.csv', index_label='date')

if __name__ == '__main__':
    main()
