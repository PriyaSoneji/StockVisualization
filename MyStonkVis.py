from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import datetime
import os
import robin_stocks as r
from time import sleep
import time
import threading
import mplcursors
import pandas as pd
import numpy as np

plt.style.use('seaborn-darkgrid')
root = Tk()

r.authentication.login(username=os.environ.get('RobinUSR'), password=os.environ.get('RobinPWD'))

symbol1 = "COTY"
symbol2 = "ALPN"
symbol3 = "AAPL"
time1 = []
price1 = []
time2 = []
price2 = []
time3 = []
price3 = []

dataup = []
datadown = []
currPrice1 = StringVar()
currPrice2 = StringVar()
gainers = StringVar(value=dataup)
losers = StringVar(value=datadown)

# labels for stock data
Label(root, textvariable=currPrice1, font=("Helvetica", 16)).grid(row=0, column=2, sticky='WENS')
Label(root, text=r.stocks.get_name_by_symbol(symbol1), font=("Helvetica", 16)).grid(row=0, column=1, sticky='WENS')
Label(root, textvariable=currPrice2, font=("Helvetica", 16)).grid(row=2, column=2, sticky='WENS')
Label(root, text=r.stocks.get_name_by_symbol(symbol2), font=("Helvetica", 16)).grid(row=2, column=1, sticky='WENS')

# labels for gainers and losers
Label(root, text="The Day's Top Gainers", font=("Helvetica", 16)).grid(row=0, column=3, sticky='WENS')
Label(root, text="The Day's Top Losers", font=("Helvetica", 16)).grid(row=2, column=3, sticky='WENS')
Listbox(root, listvariable=gainers).grid(row=1, column=3, sticky='WENS')
Listbox(root, listvariable=losers).grid(row=3, column=3, sticky='WENS')

current_time = 0

# figure one data
df1 = None
figure1 = plt.Figure(figsize=(4, 3), dpi=100)
ax1 = figure1.add_subplot(111)
canvas1 = FigureCanvasTkAgg(figure1, root)
canvas1.get_tk_widget().grid(row=1, column=1, sticky='WENS')

# figure two data
df2 = None
figure2 = plt.Figure(figsize=(4, 3), dpi=100)
ax2 = figure2.add_subplot(111)
canvas2 = FigureCanvasTkAgg(figure2, root)
mplcursors.cursor(hover=True)
canvas2.get_tk_widget().grid(row=1, column=2, sticky='WENS')

# figure three data
df3 = None
figure3 = plt.Figure(figsize=(4, 3), dpi=100)
ax3 = figure3.add_subplot(111)
canvas3 = FigureCanvasTkAgg(figure3, root)
canvas3.get_tk_widget().grid(row=3, column=1, sticky='WENS')

# figure four data
df4 = None
figure4 = plt.Figure(figsize=(4, 3), dpi=100)
ax4 = figure4.add_subplot(111)
canvas4 = FigureCanvasTkAgg(figure4, root)
mplcursors.cursor(hover=True)
canvas4.get_tk_widget().grid(row=3, column=2, sticky='WENS')

# stop event
stopEvent = threading.Event()


def resetDaily():
    global time1, time2, time3, price1, price2, price3, figure1
    figure1.clf()
    figure3.clf()
    time1 = []
    time2 = []
    time3 = []
    price1 = []
    price2 = []
    price3 = []


def startup():
    global time1, time2, price1, price2, symbol1, symbol2
    refreshStart = '09:30:00'
    refreshEnd = '20:00:00'
    t = time.localtime()
    d = datetime.datetime.now()
    currtime = time.strftime("%H:%M:%S", t)
    if (refreshStart < currtime < refreshEnd) and (d.isoweekday() in range(1, 6)):
        time1 = getDayUpNow(symbol1)
        time2 = getDayUpNow(symbol2)
        price1 = pd.DataFrame(r.stocks.get_stock_historicals(symbol1, interval="5minute", span="day"))[
            'close_price'].astype(float).tolist()
        price2 = pd.DataFrame(r.stocks.get_stock_historicals(symbol2, interval="5minute", span="day"))[
            'close_price'].astype(float).tolist()

        time1 = time1.to_numpy()
        time2 = time2.to_numpy()
        plotgraph1()
        plotgraph3()

    plotgraph2()
    plotgraph4()
    getDayMovers()


def updateDailies():
    global time1, time2, time3, price1, price2, price3, figure1, symbol1, symbol2, symbol3, current_time
    currPrice1.set("Current Price: $" + (str(round(float(r.stocks.get_latest_price(symbol1)[0]), 2))))
    currPrice2.set("Current Price: $" + (str(round(float(r.stocks.get_latest_price(symbol2)[0]), 2))))
    time1 = getCurrPrice(symbol1, time1, price1)
    time2 = getCurrPrice(symbol2, time2, price2)
    time3 = getCurrPrice(symbol3, time3, price3)
    plotgraph1()
    plotgraph3()


def stonkLoop():
    try:
        start = '09:30:00'
        end = '16:00:00'
        refreshStart = '09:29:00'
        refreshEnd = '09:29:30'
        while not stopEvent.is_set():
            t = time.localtime()
            d = datetime.datetime.now()
            currtime = time.strftime("%H:%M:%S", t)
            if (start < currtime < end) and (d.isoweekday() in range(1, 6)):
                updateDailies()

            if refreshStart < currtime < refreshEnd:
                resetDaily()

            sleep(30)

    except RuntimeError:
        print("[INFO] caught a RuntimeError")


def getDayUpNow(symbol):
    data = pd.DataFrame(r.stocks.get_stock_historicals(symbol, interval="5minute", span="day"))['begins_at']
    data['begins_at'] = pd.to_datetime(data)
    data = pd.DatetimeIndex(data['begins_at'])
    return data.tz_convert('US/Eastern').strftime("%H:%M:%S")


def getCurrPrice(symbol, timearr, pricearr):
    global current_time
    pricearr.append(round(float(r.stocks.get_latest_price(symbol)[0]), 2))
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    arr1 = [current_time]
    return np.append(timearr, arr1)


def getDayMovers():
    global gainers, losers, dataup, datadown
    dataupp = pd.DataFrame(r.markets.get_top_movers("up"))['price_movement']
    dataupp.index = pd.DataFrame(r.markets.get_top_movers("up"))['symbol']
    dataupp.to_numpy()
    datadownn = pd.DataFrame(r.markets.get_top_movers("down"))['price_movement']
    datadownn.index = pd.DataFrame(r.markets.get_top_movers("down"))['symbol']
    datadownn.to_numpy()
    datadown = datadownn.index
    dataup = dataupp.index
    gainers.set(dataup)
    losers.set(datadown)


# stonk one - current price
def plotgraph1():
    global df1, figure1, ax1, root, price1, time1
    # data for the plot
    df1 = DataFrame({'Price': price1,
                     'Time': time1})
    df1.plot(kind='line', legend=False, ax=ax1, grid=True, x='Time', y='Price', title="Current Trend")
    canvas1.draw_idle()


# stonk one - one month price graph
def plotgraph2():
    global df2, figure2, ax2, root, symbol1, figure2
    mondat = pd.DataFrame(r.stocks.get_stock_historicals(symbol1, interval="day", span="month"))['begins_at']
    mondat.index = pd.to_datetime(mondat)
    index = pd.DatetimeIndex(mondat.index)
    mondat = index.tz_convert('US/Eastern').strftime("%m/%d")
    # data for the plot
    df2 = DataFrame({'Time': mondat,
                     'Price': pd.DataFrame(r.stocks.get_stock_historicals(symbol1, interval="day", span="month"))[
                         'close_price'].astype(float)})
    df2.plot(kind='line', legend=False, ax=ax2, grid=True, x='Time', y='Price', title="One Month Trend")
    figure2.autofmt_xdate()
    canvas2.draw_idle()


# stonk two - current price
def plotgraph3():
    # grab a reference to the image panels
    global df3, figure3, ax3, root, price2, time2
    # data for the plot
    df3 = DataFrame({'Price': price2,
                     'Time': time2})
    df3.plot(kind='line', legend=False, ax=ax3, grid=True, x='Time', y='Price', title="Current Trend")
    canvas3.draw_idle()


# stonk two - one month price graph
def plotgraph4():
    # grab a reference to the image panels
    global df4, figure4, ax4, root, symbol2, figure4
    # data for the plot
    mondat = pd.DataFrame(r.stocks.get_stock_historicals(symbol2, interval="day", span="month"))['begins_at']
    mondat.index = pd.to_datetime(mondat)
    index = pd.DatetimeIndex(mondat.index)
    mondat = index.tz_convert('US/Eastern').strftime("%m/%d")
    # data for the plot
    df4 = DataFrame({'Time': mondat,
                     'Price': pd.DataFrame(r.stocks.get_stock_historicals(symbol2, interval="day", span="month"))[
                         'close_price'].astype(float)})
    df4.plot(kind='line', legend=False, ax=ax4, grid=True, x='Time', y='Price', title="One Month Trend")
    figure4.autofmt_xdate()
    canvas4.draw_idle()


plt.ion()

root.wm_title("StonksTracker")

startup()
thread = threading.Thread(target=stonkLoop, args=())
thread.start()
root.mainloop()
