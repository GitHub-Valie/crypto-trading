from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING
import config as cf
client = MongoClient(cf.mongodb['host'])

db = client[cf.mongodb['db']]

def db_insert(Symbol,Time_Open,Price_Open, Quantity, Side, Fees_Open):
    collection = db['bot_transaction']
    collection.insert_one({
        'symbol': Symbol, 
        'time_open':Time_Open,
        'price_open': Price_Open,
        'quantity': Quantity,
        'side': Side,
        'fees_entry': Fees_Open
    })

def db_update_tp(Symbol, Time_Open, Time_Close, Price_Close, Fees_Close, PNL):
    collection = db['bot_transaction']
    collection.update_one(
        {
            'symbol': Symbol,
            'time_open':Time_Open
        },{
            '$set':{
                'time_close_tp' : Time_Close,
                'price_Close_tp' : Price_Close,
                'fees_close_tp': Fees_Close,
                'pnl_tp' : PNL
            }
        }
    )

def db_update(Symbol, Time_Open, Time_Close, Price_Close, Fees_Close, PNL):
    collection = db['bot_transaction']
    collection.update_one(
        {
            'symbol': Symbol,
            'time_open':Time_Open
        },{
            '$set':{
                'time_close' : Time_Close,
                'price_Close' : Price_Close,
                'fees_close': Fees_Close,
                'pnl' : PNL
            }
        }
    )
