from pymongo import MongoClient
import config as cf

url = 'mongodb://'
if cf.mongodb['user'] and cf.mongodb['passwd']:
    url += cf.mongodb['user'] + ':' + cf.mongodb['passwd'] + '@'
url += cf.mongodb['host']
client = MongoClient(url)
db = client[cf.mongodb['db']]
from datetime import datetime


# def isEmpty(symbol):
#     collection = db[symbol]
#     return collection.find_one() is None


def getLastKandle(symbol):
    collection = db[symbol]
    cursor = list(collection.find().sort('openTime', -1).limit(1))
    if len(cursor):
        return cursor[0]['closeTime']
    return 0


def insertKandles(symbol, kandlelist):
    collection = db[symbol]
    for kandle in kandlelist:
        ot = kandle['openTime']
        kandle['datetime'] = datetime.fromtimestamp(int(ot / 1000))
    collection.insert_many(kandlelist)
