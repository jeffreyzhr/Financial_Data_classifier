import matplotlib.pyplot as plt
from datetime import date
import analyser 
import pickle
import pandas as pd
from tqdm import tqdm
import traceback


'''
this is the main python file that will run the analyser on various companies and produce a markdown file
'''

current_year = date.today().year
sp500_tickers = pd.read_csv('Stocks in the SP 500 Index.csv')['Symbol'].to_list()

def save(ticker):
    with open(f'data/{ticker}.pkl', 'wb') as f:
        pickle.dump(to_save_dict, f)

poopoo_tickers = []

count = 1
for i in tqdm(range(len(sp500_tickers)), desc="Tickers completed"):
    ticker = sp500_tickers[i]
    #for ticker in sp500_tickers:
    to_save_dict = {}
    try:
        analyser.execute(ticker, current_year, dictionary=to_save_dict, write=False)
    except:
        poopoo_tickers.append(ticker)
        print(f"{ticker} failed.")
        print(traceback.format_exc())
        continue
    save(ticker)
    #print(f'{ticker}: DONE ({count}/500)')
    count += 1

print("Calculations complete.")
print("Tickers successfully processed:", count)
print("Unsuccessful tickers:", poopoo_tickers)