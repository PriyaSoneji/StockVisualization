import matplotlib.pyplot as plt
from datetime import date
import yfinance as yf
import pandas as pd
import mplcursors

symbol1 = "AAPL"
stockOne = yf.Ticker(symbol1)

dailyData = pd.DataFrame(stockOne.history(period="1d", interval="1m"))['Open']
dailyData.index = dailyData.index.strftime("%H:%M:%S")
print(dailyData)
print(dailyData[-1])

plt.figure(figsize=(5, 5))
plt.plot(dailyData)
plt.show()