from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from datetime import date
import datetime
import pandas as pd
from time import sleep
import time
import threading
from yahoo_fin import stock_info as si
from yahoo_fin.stock_info import *
import mplcursors
import numpy as np
from win32api import GetSystemMetrics

plt.style.use('seaborn-darkgrid')
root = Tk()

e1 = Entry(root).grid(row=0, column=1, sticky='WENS')
e2 = Entry(root).grid(row=0, column=1, sticky='WENS')

symbol1 = "MSFT"
symbol2 = "ALPN"
symbol3 = "AAPL"
time1 = []
price1 = []
time2 = []
price2 = []
time3 = []
price3 = []

currPrice1 = StringVar()
currPrice2 = StringVar()
Label(root, textvariable=currPrice1, font=("Helvetica", 16)).grid(row=0, column=2, sticky='WENS')
Label(root, text=symbol1, font=("Helvetica", 16)).grid(row=0, column=1, sticky='WENS')
Label(root, textvariable=currPrice2, font=("Helvetica", 16)).grid(row=2, column=2, sticky='WENS')
Label(root, text=symbol2, font=("Helvetica", 16)).grid(row=2, column=1, sticky='WENS')

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
    time1 = []
    time2 = []
    time3 = []
    price1 = []
    price2 = []
    price3 = []
    plotgraph2()
    plotgraph4()


def startup():
    global time1, time2, price1, price2, symbol1, symbol2
    plotgraph2()
    plotgraph4()
    time1.append("09:30:00")
    time2.append("09:30:00")
    price1.append(round(si.get_live_price(symbol1), 2))
    price2.append(round(si.get_live_price(symbol2), 2))


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        return startTime <= nowTime <= endTime
    else:  # Over midnight
        return nowTime >= startTime or nowTime <= endTime


def updateDailies():
    global time1, time2, time3, price1, price2, price3, figure1, symbol1, symbol2, symbol3
    getCurrPrice(symbol1, time1, price1)
    getCurrPrice(symbol2, time2, price2)
    getCurrPrice(symbol3, time3, price3)
    currPrice1.set("Current Price: $" + str(price1[-1]))
    currPrice2.set("Current Price: $" + str(price2[-1]))
    plotgraph1()
    plotgraph3()


def stonkLoop():
    try:
        start = '09:30:10'
        end = '16:30:00'
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

            sleep(10)

    except RuntimeError:
        print("[INFO] caught a RuntimeError")


def getDataMonth(symbol, timearr, pricearr):
    pricearr.append(
        get_data(symbol, index_as_date=False, end_date=date.today().strftime("%d/%m/%Y"), start_date='06/01/2020')[
            'open'])
    timearr.append(get_data(symbol, end_date=date.today().strftime("%d/%m/%Y"), start_date='06/01/2020').index)


def getCurrPrice(symbol, timearr, pricearr):
    global current_time
    pricearr.append(round(si.get_live_price(symbol), 2))
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    timearr.append(current_time)


# stonk one - current price
def plotgraph1():
    # grab a reference to the image panels
    global df1, figure1, ax1, root, price1, time1
    # data for the plot
    df1 = DataFrame({'Price': price1,
                     'Time': time1})
    df1.plot(kind='line', legend=False, ax=ax1, grid=True, x='Time', y='Price', title="Stonks One")
    canvas1.draw_idle()


# stonk one - one month price graph
def plotgraph2():
    # grab a reference to the image panels
    global df2, figure2, ax2, root, symbol1
    # data for the plot
    df2 = DataFrame(
        {'Time': get_data(symbol1, end_date=date.today().strftime("%d/%m/%Y"), start_date='05/01/2020').index,
         'Price': (
             get_data(symbol1, index_as_date=False, end_date=date.today().strftime("%d/%m/%Y"),
                      start_date='05/01/2020')[
                 'open'])})
    df2.plot(kind='line', legend=False, ax=ax2, grid=True, x='Time', y='Price', title="One Month Trend")
    canvas2.draw_idle()


# stonk two - current price
def plotgraph3():
    # grab a reference to the image panels
    global df3, figure3, ax3, root, price2, time2
    # data for the plot
    df3 = DataFrame({'Price': price2,
                     'Time': time2})
    df3.plot(kind='line', legend=False, ax=ax3, grid=True, x='Time', y='Price', title="Stonks Two")
    canvas3.draw_idle()


# stonk two - one month price graph
def plotgraph4():
    # grab a reference to the image panels
    global df4, figure4, ax4, root, symbol2
    # data for the plot
    df4 = DataFrame(
        {'Time': get_data(symbol2, end_date=date.today().strftime("%d/%m/%Y"), start_date='05/01/2020').index,
         'Price': (
             get_data(symbol2, index_as_date=False, end_date=date.today().strftime("%d/%m/%Y"),
                      start_date='05/01/2020')[
                 'open'])})
    df4.plot(kind='line', legend=False, ax=ax4, grid=True, x='Time', y='Price', title="One Month Trend")
    canvas4.draw_idle()


plt.ion()

root.wm_title("StonksTracker")
root.geometry(str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1)))

startup()
thread = threading.Thread(target=stonkLoop, args=())
thread.start()
root.mainloop()
