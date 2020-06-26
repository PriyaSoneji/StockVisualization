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

root = Tk()


root.wm_title("StonksTracker")
root.geometry(str(GetSystemMetrics(0)) + "x" + str(GetSystemMetrics(1)))
Label(root, image=PhotoImage(file="C:\\Users\\priya\\Documents\\Stonks\\maxresdefault.png")).place(x=0, y=0, relwidth=1, relheight=1)