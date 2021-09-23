import os
#import re
import csv
import math
#import pickle
import requests
import bs4 as bs
import numpy as np
#import collections
#import pandas as pd
import tkinter as tk
from time import sleep
from tkinter import ttk
#from tkinter import *
from decimal import Decimal
from threading import Thread
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from tkinter import messagebox
#import pandas_datareader as web
#import matplotlib.pyplot as plt
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


#####################################################################################################################

class Stocks():
    def __init__(self, ticker, steps, amount, pre_price):
        self.name = ticker
        self.principal = amount
        self.price = [0]*steps
        self.previous_price = pre_price
        self.buy = []
        self.buy_time = []
        self.buy_count = 0
        self.gain = 0

    def price_manager(self, price, index):
        self.price[index] = price

#####################################################################################################################

class Crypster(tk.Tk):
    
    def __init__(self):
        super().__init__()
        #Get the current screen width and height
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.swpx = self.screen_width
        self.shpx = self.screen_height
        self.font_size = int(self.shpx*0.0177778)
        self.geometry(("{}x{}").format(self.screen_width, self.screen_height))
        self.title('Crypster v.1.0 (alpha) - Crypto Investor')
        self.canvas = tk.Canvas(self, borderwidth=0, background="salmon")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.canvas.create_line(self.swpx*0.2153, self.shpx*0.0555, self.swpx*0.2153, self.shpx*0.9000)
        self.canvas.create_line(self.swpx*0.5035, self.shpx*0.0555, self.swpx*0.5035, self.shpx*0.9000)
        self.canvas.create_line(self.swpx*0.2153, self.shpx*0.0555, self.swpx*0.5035, self.shpx*0.0555)
        self.canvas.create_line(self.swpx*0.2153, self.shpx*0.9000, self.swpx*0.5035, self.shpx*0.9000)
        self.canvas.create_line(self.swpx*0.2153, self.shpx*0.1000, self.swpx*0.5035, self.shpx*0.1000)

        self.header0 = tk.Label(self, text="Enter amount to invest (₹)")
        self.header0.place(x=self.swpx*0.006944, y=self.shpx*0.05)
        self.principal = tk.Entry(self, text="Enter Principal amount")
        self.principal.place(x=self.swpx*0.006944, y=self.shpx*0.07444)
        self.principal.focus_set()
        self.b0 = tk.Button(self, text="⭐", width=3, height=1, command=self.principal_switch)
        self.b0.place(x=self.swpx*0.14236, y=self.shpx*0.08)
        self.P_amnt = 0.0
        self.tickers = []
        self.prices = []

        # Parameters ##################################################################################

        self.delay = 25 #in seconds, maximum time to wait for the page to load
        self.offset = 5 #in seconds, the difference between delay and dt. Should always be > 0
        self.dt = self.delay + self.offset #in seconds, the time between ticker updates
        self.sample_steps = 5
        self.iterations = 10

        self.price_drop_percent = -15
        self.WAZIR_X_charge_per_transaction = 0.2
        self.max_profit_per = 100 #100%
        self.min_profit_per = 10 #10%

        ################################################################################################
        
        self.header1 = tk.Label(self, text="Selected Tickers will appear below")
        self.header1.place(x=self.swpx*0.2222, y=self.shpx*0.066667)
        self.header2 = tk.Label(self, text="Percentage (%)", background="yellow")
        self.header2.place(x=self.swpx*0.38194, y=self.shpx*0.066667)
        self.count = 0.0
        self.wdgt_trackr = {}
        self.percent = tk.StringVar()
        self.header3 = tk.Label(self, textvar=self.percent, width=5, background="red")
        self.percent.set("0.0")
        self.header3.place(x=self.swpx*0.4583, y=self.shpx*0.066667)

        self.header4 = tk.Label(self, text="Portfolio:", width=10, font=("",self.font_size,"bold"))
        self.header4.place(x=self.swpx*0.5972, y=self.shpx*0.02222)
        self.tprice = tk.StringVar()
        self.header5 = tk.Label(self, textvar=self.tprice, width=15, font=("",self.font_size,"bold"))
        self.header5.place(x=self.swpx*0.66667, y=self.shpx*0.02222)
        self.tprice.set("₹ 0.0")
        self.canvas.pack(fill="both", expand=True)

        self.b1 = tk.Button(self, text=">>", width=5, height=2, state="disabled", command=self.selected_tickers)
        self.b1.place(x=self.swpx*0.1736, y=self.shpx*0.388889)

        self.b2 = tk.Button(self, text="<<", width=5, height=2, state="disabled", command=self.del_selected_tickers)
        self.b2.place(x=self.swpx*0.1736, y=self.shpx*0.5)
        self.past_state = []

        self.b3 = tk.Button(self, text="Start Trading", width=10, height=2, state="disabled", command=self.trading_routine)
        self.b3.place(x=self.swpx*0.5208, y=self.shpx*0.5)

        self.b4 = tk.Button(self, text="Validate", width=10, height=2, state="disabled", command=self.popup_window_validate)
        self.b4.place(x=self.swpx*0.5208, y=self.shpx*0.3888889)
        
        self.yscrollbar = tk.Scrollbar(self)
        
        self.tick_var = tk.StringVar()
        self.lstbx = tk.Listbox(self, listvariable=self.tick_var, height=int(self.shpx*0.0388888),
                                width=int(self.swpx*0.0138888), fg="black",
                                selectmode="multiple", state="disabled", yscrollcommand=self.yscrollbar.set)
        self.lstbx.config(font=("",self.font_size,"bold"))
        self.lstbx.place(x=self.swpx*0.006944, y=self.shpx*0.1111)

        self.bsgl = ttk.Treeview(self, height=int(self.shpx*0.0455556), selectmode="none")
        self.bsgl["columns"] = ("Ticker", "BuyTime", "Buy (₹)", "SellTime", "Sell (₹)", "Gain (₹)")
        self.bsgl.column("#0", width=0)
        self.bsgl.column("Ticker", width=55, anchor="center")
        self.bsgl.column("BuyTime", width=140, anchor="center")
        self.bsgl.column("Buy (₹)", width=75, anchor="center")
        self.bsgl.column("SellTime", width=140, anchor="center")
        self.bsgl.column("Sell (₹)", width=75, anchor="center")
        self.bsgl.column("Gain (₹)", width=80, anchor="center")
        self.bsgl.heading("Ticker" , text="Ticker")
        self.bsgl.heading("BuyTime", text="BuyTime")
        self.bsgl.heading("Buy (₹)", text="Buy (₹)")
        self.bsgl.heading("SellTime", text="SellTime")
        self.bsgl.heading("Sell (₹)", text="Sell (₹)")
        self.bsgl.heading("Gain (₹)", text="Gain (₹)")
        self.bsgl.tag_configure('green', background='chartreuse')
        self.bsgl.tag_configure('red', background='red')
        self.bsgl.place(x=self.swpx*0.59375, y=self.shpx*0.055556)

        self.bsgl.configure(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.config(command=self.bsgl.yview)
        self.yscrollbar.config(command=self.lstbx.yview)

        self.past = self.lstbx.focus_set()
        self.bind_all("<Button-1>", lambda e: self.focus(e))

        self.STATE = 0
        self.glob_counter = 0
        
        self.update_list()


    #####################################################################################################################

    def active(self):
        if (self.count == 100):
            self.b3["state"] = "normal"

    #####################################################################################################################
    
    def focus(self, event):
        def get_data(p):
            try:
                return float(p.get("1.0",'end-1c'))
            except:
                pass
    
        if (self.past != None and ".!text" in str(self.past)):
            num = float(get_data(self.past))
            num = self.round_decimals_down(num)
            try:
                if (self.wdgt_trackr["{}".format(str(self.past))] != num):
                    self.count += (num - self.wdgt_trackr["{}".format(str(self.past))])
                    self.percent.set(str(self.count))
                    self.wdgt_trackr["{}".format(str(self.past))] = num
            except:
                self.wdgt_trackr["{}".format(str(self.past))] = num
                self.count += num
                self.percent.set(str(self.count))

        widget = self.focus_get()
        self.past = widget
        
            
        if (self.count == 100 and self.STATE == 0):
            self.header3.config(bg="chartreuse")
            self.b4["state"] = "normal"
        else:
            self.header3.config(bg="red")
            self.b3["state"] = "disabled"
            self.b4["state"] = "disabled"
            
    #####################################################################################################################

    def principal_switch(self):
        if (self.b0["text"] == "⭐"):
            self.P_amnt = self.round_decimals_down(float(self.principal.get()))
            self.b0["text"] = "★"
            self.principal["state"] = "disabled"
            self.lstbx["state"] = "normal"
            self.b1["state"] = "normal"
        else:
            self.b0["text"] = "⭐"
            self.principal["state"] = "normal"
            self.lstbx["state"] = "disabled"
            self.b1["state"] = "disabled"

    #####################################################################################################################

    def selected_tickers(self):
        self.chosen = [self.lstbx.get(i)[:7] for i in self.lstbx.curselection()] # Contains list of selected tickers
        j = 0
        l = 0
        self.b1["state"] = "disabled"
        self.b2["state"] = "normal"
        self.lbls = []
        self.txts = []

        for i in range(len(self.chosen)):
            if (self.chosen[i] not in self.past_state):
                self.lstbx1 = tk.Label(self, text=self.chosen[i])
                self.lstbx1.config(font=("",self.font_size-2,"bold"))
                self.sv = tk.StringVar()
                self.txtbx = tk.Text(self, height=1, width=5,background="yellow",
                                        highlightbackground="black", highlightthickness=2)
                k = 100+(i-j)*20
                if (k%800 == 0):
                    j = i
                    l += 1

                norm_x = (self.swpx*0.2222)+(self.swpx*0.0902778*l)
                norm_x1 = (self.swpx*0.277778)+(self.swpx*0.0902778*l)
                norm_y = (self.shpx*0.1111)+(i-j)*(self.shpx*0.02222)
                self.lstbx1.place(x=norm_x, y=norm_y)
                self.txtbx.place(x=norm_x1, y=norm_y)
                self.lbls.append(self.lstbx1)
                self.txts.append(self.txtbx)
        self.past_state = self.chosen

    #####################################################################################################################

    def del_selected_tickers(self):
        for lbl in self.lbls: lbl.destroy()
        for txt in self.txts: txt.destroy()
        if (self.lstbx["state"] == "normal"):
            self.b1["state"] = "normal"
        else:
            self.b1["state"] = "disabled"
        self.b2["state"] = "disabled"
        self.b3["state"] = "disabled"
        self.b4["state"] = "disabled"
        self.past_state = []
        self.count = 0.0
        self.wdgt_trackr = {}
        self.percent.set("0.0")
        self.header3.config(bg="red")


    ################################ START-READ/WRITE CSV ######################################################

    def read_csv(self, file):
        df = pd.read_csv(file, index_col = False)
        return df

    def write_csv(self, data, file):
        with open(file, 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(data)

    ################################ END-READ/WRITE CSV ########################################################

    def popup_window(self):
        window = tk.Toplevel()

        label = tk.Label(window, text="Trading Complete")
        label.pack(fill='x', padx=50, pady=5)

        button_close = tk.Button(window, text="Close", background="lightgray", command=window.destroy)
        button_close.pack(fill='x')

    def popup_window_validate(self):

        def set_default_values():
            self.delay = 25 #in seconds, maximum time to wait for the page to load
            self.offset = 5 #in seconds, the difference between delay and dt. Should always be > 0
            self.dt = self.delay + self.offset #in seconds, the time between ticker updates
            self.sample_steps = 5
            self.iterations = 10

            self.price_drop_percent = -15
            self.WAZIR_X_charge_per_transaction = 0.2
            self.max_profit_per = 100 #100%
            self.min_profit_per = 10 #10%

        def set_new_values():
            self.delay = int(var1.get()) #in seconds, maximum time to wait for the page to load
            self.offset = int(var2.get()) #in seconds, the difference between delay and dt. Should always be > 0
            self.dt = self.delay + self.offset #in seconds, the time between ticker updates
            self.sample_steps = int(var3.get())
            self.iterations = int(var4.get())

            self.price_drop_percent = float(var5.get())
            self.WAZIR_X_charge_per_transaction = float(var6.get())
            self.max_profit_per = float(var7.get())
            self.min_profit_per = float(var8.get())

        def contin():
            self.active()
            window1.destroy()

            
        window1 = tk.Toplevel(bg="lightgray")
        window1.resizable(False, False)

        var1 = tk.StringVar()
        var2 = tk.StringVar()
        var3 = tk.StringVar()
        var4 = tk.StringVar()
        var5 = tk.StringVar()
        var6 = tk.StringVar()
        var7 = tk.StringVar()
        var8 = tk.StringVar()
        
        tk.Label(window1, text="WebDriver waiting time [WDwt] (in seconds)", font=("",self.font_size,"bold"), bg="lightgray").pack()
        E1 = tk.Entry(window1, textvariable=var1).pack()
        var1.set(self.delay)
        var1.set(var1.get())

        tk.Label(window1, text="", height=1, bg="lightgray").pack()
        
        tk.Label(window1, text="Offset from WDwt (in seconds)", font=("",self.font_size,"bold"), bg="lightgray").pack()
        E2 = tk.Entry(window1, textvariable=var2).pack()
        var2.set(self.offset)
        var2.set(var2.get())

        tk.Label(window1, text="", height=1, bg="lightgray").pack()
        
        tk.Label(window1, text="Number of sampling steps", font=("",self.font_size,"bold"), bg="lightgray").pack()
        E3 = tk.Entry(window1, textvariable=var3).pack()
        var3.set(self.sample_steps)
        var3.set(var3.get())

        tk.Label(window1, text="", height=1, bg="lightgray").pack()
        
        tk.Label(window1, text="Number of trading cycles", font=("",self.font_size,"bold"), bg="lightgray").pack()
        E4 = tk.Entry(window1, textvariable=var4).pack()
        var4.set(self.iterations)
        var4.set(var4.get())

        tk.Label(window1, text="", height=1, bg="lightgray").pack()

        tk.Label(window1, text="Emergency minimum loss sell (in %)", font=("",self.font_size,"bold"), bg="lightgray").pack()
        E5 = tk.Entry(window1, textvariable=var5).pack()
        var5.set(self.price_drop_percent)
        var5.set(var5.get())

        tk.Label(window1, text="", height=1, bg="lightgray").pack()

        tk.Label(window1, text="Charge per transaction (in %)", font=("",self.font_size,"bold"), bg="lightgray").pack()
        E6 = tk.Entry(window1, textvariable=var6).pack()
        var6.set(self.WAZIR_X_charge_per_transaction)
        var6.set(var6.get())

        tk.Label(window1, text="", height=1, bg="lightgray").pack()

        tk.Label(window1, text="Maximum expected profit (in %)", font=("",self.font_size,"bold"), bg="lightgray").pack()
        E7 = tk.Entry(window1, textvariable=var7).pack()
        var7.set(self.max_profit_per)
        var7.set(var7.get())

        tk.Label(window1, text="", height=1, bg="lightgray").pack()

        tk.Label(window1, text="Minimum expected profit (in %)", font=("",self.font_size,"bold"), bg="lightgray").pack()
        E8 = tk.Entry(window1, textvariable=var8).pack()
        var8.set(self.min_profit_per)
        var8.set(var8.get())

        b_def = tk.Button(window1, text="Set default values", width=14, height=2,
                          command=set_default_values)
        b_def.pack()
        b_new = tk.Button(window1, text="Set new values", width=14, height=2,
                          command=set_new_values)
        b_new.pack()
        b_ok = tk.Button(window1, text="Continue", width=14, height=2,
                          command=contin)
        b_ok.pack()


    ################################ START-BUY/SELL ROUTINE ####################################################

    def load_bsr(self, num, price, date, threshold, variance, per_change):
        print('Ticker: {}'.format(self.price_book[num].name))

        name = self.price_book[num].name
        principal = self.price_book[num].principal
        buy =  self.price_book[num].buy
        buy_time = self.price_book[num].buy_time
        gain = self.price_book[num].gain
        buy_count = self.price_book[num].buy_count

        if (len(buy) != 0):
            trading_price = principal + (principal * per_change)
        else:
            trading_price = principal

        trading_price = self.round_decimals_down(trading_price)

        transaction_cost = self.WAZIR_X_charge_per_transaction * 0.01 * trading_price


        def buy_routine(price, time, transaction_cost):
            delta = price - transaction_cost
            buy.append(self.round_decimals_down(delta))
            buy_time.append(time)
            ids = self.price_book[num].name + str(self.glob_counter) + "buy"
            self.bsgl.insert("", index="end", iid=ids, text="",
                             values=(self.price_book[num].name, time, buy[0],
                                     "-", "-", "-"), tag="green")
            return buy[0]
    
        def sell_routine(price, min_buy, transaction_cost):
            profit = (price - min_buy - transaction_cost)
            print(profit, price, min_buy, transaction_cost)
            return (self.round_decimals_down(profit))


        var1 = -1
        var2 = 1

        min_threshold = var1 * variance
        max_threshold = var2 * variance


        # Selling any buys with sufficient profits
        if (len(buy) != 0 and trading_price >= buy[0] * (1 + self.max_profit_per * 0.01)):
            gain = sell_routine(trading_price, buy[0], transaction_cost)
            trading_price += gain  # Remove when updating from the website
            self.write_csv([buy_time[0], buy[0], date,
                            trading_price, gain], 'bs_{}.csv'.format(name))
            ids = self.price_book[num].name + str(self.glob_counter) + "sell0"
            self.bsgl.insert("", index="end", iid=ids, text="",
                             values=(self.price_book[num].name, buy_time[0], buy[0],
                                     date, trading_price-gain, gain), tag="red")
            del(buy_time[0])
            del(buy[0])

        # Price is dropping fast. Sell max buy at min loss
        if (len(buy) != 0 and trading_price < (buy[0] * (1 + self.price_drop_percent * 0.01))):
            gain = sell_routine(trading_price, buy[0], transaction_cost)
            trading_price += gain  # Remove when updating from the website
            self.write_csv([buy_time[0], buy[0], date, trading_price, gain],
                        'bs_{}.csv'.format(name))
            ids = self.price_book[num].name + str(self.glob_counter) + "sell1"
            self.bsgl.insert("", index="end", iid=ids, text="",
                             values=(self.price_book[num].name, buy_time[0], buy[0],
                                     date, trading_price-gain, gain), tag="red")
            del(buy_time[0])
            del(buy[0])

        # Initiate a buy
        if (len(buy) == 0 and threshold < min_threshold):
            trading_price = buy_routine(trading_price, date, transaction_cost)
            buy_count += 1
            self.write_csv([date, trading_price, price, 'NaN', 'NaN'],
                        'bs_{}.csv'.format(name))
                         
        # Initiate a sell
        if (len(buy) != 0 and threshold > max_threshold):
            min_target = buy[0] * (1 + self.min_profit_per * 0.01)       
            if (trading_price >= min_target):
                gain = sell_routine(trading_price, buy[0], transaction_cost)
                trading_price += gain  # Remove when updating from the website
                self.write_csv([buy_time[0], buy[0], date, trading_price-gain, gain],
                        'bs_{}.csv'.format(name))
                ids = self.price_book[num].name + str(self.glob_counter) + "sell2"
                self.bsgl.insert("", index="end", iid=ids, text="",
                             values=(self.price_book[num].name, buy_time[0], buy[0],
                                     date, trading_price-gain, gain), tag="red")
                del(buy_time[0])
                del(buy[0])
        
                
        self.price_book[num].principal = trading_price
        self.price_book[num].buy = buy
        self.price_book[num].buy_time = buy_time
        self.price_book[num].gain = gain
        self.price_book[num].buy_count = buy_count

    ################################ END-BUY/SELL ROUTINE #####################################################

    def round_decimals_down(self, number:float, decimals:int=2):
        """
        Returns a value rounded down to a specific number of decimal places.
        """
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more")
        elif decimals == 0:
            return math.floor(number)

        factor = 10 ** decimals
        return (math.floor(number * factor) / factor)

    #####################################################################################################################    

    def trading_routine(self):

        if (self.STATE == 0):
            self.lstbx["state"] = "disabled"
            self.principal["state"] = "disabled"
            self.b1["state"] = "disabled"
            self.b2["state"] = "disabled"
            self.b3["state"] = "disabled"
            self.b4["state"] = "disabled"

            for i in range(len(self.txts)):
                self.txts[i]["state"] = "disabled"
                self.txts[i]["bg"] = "lightgray"
            
            self.percent_change = 0 
            self.reset_counter = 0
            self.port = 0.0
            self.price_book = []
            self.Pamounts = [] # Principal amount per ticker 

            for i in range(len(self.chosen)):
                if (i == 0):
                    tmp_var = self.P_amnt * self.wdgt_trackr[".!text"] * 0.01 # 0.01 for converting the input to %
                else:
                    tmp_var = self.P_amnt * self.wdgt_trackr[".!text{}".format(i+1)] * 0.01

                self.Pamounts.append(self.round_decimals_down(tmp_var))

            for i in range(len(self.chosen)):
                self.price_book.append(Stocks(self.chosen[i], self.sample_steps, self.Pamounts[i], 0))

            self.STATE = 1
        
        else:
            self.glob_counter += 1
            self.reset_counter += 1
            self.now = datetime.now()
            self.time = self.now.strftime("%d/%m/%Y %H:%M:%S")

            for i in range(len(self.chosen)):
                if (self.glob_counter <= self.sample_steps):
                    index = self.tickers.index(self.chosen[i].replace(" ", ""))
                    self.price_book[i].price_manager(self.prices[index], (self.sample_steps-self.reset_counter))
                    self.port += self.price_book[i].principal
        
                else:
                    index = self.tickers.index(self.chosen[i].replace(" ", ""))
                    self.loc_avg = sum(self.price_book[i].price[:])/self.sample_steps
                    self.diff = (self.prices[index] - self.loc_avg)/self.loc_avg
                    
                    # Solving issues with parity
                    if (abs(self.diff) > 0.1):
                        self.prices[index] = self.price_book[i].previous_price
                        self.diff = (self.prices[index] - self.loc_avg)/self.loc_avg
                        
                    self.variance = pow((self.diff * self.loc_avg), 2)/self.sample_steps
                    
                    try:
                        self.percent_change = (self.prices[index] - self.price_book[i].previous_price)/self.price_book[i].previous_price
                    except:
                        self.percent_change = 0

                    self.load_bsr(i, self.prices[index], self.time, self.diff, self.variance, self.percent_change)
                    self.price_book[i].price_manager(self.prices[index], (self.sample_steps-self.reset_counter))
                    self.price_book[i].previous_price = self.prices[index]

                    # Writing to CSV file
                    self.write_csv([self.time, self.prices[index], self.price_book[i].gain], '{}.csv'.format(self.price_book[i].name))
                    self.price_book[i].gain = 0.0

                    # Calculating the portfolio amount
                    self.port += self.price_book[i].principal

            # Updating the portfolio label
            self.tprice.set("₹ {}".format(str(round(self.port, 2))))
            self.port = 0.0

            if (self.glob_counter % self.sample_steps == 0):
                self.reset_counter = 0
                
    #####################################################################################################################
    
    def update_list(self):
        if (self.glob_counter == self.iterations-1):
            self.after_cancel(self.loop_bsr)
        if (self.glob_counter == self.iterations):
            self.popup_window()
            self.STATE = 0
            self.principal["state"] = "normal"

        if (self.STATE == 1):
            self.loop_bsr = self.after(self.dt*1000, self.trading_routine)
        
        Thread(target=self.selenium_run(Thread, driver, url, self.delay, self.tick_var)).start()

        self.loop = self.after(self.dt*1000, self.update_list)

    #####################################################################################################################
    
    def selenium_run(self, Thread, driver, url, delay, tick_var):
        driver.get(url)
        try:
            myElem = WebDriverWait(driver, delay)\
                    .until(EC.presence_of_element_located((By.CLASS_NAME, 'price-text')))
            print('Loading succesful!')

            self.prices = [x.text for x in driver.find_elements_by_class_name('price-text')]
            self.prices = [price.replace(",","") for price in self.prices]
            self.prices = [float(price[1:]) for price in self.prices]
            self.tickers = [x.text for x in driver.find_elements_by_class_name('market-name-text')]
            self.tickers = [ticker[:len(ticker)-4] for ticker in self.tickers]

            sort_index = np.argsort(self.tickers)
            self.tickers = sorted(self.tickers)
            self.prices = [self.prices[i] for i in sort_index]
        
        except TimeoutException:
            print('Loading took too much time!')

        tic = []
        for i in range(len(self.tickers)):
            spacing = " " * (15 - len(self.tickers[i]))
            temp = " " + self.tickers[i] + spacing + "₹ " + str(self.prices[i])
            tic.append(temp)
        self.tick_var.set(tic)


################################ START-MAIN ################################################################
if __name__ == "__main__":

    url = "https://wazirx.com/exchange/BTC-INR"

    path = os.getcwd()

    try:
        os.makedirs("CSV_FILES")
        os.chdir(path + "/CSV_FILES")
    except FileExistsError:
        os.chdir(path + "/CSV_FILES")

    start_time = datetime.now().strftime("%d%m%Y")
    path = os.getcwd()
    
    try:
        os.makedirs("{}".format(start_time))
        os.chdir(path + "/{}".format(start_time))
    except FileExistsError:
        os.chdir(path + "/{}".format(start_time))

    #Selenium headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chromedriv_location = ChromeDriverManager().install()
    driver = webdriver.Chrome(chromedriv_location, options=chrome_options)
    
    #Tkinter
    crypster = Crypster()
    
    # handle WM_DELETE_WINDOW event
    def handle_exit():
        # open a dialog
        if messagebox.askokcancel("Notice", "Are you sure to close the window"):
           # close the application
           driver.close()
           crypster.destroy()
           
    crypster.protocol("WM_DELETE_WINDOW", handle_exit)
    crypster.mainloop()


    
