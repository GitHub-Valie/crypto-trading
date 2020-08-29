from pymongo import MongoClient
import config as cf
import pandas as pd
import time
import matplotlib

url = 'mongodb://'

if cf.mongodb['user'] and cf.mongodb['passwd']:
    url += cf.mongodb['user'] + ':' + cf.mongodb['passwd'] + '@'

url += cf.mongodb['host']
client = MongoClient(url)
db = client[cf.mongodb['db']]


def makeTimeStat(start, message='Elapsed Time: '):
    d = time.time() - start
    display = message
    if d // 3600:
        display += str(d // 3600) + 'h '

    if d // 60:
        display += str(d // 60) + 'm '

    display += str(round(d % 60, 2)) + 's'
    print(display)


def getKandles(symbol, skip=0):
    start = time.time()
    collection = db[symbol]
    collection.create_index(
        [('openTime', 1)],
        name='sort_index'
    )
    cursor = list(
        collection.find(
            {},
            {
                '_id': False,
                'openTime': False,
                'symbol': False,
                'closeTime': False,
                'quoteAssetVolume': False,
                'nbTrade': False,
                'takerBuyBaseAssetVolume': False,
                'takerBuyQuoteAssetVolume': False
            }
        ).skip(skip).sort('openTime', 1)
    )
    makeTimeStat(
        start,
        '\nGet from db '
    )
    start = time.time()
    df = pd.DataFrame(cursor)
    makeTimeStat(
        start,
        'DateFrame from db list '
    )
    start = time.time()
    df.to_csv(
        f'{symbol}.txt',
        index=False
    )
    makeTimeStat(
        start,
        'Generate CSV '
    )
