from flask import Flask, render_template
import jsonify, itertools

import pandas as pd
import config as cf ,csv
from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import *

app = Flask(__name__)

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

@app.route('/')
def index ():
    title = 'Index'
    my_balance = []
    account = client.get_account()
    balance = account['balances']

    for x in balance:
        if (x['free'] != '0.00000000') and (x['free'] != '0.00'):
            my_balance.append({'Assets': x['asset'],
                               'Free': x['free'],
                               'Symbol': x['asset'] + "USDT",
                               'Value': "0"}
                              )
    my_total = 0
    for index in range(len(my_balance)):
        try:
            value = client.get_avg_price(symbol=my_balance[index]['Symbol'])
            tmp= float(value['price']) * float(my_balance[index]['Free'])
            my_total += tmp
            my_balance[index]['Value'] = round(tmp,2)
            my_balance[index]['Free'] = round(float(my_balance[index]['Free']),4)
        except:
            tmp = float(my_balance[index]['Free'])
            my_total += tmp
            my_balance[index]['Value'] = round(tmp, 2)
            my_balance[index]['Free'] = round(float(my_balance[index]['Free']), 4)

    my_total = round(my_total,2)
    return render_template(
        'index.html', 
        title=title,
        my_balance=my_balance,
        my_total=my_total
    )


# @app.route('/market')
# def Market ():
#     title = 'Market'
#     return render_template('market.html', title=title)

# @app.route('/history')
# def History ():
#     title = 'Historical Trades'
#     account_future = client.futures_exchange_info()
#     liste_trades_future = []
#     account_future = account_future['symbols']
#     for index in range(len(account_future)):
#         trades_future = client.futures_account_trades(symbol=account_future[index]['symbol'],startTime = 1598257547000 ) #,startTime = 1597622400
#         for index in range(len(trades_future)):
#             try:
#                 liste_trades_future.append({'Symbol': trades_future[index]['symbol'],
#                                             'Side': trades_future[index]['side'],
#                                             'Price': trades_future[index]['price'],
#                                             'Quantity': trades_future[index]['qty'],
#                                             'PNL': trades_future[index]['realizedPnl'],
#                                             'Time': trades_future[index]['time']})
#             except:
#                 pass
#     PNL = []
#     for key, group in itertools.groupby(liste_trades_future, lambda item: item["Symbol"]):
#         new_dict = {}
#         new_dict['Symbol'] = key
#         new_dict['PNL'] = round(sum([float(item["PNL"]) for item in group]),2)
#         PNL.append(new_dict)
#     return render_template('history.html', title=title, futur_trades = liste_trades_future, PNL = PNL)




if __name__ == "__main__":
    # app.run(host='localhost', debug=False)

    app.run(debug=True)
