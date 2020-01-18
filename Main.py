import datetime
import quandl
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from GKYZ import get_estimator

plt.style.use('ggplot')
ENX = ['ING', 'KER', 'UNA', 'FR', 'CO']


# %% Calculate Window Lengths
def calculate_windows():
    windows = []
    today = datetime.date.today()
    expirations = [
        '2020-01-17',
        '2020-02-21',
        '2020-03-21',
        '2020-06-19',
        '2020-09-18',
        '2020-12-18'
    ]
    a = [datetime.datetime.strptime(x, '%Y-%m-%d').date() for x in expirations]
    for i in a:
        delta = (i - today).days
        windows.append(delta)
    return windows


windows = calculate_windows()


# %% Get PX Data
def get_data(stock):
    stock_name = "EURONEXT/{}".format(stock)
    mydata = quandl.get(stock_name, authtoken="TgiANGGcp_jCvz9gQWmx").drop(columns=['Turnover', 'Volume'])
    newdata = pd.DataFrame(mydata)
    newdata.loc[:, 'symbol'] = stock
    newdata.reset_index(drop=True)
    return newdata


def combine_data():
    prices = {}

    for i in ENX:
        prices[i] = get_data(i)

    price_data_combined = pd.concat(prices)
    return price_data_combined


price_data_combined = combine_data()



# %% Calculate HVGs
def calc_vols(data):
    window_list = {}
    for w in windows:
        window_list[w] = get_estimator(data, w)

    window_list = pd.DataFrame(window_list)
    vols = price_data_combined.join(window_list)
    return vols


vols = calc_vols(price_data_combined)


