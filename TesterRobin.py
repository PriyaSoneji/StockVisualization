import pandas as pd
import robin_stocks as r
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
from pandas import DataFrame

symbol = "AAPL"

r.authentication.login(username=os.environ.get('RobinUSR'), password=os.environ.get('RobinPWD'))

df1 = pd.DataFrame(r.stocks.get_stock_historicals(symbol, interval="5minute", span="day"))['begins_at']
df1['begins_at'] = pd.to_datetime(df1)
df1 = pd.DatetimeIndex(df1['begins_at'])
df1 = df1.tz_convert('US/Eastern').strftime("%H:%M:%S")
current_time = datetime.datetime.now().strftime("%H:%M:%S")
df1 = df1.to_numpy()
arr1 = [current_time]
time = np.append(df1, arr1)
print(len(time))

price = pd.DataFrame(r.stocks.get_stock_historicals(symbol, interval="5minute", span="day"))['close_price'].astype(
    float).tolist()
price.append(round(float(r.stocks.get_latest_price(symbol)[0]), 2))
print(len(price))

data = DataFrame({'Price': price,
                  'Time': time})

print(data)

plt.figure(figsize=(5, 5))
plt.plot(time, price)
plt.show()
