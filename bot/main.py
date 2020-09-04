from binance.client import Client
from binance.enums import *
import config as cf
import json, websocket, pprint, time, numpy, talib

numpy.set_printoptions(precision=8)

TRADE_SYMBOL = 'BATBNB'
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
FAST_SMA_PERIOD = 3
SLOW_SMA_PERIOD = 6
SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_3m".format(TRADE_SYMBOL.lower())
TRADE_QUANTITY = 12

closes = []
PNL = []
in_position = False

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("SENDING ORDER")
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )
        print(order)
    except Exception as e:
        print("EXCEPTION OCCURED - {}".format(e))
        return False
    return True

def on_open(ws):
    print("OPENED CONNECTION")

def on_close(ws):
    print("CLOSED CONNECTION")

def on_message(ws, message):
    global closes, in_position

    print('\nRECEIVED MESSAGE')
    json_message = json.loads(message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    print(
        json_message['s'],
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

        if len(closes) >= SLOW_SMA_PERIOD:
            float_data = [float(x) for x in closes]
            np_closes = numpy.array(float_data)
            fast_sma = talib.SMA(
                np_closes, 
                FAST_SMA_PERIOD
            )
            slow_sma = talib.SMA(
                np_closes, 
                SLOW_SMA_PERIOD
            )
            # rsi = talib.RSI(np_closes, RSI_PERIOD)
            LAST_FAST_SMA = fast_sma[-1]
            LAST_SLOW_SMA = slow_sma[-1]
            # last_rsi = rsi[-1]
            print(
                "\nCURRENT FAST SMA: {:.8f}".format(LAST_FAST_SMA),
                "\nCURRENT SLOW SMA: {:.8f}".format(LAST_SLOW_SMA)
                # "\nCURRENT RSI: {:.8f}".format(last_rsi)
            )

            # Golden Cross Strategy
            if LAST_FAST_SMA < LAST_SLOW_SMA:
                if in_position:
                    print('FAST SMA < SLOW SMA: SELL')
                    order_succeeded = order(
                        side=SIDE_SELL,
                        quantity=TRADE_QUANTITY,
                        symbol=TRADE_SYMBOL,
                        order_type=ORDER_TYPE_MARKET
                    )
                    if order_succeeded:
                        print('{} SELL ORDER SUCCESSFUL'.format(TRADE_SYMBOL))
                        in_position = False

                        get_orders = client.get_all_orders(
                            symbol=TRADE_SYMBOL
                        )

                        my_trades = client.get_my_trades(
                            symbol=TRADE_SYMBOL
                        )

                        LAST_ORDER = get_orders[-1]
                        LAST_ORDER_ID = LAST_ORDER['orderId']
                        LAST_ORDER_SIDE = LAST_ORDER['side']

                        SECOND_TO_LAST_ORDER = get_orders[-2]
                        SECOND_TO_LAST_ORDER_ID = SECOND_TO_LAST_ORDER['orderId']
                        SECOND_TO_LAST_ORDER_SIDE = SECOND_TO_LAST_ORDER['side']

                        LAST_TRADE = my_trades[-1]
                        LAST_TRADE_ID = LAST_TRADE['orderId']

                        SECOND_TO_LAST_TRADE = my_trades[-2]
                        SECOND_TO_LAST_TRADE_ID = SECOND_TO_LAST_TRADE['orderId']

                        # 1. Vérifier si les ID des ordres et des trades correspondent
                        if SECOND_TO_LAST_ORDER_ID == SECOND_TO_LAST_TRADE_ID and LAST_ORDER_ID == LAST_TRADE_ID:

                            # 2. Vérifier si le dernier trade est coté SELL et l'avant dernier côté BUY
                            if SECOND_TO_LAST_ORDER_SIDE == 'BUY' and LAST_ORDER_SIDE == 'SELL':
                                print('BUY-SELL CHECKED')

                                # 3. Calculer les prix d'achat et de vente en prenant en compte les commissions Binance
                                BUY_PRICE = float(SECOND_TO_LAST_TRADE['price'])
                                BUY_FEE = float(SECOND_TO_LAST_TRADE['commission'])

                                SELL_PRICE = float(LAST_TRADE['price'])
                                SELL_FEE = float(SECOND_TO_LAST_TRADE['commission'])

                                LAST_PNL = SELL_PRICE - SELL_FEE - (BUY_PRICE + BUY_FEE)
                                print('LAST PNL:            {}'.format(LAST_PNL))
                                PNL.append(LAST_PNL)
                                print('TOTAL PNL SO FAR:    {}'.format(sum(PNL)))                       
                else:
                    print('SHOULD SELL, BUT NO {} OWNED'.format(TRADE_SYMBOL))

            if LAST_FAST_SMA > LAST_SLOW_SMA:
                if in_position:
                    print('SHOULD BUY, BUT {} ALREADY OWNED'.format(TRADE_SYMBOL))
                else:
                    print('FAST SMA > SLOW SMA: BUY')
                    order_succeeded = order(
                        side=SIDE_BUY,
                        quantity=TRADE_QUANTITY,
                        symbol=TRADE_SYMBOL,
                        order_type=ORDER_TYPE_MARKET
                    )
                    if order_succeeded:
                        print('{} BUY ORDER SUCCESSFUL'.format(TRADE_SYMBOL))
                        in_position = True

while True:
    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()