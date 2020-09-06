from binance.client import Client
import config as cf

client = Client(
    cf.binance['public_key'],
    cf.binance['secret_key']
)

