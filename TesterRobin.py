import pandas as pd
import robin_stocks as r
import matplotlib.pyplot as plt
import os

symbol = "ALPN"
arr1 = []

r.authentication.login(username=os.environ.get('RobinUSR'), password=os.environ.get('RobinPWD'))

df1 = pd.DataFrame(r.stocks.get_stock_historicals("alpn", interval="5minute", span="day"))
df1.index = pd.to_datetime(df1)
index = pd.DatetimeIndex(df1.index)
df1 = index.tz_convert('US/Eastern').strftime("%H:%M:%S")

price = pd.DataFrame(r.stocks.get_stock_historicals(symbol, interval="5minute", span="day"))['close_price'].astype(float).tolist()


# plt.figure(figsize=(10,10))
# plt.plot(df1, price)
# plt.show()
