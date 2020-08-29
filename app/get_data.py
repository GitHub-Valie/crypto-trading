import csv, json, talib
import numpy as np
from numpy import genfromtxt
import config as cf
import pandas as pd
import bt_db as db
from binance.client import Client

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

def getData():
    symbol = 'batbtc15m'

    db.getKandles(symbol)
    prices = pd.readcsv(f'C:/Users/Valentin/crypto_trading/{symbol}.txt', parse_dates=True)
    list = []
    for index, row in prices.iterrows():
        list.append({
            'time' : row['datetime'],
            'open' : row['open'],
            'high' : row['high'],
            'low' : row['low'],
            'close' : row['close']
        })
        return list
    
    getData()