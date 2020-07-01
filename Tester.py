import matplotlib.pyplot as plt
from datetime import date
import yfinance as yf
import pandas as pd
from yahoo_fin import stock_info as si
import mplcursors

symbol1 = "AAPL"
stockOne = yf.Ticker(symbol1)

dailyData = pd.DataFrame(stockOne.history(period="1d", interval="1m"))['Open']
dailyData.index = dailyData.index.strftime("%H:%M:%S")


gainers = pd.DataFrame(si.get_day_gainers())[['Price (Intraday)', '% Change']]
gainers.index = pd.DataFrame(si.get_day_gainers())['Symbol']

losers = pd.DataFrame(si.get_day_losers())[['Price (Intraday)', '% Change']]
losers.index = pd.DataFrame(si.get_day_losers())['Symbol']

active = pd.DataFrame(si.get_day_most_active())[['Price (Intraday)', '% Change']]
active.index = pd.DataFrame(si.get_day_most_active())['Symbol']

print(gainers.head())
print(losers.head())
print(active.head())
