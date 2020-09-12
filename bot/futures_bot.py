from binance.client import Client
import config_futures as cff
import json, websocket

client = Client(
    cff.binance['futures_key'],
    cff.binance['futures_secret']
)

TRADE_SYMBOL = 'ETHUSDT'
SOCKET = "wss://fstream3.binance.com/stream?streams={}@kline_1m".format(TRADE_SYMBOL.lower())

closes = []

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
    # print(candle)
    is_candle_closed = candle['x']
    close = candle['c']
    print(
        candle['s'],
        "\nopen:      ", candle['o'],
        "\nhigh:      ", candle['h'],
        "\nlow:       ", candle['l'],
        "\nclose:     ", close,
        "\nvolume:    ", candle['v']
    )

    if is_candle_closed:
        print("\nCANDLE CLOSED AT {:.8f}".format(float(close)))
        closes.append(float(close))
        print("\nCLOSES")
        print(closes)

    # INSERT STRATEGY HERE
 
ws = websocket.WebSocketApp(
    SOCKET, 
    on_open=on_open,
    on_close= on_close, 
    on_message= on_message
)

while True:
    print("RECONNECTION")
    ws.run_forever()