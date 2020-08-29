from binance.client import Client
import config as cf
import src.db as db
from threading import Thread
import math
import time

client = Client(cf.binance['public_key'], cf.binance['secret_key'])


def getKline(symbol, start, stop):
    klines = client.get_historical_klines(
        symbol,
        Client.KLINE_INTERVAL_15MINUTE,
        start,
        stop
    )

    liste = []

    for kl in klines:
        liste.append(
            {
                'symbol': symbol,
                'openTime': kl[0],
                'open': kl[1],
                'high': kl[2],
                'low': kl[3],
                'close': kl[4],
                'volume': kl[5],
                'closeTime': kl[6],
                'quoteAssetVolume': kl[7],
                'nbTrade': kl[8],
                'takerBuyBaseAssetVolume': kl[9],
                'takerBuyQuoteAssetVolume': kl[10]
            }
        )
    return liste


class extract(Thread):
    def __init__(self, symbol, start, stop):
        Thread.__init__(self)
        self.symbol = symbol
        self.timestart = start
        self.timestop = stop

    def run(self):
        tmp = getKline(self.symbol, self.timestart, self.timestop)
        if len(tmp):
            db.insertKandles(self.symbol, tmp)


def startExtract(symbol):

    threadList = []
    print('Extraction ' + symbol)
    lastkandle = db.getLastKandle(symbol)

    if lastkandle:
        initdate = lastkandle + 1

    else:
        firstTrade = client.get_historical_trades(symbol=symbol, fromId=1)[0]['time'] // 1000 // 3600 * 3600
        initKline = client.get_historical_klines(
            symbol,
            client.KLINE_INTERVAL_15MINUTE,
            (firstTrade - 3600) * 1000,
            firstTrade * 1000
        )

        initdate = (firstTrade - 3600) * 1000

        while len(initKline):
            firstTrade -= 3600
            initdate = initKline[0][0]
            initKline = client.get_historical_klines(
                symbol,
                client.KLINE_INTERVAL_15MINUTE,
                (firstTrade - 3600) * 1000,
                firstTrade * 1000
            )
    dayNb = math.ceil((time.time() * 1000 - initdate) / 86400000)

    for x in range(0, dayNb):
        start = initdate + x * 86400000
        stop = start + 86340000
        threadList.append(extract(symbol, start, stop))

    for index, thread in enumerate(threadList):
        thread.start()
        time.sleep(0.195)
        print(f' {index + 1}/{dayNb} jours', end='\r')

    for thread in threadList:
        thread.join()
