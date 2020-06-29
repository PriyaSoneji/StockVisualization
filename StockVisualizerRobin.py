# import packages
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

# define the plot style and initialize the tkinter GUI
plt.style.use('seaborn-darkgrid')
root = Tk()

# login to RobinHood using environment variables
r.authentication.login(username=os.environ.get('RobinUSR'), password=os.environ.get('RobinPWD'))

# define the tickers and arrays to hold the data
symbol1 = "KSS"
symbol2 = "NBL"
time1 = []
price1 = []
time2 = []
price2 = []

# define the arrays and string variables for the top movers
dataup = []
datadown = []
pctup = []
pctdown = []
currPrice1 = StringVar()
currPrice2 = StringVar()
gainers = StringVar(value=dataup)
losers = StringVar(value=datadown)
gainups = StringVar(value=pctup)
gaindowns = StringVar(value=pctdown)

# labels for stock data
Label(root, textvariable=currPrice1, font=("Times", 16)).grid(row=0, column=2, sticky='WENS')
Label(root, text=r.stocks.get_name_by_symbol(symbol1), font=("Times", 16)).grid(row=0, column=1, sticky='WENS')
Label(root, textvariable=currPrice2, font=("Times", 16)).grid(row=2, column=2, sticky='WENS')
Label(root, text=r.stocks.get_name_by_symbol(symbol2), font=("Times", 16)).grid(row=2, column=1, sticky='WENS')

# labels for gainers and losers
Label(root, text="Top Gainers", font=("Times", 16), fg="green").grid(row=0, column=3, sticky='WENS')
Label(root, text="Top Losers", font=("Times", 16), fg="red").grid(row=2, column=3, sticky='WENS')
Listbox(root, listvariable=gainers, font=("Times", 16), fg="green").grid(row=1, column=3, sticky='WENS')
Listbox(root, listvariable=losers, font=("Times", 16), fg="red").grid(row=3, column=3, sticky='WENS')
Label(root, text="% Up", font=("Times", 16), fg="green").grid(row=0, column=4, sticky='WENS')
Label(root, text="% Down", font=("Times", 16), fg="red").grid(row=2, column=4, sticky='WENS')
Listbox(root, listvariable=gainups, font=("Times", 16), fg="green").grid(row=1, column=4, sticky='WENS')
Listbox(root, listvariable=gaindowns, font=("Times", 16), fg="red").grid(row=3, column=4, sticky='WENS')

# initialize the current time
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

# stop event for threading
stopEvent = threading.Event()


# resets the plots
def resetDaily():
    global time1, time2, time3, price1, price2, price3, figure1
    figure1.clf()
    figure3.clf()
    time1 = []
    time2 = []
    price1 = []
    price2 = []


# defines what to do on startup to initialize everything
def startup():
    global time1, time2, price1, price2, symbol1, symbol2

    # set up the times
    refreshStart = '09:30:00'
    refreshEnd = '20:00:00'
    t = time.localtime()
    d = datetime.datetime.now()
    currtime = time.strftime("%H:%M:%S", t)

    # check if the stock market is open
    if (refreshStart < currtime < refreshEnd) and (d.isoweekday() in range(1, 6)):
        # get the data from today up till the current time
        time1 = getDayUpNow(symbol1)
        time2 = getDayUpNow(symbol2)
        price1 = pd.DataFrame(r.stocks.get_stock_historicals(symbol1, interval="5minute", span="day"))[
            'close_price'].astype(float).tolist()
        price2 = pd.DataFrame(r.stocks.get_stock_historicals(symbol2, interval="5minute", span="day"))[
            'close_price'].astype(float).tolist()

        # change the time arrays to a numpy array to accomodate new data being appended
        time1 = time1.to_numpy()
        time2 = time2.to_numpy()

        # plot the graphs
        plotgraph1()
        plotgraph3()

    # plot the historical graphs and set up the top movers lists
    plotgraph2()
    plotgraph4()
    getDayMovers()


# updates the daily graphs and label
def updateDailies():
    global time1, time2, price1, price2, figure1, symbol1, symbol2, current_time

    # set the current price label to the current price
    currPrice1.set("Current Price: $" + (str(round(float(r.stocks.get_latest_price(symbol1)[0]), 2))))
    currPrice2.set("Current Price: $" + (str(round(float(r.stocks.get_latest_price(symbol2)[0]), 2))))

    # add the new data points to the arrays
    time1 = getCurrPrice(symbol1, time1, price1)
    time2 = getCurrPrice(symbol2, time2, price2)

    # plot the graphs
    plotgraph1()
    plotgraph3()


# main loop to handle updating the graph once program starts
def stonkLoop():
    try:
        # define the timings
        start = '09:30:00'
        end = '16:00:00'
        refreshStart = '09:29:00'
        refreshEnd = '09:29:30'

        # confirm threading stopEvent
        while not stopEvent.is_set():
            # get current time and date
            t = time.localtime()
            d = datetime.datetime.now()
            currtime = time.strftime("%H:%M:%S", t)

            # check if stock market is open
            if (start < currtime < end) and (d.isoweekday() in range(1, 6)):
                updateDailies()

            # check if its the refresh time
            if refreshStart < currtime < refreshEnd:
                resetDaily()

            # amount between graph and price updates - in seconds
            sleep(30)

    except RuntimeError:
        print("[INFO] caught a RuntimeError")


# gets the time data from today
def getDayUpNow(symbol):
    # gets the daily data with 5 minute interval from RobinHood and converts it into proper format
    data = pd.DataFrame(r.stocks.get_stock_historicals(symbol, interval="5minute", span="day"))['begins_at']
    data['begins_at'] = pd.to_datetime(data)
    data = pd.DatetimeIndex(data['begins_at'])
    return data.tz_convert('US/Eastern').strftime("%H:%M:%S")


# gets the current price and time
def getCurrPrice(symbol, timearr, pricearr):
    global current_time
    # appends the current price to the price array
    pricearr.append(round(float(r.stocks.get_latest_price(symbol)[0]), 2))
    # gets the current time in hour:minute:second format
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    arr1 = [current_time]
    return np.append(timearr, arr1)


# get the daily movers
def getDayMovers():
    global gainers, losers, dataup, datadown, pctup, pctdown, gainups, gaindowns
    dataupp = pd.DataFrame(r.markets.get_top_movers("up"))
    datadownn = pd.DataFrame(r.markets.get_top_movers("down"))

    dataupp['pct'] = dataupp['price_movement'].apply(lambda x: x['market_hours_last_movement_pct'])
    datadownn['pct'] = datadownn['price_movement'].apply(lambda x: x['market_hours_last_movement_pct'])

    pctup = dataupp['pct']
    pctdown = datadownn['pct']

    dataupp.index = pd.DataFrame(r.markets.get_top_movers("up"))['symbol']
    datadownn.index = pd.DataFrame(r.markets.get_top_movers("down"))['symbol']

    datadownn.to_numpy()
    dataupp.to_numpy()
    datadown = datadownn.index
    dataup = dataupp.index

    # sets the list box data
    gainers.set('\n'.join(dataup))
    losers.set('\n'.join(datadown))
    gainups.set('\n'.join(pctup))
    gaindowns.set('\n'.join(pctdown))


# stonk one - current price
def plotgraph1():
    global df1, figure1, ax1, root, price1, time1
    # data for the plot
    df1 = DataFrame({'Price': price1,
                     'Time': time1})
    df1.plot(kind='line', legend=False, ax=ax1, grid=True, x='Time', y='Price', title="Current Trend")
    figure1.autofmt_xdate()
    canvas1.draw_idle()


# stonk one - one month price graph
def plotgraph2():
    global df2, figure2, ax2, root, symbol1
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
    global df3, figure3, ax3, root, price2, time2
    # data for the plot
    df3 = DataFrame({'Price': price2,
                     'Time': time2})
    df3.plot(kind='line', legend=False, ax=ax3, grid=True, x='Time', y='Price', title="Current Trend")
    figure3.autofmt_xdate()
    canvas3.draw_idle()


# stonk two - one month price graph
def plotgraph4():
    global df4, figure4, ax4, root, symbol2
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


# turn on interactive mode for plots
plt.ion()

# set GUI title
root.wm_title("StonksTracker")

startup()

# start the threading
thread = threading.Thread(target=stonkLoop, args=())
thread.start()

# start GUI mainloop
root.mainloop()
