import pandas as pd
from config import cryptocompare_data_path
import numpy as np
import os

def main():

    for ticker in [x.split('.')[0] for x in os.listdir("data/")]:
        print(ticker)
        additional_data = pd.read_csv("data/" + ticker + ".csv")
        plain_data = pd.read_csv(cryptocompare_data_path + ticker + ".txt")
        if plain_data.empty:
            continue

        additional_data = additional_data.iloc[np.repeat(np.arange(len(additional_data)), 24)].drop(columns=['date']).set_index(pd.date_range(start='1/1/2017', periods=additional_data.shape[0] * 24, freq='1H')).fillna(0)
        plain_data.index = pd.to_datetime(plain_data.date)    
        plain_data = plain_data.drop(columns=['date']).fillna(0)
        pd.concat([plain_data, additional_data], axis=1).dropna().to_csv("concat_data/" + ticker + ".csv")

if __name__ == '__main__':
    main()