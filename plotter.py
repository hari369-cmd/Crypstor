import os
import csv
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

tickers = ["ALPHA"]
datetime = "22092021"

tick_files = [" " + i + (6-len(i))*" " + ".csv" for i in tickers]
bs_files = ["bs_ " + i + (6-len(i))*" " + ".csv" for i in tickers]

try:
    path = os.getcwd() + "/CSV_FILES" + "/" + datetime
    os.chdir(path)
except FileExistsError:
    pass


for i in range(len(tickers)):
    try:
        tick_df = pd.read_csv(tick_files[i], header=None, index_col=False)
        bs_df = pd.read_csv(bs_files[i], header=None, index_col=False)
    except FileExistsError:
        pass

    time = list(tick_df[:][0])
    price = list(tick_df[:][1])
    gain = list(tick_df[:][2])
    b_time = list(bs_df[:][0])
    s_time = list(bs_df[:][2])
    

    fig, ax = plt.subplots()
    plt.plot(time, price, "-", color="blue")
    
    # Green - buy, Red - sell, Blue - price
    for j in range(len(b_time)):
        index = time.index(b_time[j])
        plt.plot(b_time[j], price[index], "o", color="green")

    for j in range(len(s_time)):
        try:
            index = time.index(s_time[j])
            plt.plot(s_time[j], price[index], "o", color="red")
        except:
            pass


    every_nth = 10
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    plt.xticks(rotation=45)
    plt.show()
    
    
