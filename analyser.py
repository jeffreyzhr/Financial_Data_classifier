import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date, timedelta


def execute(ticker, current_year, dictionary, write = True):
    current = yf.Ticker(ticker)
    #quarterly data
    cashflow = current.quarterly_cashflow
    financials = current.quarterly_financials
    balance_sheet = current.quarterly_balance_sheet

    #annual data
    years_index = current.shares.index.to_list() # list of years to use as keys
    years_index.append(current_year)
    annual_earnings = current.earnings["Earnings"].to_dict() # earnings dict with years as keys
    shares = current.shares['BasicShares'].to_dict() # shares dict with years as keys
    fivey_hist = current.history(period="5y")
    
    dictionary[f'{ticker} Annual Earnings'] = annual_earnings
    dictionary[f'{ticker} Annual Outstanding Shares'] = shares

    #method to get quarterly filing dates. Returns list of dates
    file_dates = []
    quarter_dates = balance_sheet.columns.to_list()
    quarter_dates.insert(0, date.today() - timedelta(days = 1))
    for day in quarter_dates:
        while day.strftime('%Y-%m-%d') not in fivey_hist["Close"].keys():
            day = day - pd.Timedelta(days=1)
        file_dates.insert(0, day.strftime('%Y-%m-%d'))

    #list of close prices at quarterly filing date
    quarterly_close_price = [fivey_hist["Close"].loc[date] for date in file_dates]

    # estimating [current_year] annual data using quarterly data
    estimated_earnings = current.quarterly_earnings['Earnings'].sum()
    current_shares = current.info['sharesOutstanding']


    annual_earnings[current_year] = estimated_earnings
    shares[current_year] = current_shares

    # EPS per year dictionary
    annual_EPS = {}
    for year in years_index:
        eps = annual_earnings.get(year)/shares.get(year)
        annual_EPS[year] = eps
    dictionary[f'{ticker} Annual EPS'] = annual_EPS

    # Splitting 5yr hist into respective years
    years_index_timestamp = [pd.Timestamp(year = y, month = 1, day = 1) for y in years_index]

    yearly_hist = {}
    for i in range(len(years_index_timestamp) - 1):
        start = years_index_timestamp[i]
        cutoff = years_index_timestamp[i+1]
        
        close = current.history(start = start, end=cutoff)
        yearly_hist[years_index[i]] = close
    yearly_hist[years_index[-1]] = current.history(start = years_index_timestamp[-1], end=None)
    dictionary[f'{ticker} Yearly Hist values'] = yearly_hist #reminder that yearly hist is a dict with years as keys has has cols (open, close, volume etc)

    # Getting daily PE ratios for each year based on annual_EPS and yearly_hist
    yearly_PE = {}
    for year in years_index:
        close = yearly_hist[year]['Close'].to_list()
        PE_ratio = [price/annual_EPS[year] for price in close]
        yearly_PE[year] = PE_ratio
    dictionary[f'{ticker} Annual PE ratio'] = yearly_PE #daily PE ratio for each year