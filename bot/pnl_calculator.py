from binance.client import Client
import config as cf

TRADE_SYMBOL = 'BNBBTC'
BASE_ASSET = 'BNB'
QUOTE_ASSET = 'BTC'

buy_total = []
sell_total = []
order_buy_id = []
order_sell_id = []

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

base_asset_balance = client.get_asset_balance(
    asset=BASE_ASSET
)

quote_asset_balance = client.get_asset_balance(
    asset=QUOTE_ASSET
)

get_orders = client.get_all_orders(
    symbol=TRADE_SYMBOL
)

my_trades = client.get_my_trades(
    symbol=TRADE_SYMBOL
)

print("{} TRADES ON {} ".format(len(get_orders), TRADE_SYMBOL))

for order in get_orders:
    if order['side'] == 'BUY':
        order_buy_id.append(order['orderId'])
        for trade in my_trades:
            if trade['orderId'] == order['orderId']:
                net_buy = float(trade['price']) + float(trade['commission'])
                buy_total.append(net_buy)
                # print('Order ID {} is a BUY:    {}'.format(trade['orderId'], net_buy))
    else:
        order_sell_id.append(order['orderId'])
        for trade in my_trades:
            if trade['orderId'] == order['orderId']:
                net_sell = float(trade['price']) - float(trade['commission'])
                sell_total.append(net_sell)
                # print('Order ID {} is a SELL:   {}'.format(trade['orderId'], net_sell))

TOTAL_BUY = sum(buy_total)
TOTAL_SELL = sum(sell_total)
PNL = TOTAL_SELL - TOTAL_BUY
print("PNL:        ", round(PNL, 10))
print("{} Balance:  {}".format(base_asset_balance['asset'], base_asset_balance['free']))
print("{} Balance:  {}".format(quote_asset_balance['asset'], quote_asset_balance['free']))