import matplotlib.pyplot as plt
from datetime import date
from yahoo_fin.stock_info import *
import mplcursors

plt.figure(figsize=(10,10))
plt.plot((get_data("AAPL", end_date=date.today().strftime("%d/%m/%Y"), start_date='06/01/2020').index), (get_data("AAPL", index_as_date=False, end_date=date.today().strftime("%d/%m/%Y"), start_date='06/01/2020')['open']))
mplcursors.cursor(hover=True)
plt.show()