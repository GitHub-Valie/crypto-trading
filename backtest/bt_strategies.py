import backtrader as bt
from datetime import datetime
import math


class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.6f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.6f' % order.executed.price)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):

        self.log('Close %.6f' % self.dataclose[0])
        if self.order:
            return

        if not self.position:

            if self.data.close[0] < self.data.close[-1]:

                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('BUY CREATE, %.6f' % self.data.close[0])
                    self.order = self.buy(exectype=bt.Order.Market)

        else:
            if self.data.close[0] > self.data.close[-1]:
                if self.data.close[-1] > self.data.close[-2]:
                    self.log('SELL CREATE, %.6f' % self.data.close[0])
                    self.order = self.sell(exectype=bt.Order.Market)


class GoldenCross(bt.Strategy):
    params = (
        ('fast', 7),
        ('slow', 24),
        ('order_percentage', 0.95)
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):

        self.fast_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.fast,
            plotname='fast MA'
        )

        self.slow_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.slow,
            plotname='slow MA'
        )
        self.crossover = bt.indicators.CrossOver(
            self.fast_moving_average,
            self.slow_moving_average
        )
        self.dataclose = self.datas[0].close # Keep a reference to the "close" line in the data[0] dataseries
        self.order = None # Property to keep track of pending orders.
        # There are no orders when the strategy is initialized.

    def notify_order(self, order):

        # 1. If order is submitted/accepted, do nothing
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 2. If order is BUY/SELL executed, report price executed
        if order.status in [order.Completed]:

            if order.isbuy():

                self.log('BUY EXECUTED, %.6f\n' % order.executed.price)

            elif order.issell():

                self.log('SELL EXECUTED, %.6f\n' % order.executed.price)

        # 3. Else, if order is canceled/margin/rejected, report order canceled
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
        self.dataclose = self.datas[0].close

    def next(self):

        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                # Log the closing prices of the series from the reference
                self.log('BUY CREATE, %.6f' % self.data.close[0])
                # print('BUY CREATE / qty: {} / price: {}'.format(self.size, self.data.close[0]))
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
                self.log('SELL CREATE, %.6f' % self.data.close[0])
                # print('SELL CREATE / qty: {} / price: {}'.format(self.size, self.data.close[0]))
                self.sell(size=self.size)
