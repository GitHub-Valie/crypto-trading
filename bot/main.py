from binance.client import Client
import config as cf
import config_bot
import class_bot
import json, websocket, pprint, time

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

SOCKET = "wss://fstream3.binance.com/stream?streams="


bots = []
for bot in config_bot.bots:
    bots.append(bot)
    bots[-1]['bot'] = class_bot.bot(
        bot['pair'],
        bot['fast_trend'],
        bot['slow_trend'],
        bot['leverage'],
        bot['percentage'],
        bot['precision']
    )
    SOCKET+=bot['pair'].lower()+"@kline_1m/"

def on_open(ws):
    print("OPENED CONNECTION")

def on_close(ws):
    print("CLOSED CONNECTION")

def on_message(ws, message):
    print('RECEIVED MESSAGE')
    json_message = json.loads(message)
    data = json_message['data']['k']
    pprint.pprint(json_message)
    for bot in bots:
        if bot['pair'] == data['s']:
            bot['bot'].next(data)
            break

ws = websocket.WebSocketApp(
    SOCKET,
    on_open = on_open,
    on_close = on_close, 
    on_message = on_message
)

while True:
    print('RECONNECTION')
    ws.run_forever()