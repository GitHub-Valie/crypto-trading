from binance.client import Client
import config_futures as cff
import json, websocket

client = Client(
    cff.binance['futures_key'],
    cff.binance['futures_secret']
)

TRADE_SYMBOL = 'BNB'
SOCKET = "wss://fstream3.binance.com/stream?streams={}@kline_1m".format(TRADE_SYMBOL.lower())

# futures_account = client.futures_account()

# total_wallet_balance = futures_account['totalWalletBalance']
# # for x in futures_account:
# #     print(x)

# exchange_info = client.get_exchange_info()
# # for x in exchange_info:
# #     print(x)

# exchange_symbols = exchange_info['symbols']
# # print(exchange_info)

def on_open(ws):
    print("OPENED CONNECTION")

def on_close(ws):
    print("CLOSED CONNECTION")

def on_message(ws,message):
    global closes, in_position

    print('\nRECEIVED MESSAGE')
    json_message = json.loads(message)
    # print(json_message)
    data = json_message['data']
    candle = data['k']
    print(candle)
    # is_candle_closed = candle['x']
    # close = candle['c']
    # print(
    #     json_message['s'],
    #     "\nopen:      ", candle['o'],
    #     "\nhigh:      ", candle['h'],
    #     "\nlow:       ", candle['l'],
    #     "\nclose:     ", close,
    #     "\nvolume:    ", candle['v']
    # )
 
ws = websocket.WebSocketApp(
    SOCKET, 
    on_open=on_open,
    on_close= on_close, 
    on_message= on_message
)

while True:
    print("RECONNECTION")
    ws.run_forever()