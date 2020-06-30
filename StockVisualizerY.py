# import packages
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import datetime
import yfinance as yf
from yahoo_fin import *
from time import sleep
import time
import threading
import pandas as pd
import numpy as np

# define the plot style and initialize the tkinter GUI
plt.style.use('seaborn-darkgrid')
root = Tk()

# define the tickers and arrays to hold the data
symbol1 = "KSS"
symbol2 = "NBL"

# initialize the stocks
stockOne = yf.Ticker(symbol1)
stockTwo = yf.Ticker(symbol2)

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
Label(root, text=symbol1, font=("Times", 16)).grid(row=0, column=1, sticky='WENS')
Label(root, textvariable=currPrice2, font=("Times", 16)).grid(row=2, column=2, sticky='WENS')
Label(root, text=symbol2, font=("Times", 16)).grid(row=2, column=1, sticky='WENS')

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
canvas4.get_tk_widget().grid(row=3, column=2, sticky='WENS')

# stop event for threading
stopEvent = threading.Event()


# resets the plots
def resetDaily():
    global figure1, figure3
    figure1.clf()
    figure3.clf()
    time1 = []
    time2 = []
    price1 = []
    price2 = []


# defines what to do on startup to initialize everything
def startup():
    # plot the historical graphs and set up the top movers lists
    plotgraph2()
    plotgraph4()
    # getDayMovers()


# updates the daily graphs and label
def updateDailies():
    global stockOne, stockTwo
    # set the current price label to the current price
    dailyData1 = pd.DataFrame(stockOne.history(period="1d", interval="1m"))['Open']
    dailyData2 = pd.DataFrame(stockTwo.history(period="1d", interval="1m"))['Open']
    currPrice1.set("Current Price: $" + (str(round(float(dailyData1[-1]), 2))))
    currPrice2.set("Current Price: $" + (str(round(float(dailyData2[-1]), 2))))

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
                # get the current data and update the graphs
                updateDailies()

            # check if its the refresh time
            if refreshStart < currtime < refreshEnd:
                resetDaily()

            # amount between graph and price updates - in seconds
            sleep(60)

    except RuntimeError:
        print("[INFO] caught a RuntimeError")


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
    global df1, figure1, ax1, root
    dailyData = pd.DataFrame(stockOne.history(period="1d", interval="1m"))['Open']
    dailyData.index = dailyData.index.strftime("%H:%M:%S")
    # data for the plot
    df1 = dailyData
    df1.plot(kind='line', legend=False, ax=ax1, grid=True, x=df1.index, y=df1, title="Current Trend")
    figure1.autofmt_xdate()
    canvas1.draw_idle()


# stonk one - one month price graph
def plotgraph2():
    global df2, figure2, ax2, root
    monthlyData = pd.DataFrame(stockOne.history(period="1mo", interval="1d"))['Open']
    monthlyData.index = monthlyData.index.strftime("%m/%d")
    # data for the plot
    df2 = monthlyData
    df2.plot(kind='line', legend=False, ax=ax2, grid=True, x=df2.index, y=df2, title="One Month Trend")
    figure2.autofmt_xdate()
    canvas2.draw_idle()


# stonk two - current price
def plotgraph3():
    global df3, figure3, ax3, root
    dailyData = pd.DataFrame(stockTwo.history(period="1d", interval="1m"))['Open']
    dailyData.index = dailyData.index.strftime("%H:%M:%S")
    # data for the plot
    df3 = dailyData
    df3.plot(kind='line', legend=False, ax=ax3, grid=True, x=df3.index, y=df3, title="Current Trend")
    figure3.autofmt_xdate()
    canvas3.draw_idle()


# stonk two - one month price graph
def plotgraph4():
    global df4, figure4, ax4, root
    # data for the plot
    monthlyData = pd.DataFrame(stockTwo.history(period="1mo", interval="1d"))['Open']
    monthlyData.index = monthlyData.index.strftime("%m/%d")
    # data for the plot
    df4 = monthlyData
    df4.plot(kind='line', legend=False, ax=ax4, grid=True, x=df4.index, y=df4, title="One Month Trend")
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
