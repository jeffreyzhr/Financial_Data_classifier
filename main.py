import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date
import analyser

'''
this is the main python file that will run the analyser on various companies and produce a markdown file
'''
print(1)
ticker = 'AAPL'
current_year = date.today().year

analyser.execute('AAPL', current_year, write=False)