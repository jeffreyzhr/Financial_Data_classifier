import matplotlib.pyplot as plt
from datetime import date
import analyser 
import pickle
import pandas as pd


'''
this is the main python file that will run the analyser on various companies and produce a markdown file
'''

current_year = date.today().year
sp500_tickers = pd.read_csv('Stocks in the SP 500 Index.csv')['Symbol'].to_list()

def save(ticker):
    with open(f'data/{ticker}.pkl', 'wb') as f:
        pickle.dump(to_save_dict, f)

count = 1
for ticker in sp500_tickers:
    to_save_dict = {}
    analyser.execute('AAPL', current_year, dictionary=to_save_dict, write=False)
    save(ticker)
    print(f'{ticker}: DONE ({count}/500)')
    count += 1
