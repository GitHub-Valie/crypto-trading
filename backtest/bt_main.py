import backtrader as bt
import backtrader.feeds as btfeeds
import pandas as pd
import bt_db as btdb
from config import binance
from bt_strategies import *
import matplotlib

# prices = pd.read_csv('', index_col='datetime', parse_dates=True)

# data = bt.feeds.PandasData(dataname=prices)

if __name__ == '__main__':
    startcash = 100

    print('\nCreating an instance of Cerebro ...')
    cerebro = bt.Cerebro()

    # crypto = input('\nChoose crypto pair from watchlist ' + str(binance['watchlist']) + ': ')
    crypto = 'BATBTC'
    btdb.getKandles(crypto)

    cerebro.optstrategy(
        GoldenCross,
        fast=range(180, 300, 20),
        slow=range(240, 720, 40)
    )

    prices = pd.read_csv(
        f'{crypto}.txt',
        index_col='datetime',
        parse_dates=True)

    data = bt.feeds.PandasData(dataname=prices)

    cerebro.adddata(data)

    cerebro.broker.setcash(startcash)

    # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    # cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    cerebro.broker.setcommission(commission=0.0)

    opt_runs = cerebro.run(optreturn=False)

    # Generate results list
    final_results_list = []
    for run in opt_runs:
        for strategy in run:
            value = round(strategy.broker.get_value(), 2)
            PnL = round(value - startcash, 2)
            slow = strategy.params.slow
            fast = strategy.params.fast
            final_results_list.append([slow, fast, PnL])

    # Sort Results List
    by_PnL = sorted(final_results_list, key=lambda x: x[2], reverse=True)

    # Print results
    # print('\nResults: Ordered by period:')
    # for result in by_period:
    #     print('Period: {}, PnL: {}'.format(result[0], result[1]))
    print('\nResults: Ordered by Profit:')
    for result in by_PnL:
        print('slow_ma: {} / fast_ma: {} / PnL: {}'.format(result[0], result[1], result[2]))

    print(by_PnL)

    # results = pd.DataFrame(by_PnL)

    # print('\nStarting Portfolio Value: $ %.6f' % cerebro.broker.getvalue())

    # print('\nFinal Portfolio Value: $ %.6f' % cerebro.broker.getvalue())

    # cerebro.plot(style='candlestick')

