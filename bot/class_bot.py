from binance.client import Client
import config as cf

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

class bot:
    def __init__(self, symbol, fast, slow, leverage, percentage, precision):
        self.symbol = symbol
        self.fast = fast
        self.slow = slow
        self.leverage = leverage
        self.percentage = percentage
        self.precision = precision
        self.time_open = 0
        self.fees_open = 0
        self.fees_close = 0 
        self.fees_total = 0
        self.price_open = 0
        self.price_close = 0
        self.data = []
        self.position = 0
        self.qtity = 0
        self.pnl = 0
        klines = client.get_klines(
            symbol = symbol,
            interval = Client.KLINE_INTERVAL_1MINUTE
        )
        for index in range(len(klines)):
            if len(self.data) < self.slow:
                self.data.append({
                    'time_open' : klines[index][0],
                    'open' : klines[index][1],
                    'high' : klines[index][2],
                    'med' : (float(klines[index][2]) + float(klines[index][3])) / 2,
                    'low' : klines[index][3],
                    'close' : klines[index][4],
                    'time_close' : klines[index][6]
                })
            else:
                self.data.append({
                    'time_open' : klines[index][0],
                    'open' : klines[index][1],
                    'high' : klines[index][2],
                    'med' : (float(klines[index][2]) + float(klines[index][3])) / 2,
                    'low' : klines[index][3],
                    'close' : klines[index][4],
                    'time_close' : klines[index][6]
                })

def next(self, kline):
    if kline['t'] != self.data[-1]['time_open']:
        self.data.pop(0)
        self.data.append({
            'time_open' : kline['t'],
            'open' : kline['o'],
            'high' : kline['h'],
            'med' : (float(kline['h']) + float(kline['l'])) / 2,
            'low' : kline['l'],
            'close' : kline['c'],
            'time_close' : kline['T']
        })
    
    else:
        self.data[-1] = {
            'time_open' : kline['t'],
            'open' : kline['o'],
            'high' : kline['h'],
            'med' : (float(kline['h']) + float(kline['l'])) / 2,
            'low' : kline['l'],
            'close' : kline['c'],
            'time_close' : kline['T']
        }