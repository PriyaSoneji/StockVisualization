import pandas as pd
import robin_stocks as r
import matplotlib.pyplot as plt
import os

symbol = "AAPL"
arr1 = []

r.authentication.login(username=os.environ.get('RobinUSR'), password=os.environ.get('RobinPWD'), store_session=True)

df1 = pd.DataFrame(r.stocks.get_stock_historicals(symbol, interval="5minute", span="day"))['begins_at']
df1.index = pd.to_datetime(df1)
index = pd.DatetimeIndex(df1.index)
df1 = index.tz_convert('US/Eastern').strftime("%H:%M:%S")

price = pd.DataFrame(r.stocks.get_stock_historicals(symbol, interval="5minute", span="day"))['close_price'].astype(float).tolist()
# print(df1)
# print(price)
print(round(float(r.stocks.get_latest_price(symbol)[0]), 2))

plt.figure(figsize=(10,10))
plt.plot(df1, price)
plt.show()
