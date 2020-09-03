from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
import config as cf
import json, websocket, pprint, time, numpy, talib

numpy.set_printoptions(precision=8)

TRADE_SYMBOL = 'BATBTC'
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
FAST_SMA_PERIOD = 62
SLOW_SMA_PERIOD = 61
SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_5m".format(TRADE_SYMBOL.lower())
TRADE_QUANTITY = 0.05

closes = []
trades = []
in_position = False

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("SENDING ORDER")
        order = client.create_test_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity,
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
        print("\nCLOSES", "\n")
        print(closes)

        if len(closes) > SLOW_SMA_PERIOD:
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
                        SIDE_SELL,
                        TRADE_QUANTITY,
                        TRADE_SYMBOL
                    )
                    if order_succeeded:
                        print('{} SELL ORDER SUCCESSFUL'.format(TRADE_SYMBOL))
                        in_position = False
                else:
                    print('SHOULD SELL, BUT NO {} OWNED'.format(TRADE_SYMBOL))

                if LAST_FAST_SMA > LAST_SLOW_SMA:
                    if in_position:
                        print('SHOULD BUY, BUT {} ALREADY OWNED'.format(TRADE_SYMBOL))
                    else:
                        print('FAST SMA > SLOW SMA: BUY')
                        order_succeeded = order(
                            SIDE_BUY,
                            TRADE_QUANTITY,
                            TRADE_SYMBOL
                        )
                        if order_succeeded:
                            print('{} BUY ORDER SUCCESSFUL'.format(TRADE_SYMBOL))
                            in_position = True

            # RSI Strategy
            # if last_rsi > RSI_OVERBOUGHT:
            #     if in_position:
            #         print("Overbought! Sell! Sell! Sell!")
            #         # put binance sell logic here
            #         order_succeeded = order(
            #             SIDE_SELL, 
            #             TRADE_QUANTITY, 
            #             TRADE_SYMBOL
            #         )
            #         if order_succeeded:
            #             in_position = False
            #     else:
            #         print("It is overbought, but we don't own any. Nothing to do.")
            # if last_rsi < RSI_OVERSOLD:
            #     if in_position:
            #         print("It is oversold, but you already own it. Nothing to do.")
            #     else:
            #         print("Oversold! Buy! Buy! Buy!")
            #         # put binance buy order logic here
            #         order_succeeded = order(
            #             SIDE_BUY, 
            #             TRADE_QUANTITY,
            #             TRADE_SYMBOL
            #         )
            #         if order_succeeded:
            #             in_position = True

ws = websocket.WebSocketApp(
    SOCKET,
    on_open = on_open,
    on_close = on_close, 
    on_message = on_message
)

ws.run_forever()
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)