# import packages
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import datetime
import yfinance as yf
from yahoo_fin import stock_info as si
from time import sleep
import time
import threading
import pandas as pd
import numpy as np

# define the plot style and initialize the tkinter GUI
plt.style.use('seaborn-darkgrid')
root = Tk()

# define the tickers and arrays to hold the data
symbol1 = "POLA"
symbol2 = "CYDY"
gainerdata = []
loserdata = []
activedata = []

# initialize the stocks
stockOne = yf.Ticker(symbol1)
stockTwo = yf.Ticker(symbol2)

# define the arrays and string variables for the top movers
currPrice1 = StringVar()
currPrice2 = StringVar()
gainers = StringVar()
losers = StringVar()
activity = StringVar()
symbol = StringVar()
symbol.set(symbol2)

# labels for stock data
Label(root, textvariable=currPrice1, font=("Times", 16)).grid(row=0, column=2, sticky='WENS')
Label(root, text=symbol1, font=("Times", 16)).grid(row=0, column=1, sticky='WENS')
Label(root, textvariable=currPrice2, font=("Times", 16)).grid(row=2, column=2, sticky='WENS')
Label(root, textvariable=symbol, font=("Times", 16)).grid(row=2, column=1, sticky='WENS')


def onselectGainer(evt):
    global symbol2, gainerdata, stockTwo, canvas3
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    symbol2 = gainerdata['Symbol'][index]
    symbol.set(symbol2)
    stockTwo = yf.Ticker(symbol2)
    updateDailies()
    plotgraph4()


def onselectLoser(evt):
    global symbol2, loserdata, stockTwo
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    symbol2 = loserdata['Symbol'][index]
    symbol.set(symbol2)
    stockTwo = yf.Ticker(symbol2)
    updateDailies()
    plotgraph4()


def onselectActive(evt):
    global symbol2, activedata, stockTwo
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    symbol2 = activedata['Symbol'][index]
    symbol.set(symbol2)
    stockTwo = yf.Ticker(symbol2)
    updateDailies()
    plotgraph4()


# labels for gainers and losers
Label(root, text="Top Gainers", font=("Times", 16), fg="green").grid(row=0, column=3, sticky='WENS')
gainerbox = Listbox(root, listvariable=gainers, font=("Times", 12), fg="green", width=30, selectmode=SINGLE)
gainerbox.grid(row=1, column=3, sticky='WENS')
Label(root, text="Top Active", font=("Times", 16), fg="blue").grid(row=2, column=3, sticky='WENS')
activitybox = Listbox(root, listvariable=activity, font=("Times", 12), fg="blue", width=30, selectmode=SINGLE)
activitybox.grid(row=3, column=3, sticky='WENS')
Label(root, text="Top Losers", font=("Times", 16), fg="red").grid(row=0, column=4, sticky='WENS')
loserbox = Listbox(root, listvariable=losers, font=("Times", 12), fg="red", width=30, selectmode=SINGLE)
loserbox.grid(row=1, column=4, sticky='WENS')

gainerbox.bind("<Double-Button-1>", onselectGainer)
loserbox.bind("<Double-Button-1>", onselectLoser)
activitybox.bind("<Double-Button-1>", onselectActive)

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


# defines what to do on startup to initialize everything
def startup():
    # plot the historical graphs and set up the top movers lists
    plotgraph1()
    plotgraph3()
    getDayMovers()
    plotgraph2()
    plotgraph4()


# updates the daily graphs and label
def updateDailies():
    global stockOne, stockTwo, loserbox, gainerbox, activitybox
    # set the current price label to the current price
    currPrice1.set("Current Price: $" + (str(round(float(si.get_live_price(symbol1)), 2))))
    currPrice2.set("Current Price: $" + (str(round(float(si.get_live_price(symbol2)), 2))))

    # plot the graphs
    plotgraph1()
    plotgraph3()
    getDayMovers()


# main loop to handle updating the graph once program starts
def stonkLoop():
    try:
        # define the timings
        start = '09:30:00'
        end = '16:00:00'

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

            # amount between graph and price updates - in seconds
            sleep(30)

    except RuntimeError:
        print("[INFO] caught a RuntimeError")


# get the daily movers
def getDayMovers():
    global gainers, losers, activity, gainerdata, loserdata, activedata
    gainerdata = pd.DataFrame(si.get_day_gainers())[['Symbol', 'Price (Intraday)', '% Change']]
    gainerdata['Price (Intraday)'] = "$" + gainerdata['Price (Intraday)'].astype(str)
    gainerdata['% Change'] = "+" + gainerdata['% Change'].astype(str) + "%"
    gainerdata['Combined'] = gainerdata[gainerdata.columns[0:]].apply(
        lambda x: ':'.join(x.dropna().astype(str)),
        axis=1
    )

    loserdata = pd.DataFrame(si.get_day_losers())[['Symbol', 'Price (Intraday)', '% Change']]
    loserdata['Price (Intraday)'] = "$" + loserdata['Price (Intraday)'].astype(str)
    loserdata['% Change'] = loserdata['% Change'].astype(str) + "%"
    loserdata['Combined'] = loserdata[loserdata.columns[0:]].apply(
        lambda x: ':'.join(x.dropna().astype(str)),
        axis=1
    )

    activedata = pd.DataFrame(si.get_day_most_active())[['Symbol', 'Price (Intraday)', '% Change']]
    activedata['Price (Intraday)'] = "$" + activedata['Price (Intraday)'].astype(str)
    activedata['% Change'] = activedata['% Change'].astype(str) + "%"
    activedata['Combined'] = activedata[activedata.columns[0:]].apply(
        lambda x: ':'.join(x.dropna().astype(str)),
        axis=1
    )

    # sets the list box data
    gainers.set('\n'.join(gainerdata['Combined']))
    losers.set('\n'.join(loserdata['Combined']))
    activity.set('\n'.join(activedata['Combined']))


# stonk one - current price
def plotgraph1():
    global df1, figure1, ax1, root, canvas1
    dailyData = pd.DataFrame(stockOne.history(period="1d", interval="1m"))['Open']
    dailyData.index = dailyData.index.strftime("%H:%M:%S")
    ax1.clear()
    # data for the plot
    df1 = None
    df1 = dailyData
    df1.plot(kind='line', legend=False, ax=ax1, grid=True, x=df1.index, y=df1, title="Current Trend")
    figure1.autofmt_xdate()
    canvas1.draw_idle()


# stonk one - one month price graph
def plotgraph2():
    global df2, figure2, ax2, root, canvas2
    monthlyData = pd.DataFrame(stockOne.history(period="1mo", interval="1d"))['Open']
    monthlyData.index = monthlyData.index.strftime("%m/%d")
    ax2.clear()
    # data for the plot
    df2 = None
    df2 = monthlyData
    df2.plot(kind='line', legend=False, ax=ax2, grid=True, x=df2.index, y=df2, title="One Month Trend")
    figure2.autofmt_xdate()
    canvas2.draw_idle()


# stonk two - current price
def plotgraph3():
    global df3, figure3, ax3, root, canvas3
    dailyData = pd.DataFrame(stockTwo.history(period="1d", interval="1m"))['Open']
    dailyData.index = dailyData.index.strftime("%H:%M:%S")
    ax3.clear()
    # data for the plot
    df3 = None
    df3 = dailyData
    df3.plot(kind='line', legend=False, ax=ax3, grid=True, x=df3.index, y=df3, title="Current Trend")
    figure3.autofmt_xdate()
    canvas3.draw_idle()


# stonk two - one month price graph
def plotgraph4():
    global df4, figure4, ax4, root, canvas4
    # data for the plot
    monthlyData = pd.DataFrame(stockTwo.history(period="1mo", interval="1d"))['Open']
    monthlyData.index = monthlyData.index.strftime("%m/%d")
    ax4.clear()
    # data for the plot
    df4 = None
    df4 = monthlyData
    df4.plot(kind='line', legend=False, ax=ax4, grid=True, x=df4.index, y=df4, title="One Month Trend")
    figure4.autofmt_xdate()
    canvas4.draw_idle()


# turn on interactive mode for plots
plt.show()

# set GUI title
root.wm_title("StonksTracker")

startup()

# start the threading
thread = threading.Thread(target=stonkLoop, args=())
thread.start()

# start GUI mainloop
root.mainloop()
