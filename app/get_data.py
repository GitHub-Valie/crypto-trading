# import csv, json, talib
# import numpy as np
# from numpy import genfromtxt
import config as cf
# import pandas as pd
# import bt_db as db
import csv
from binance.client import Client

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

# def getData():
#     symbol = 'batbnb3m'

#     db.getKandles(symbol)
#     prices = pd.readcsv(f'C:/Users/Valentin/crypto_trading/{symbol}.txt', parse_dates=True)
#     list = []
#     for index, row in prices.iterrows():
#         list.append({
#             'time' : row['datetime'],
#             'open' : row['open'],
#             'high' : row['high'],
#             'low' : row['low'],
#             'close' : row['close']
#         })
#         return list
    
#     getData()

TRADE_SYMBOL = 'BATBNB'

candles = client.get_klines(
    symbol=TRADE_SYMBOL,
    interval=Client.KLINE_INTERVAL_3MINUTE
)

csvfile = open('{}_3minutes.csv'.format(TRADE_SYMBOL), 'w', newline='')

candlestick_writer = csv.writer(
    csvfile,
    delimiter=','
)

# for candlestick in candles:
#     print(candlestick)
#     candlestick_writer.writerow(candlestick)

# print(len(candles))

candlesticks = client.get_historical_klines(
    TRADE_SYMBOL,
    Client.KLINE_INTERVAL_3MINUTE,
    "1 Aug, 2020",
    "3 Sep, 2020"
)

for candlestick in candlesticks:
    candlestick_writer.writerow(candlestick)

csvfile.close()