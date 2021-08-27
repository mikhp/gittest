# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys
from tkinter.constants import S  # To find out the script name (in argv[0])
import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (('maperiod', 15), )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)
        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0],
                                            period=25,
                                            subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price, order.executed.value,
                          order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price, order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


class kdjStrategy(bt.Strategy):
    params = dict(
        fast_ma=2,
        slow_ma=5,
        rsi_period =5,
        rsi_high=60,
        rsi_low=50,
    )

    def __init__(self):
        self.order = None
        self.sma = bt.indicators.MovingAverageSimple(period=self.p.fast_ma)
        self.sma2 = bt.indicators.MovingAverageSimple(period=self.p.slow_ma)
        self.rsi = bt.indicators.RSI(period=self.p.rsi_period)
        # self.dataclose = self.datas[0].close
        # fast_ma = bt.ind.EMA(period=self.p.fast_ma)
        # slow_ma = bt.ind.EMA(period=self.p.slow_ma)
        self.crossover = bt.ind.CrossOver(self.sma,self.sma2)
      
        

        # print(self.datas[0])
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):

        if self.order:
            return

        if self.crossover < 0 and self.rsi < self.p.rsi_low:
            self.order = self.buy()
            
        elif self.crossover > 0 and self.rsi > self.p.rsi_high:
            self.order = self.sell()
            
            

        self.order = None

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('买入, %.2f' % order.executed.price)
            elif order.issell():
                self.log('卖出, %.2f' % order.executed.price)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("需要stockid，如：600031.sh或者300348.sz")
        sys.exit()

    stockid_input = sys.argv[1]

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(kdjStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    # datapath = os.path.join(modpath, 'orcl-1995-2014.txt')
    STOCKID = stockid_input
    datapath = os.path.join(modpath, '{}.csv'.format(STOCKID))

    # Create a Data Feed
    # Data Feeds, Indicators and Strategies have lines.A line is a succession of points that when joined together form this line. When talking about the markets,
    # a Data Feed has usually the following set of points per day:Open, High, Low, Close, Volume, OpenInterest

    print(datapath)
    # fromdate 要早于数据源开始时间  todate 要迟于数据源结束时间，否则报错 array assignment index out of range
    data = bt.feeds.YahooFinanceCSVData(dataname=datapath,
                                        fromdate=datetime.datetime(1995, 1, 1),
                                        todate=datetime.datetime(2022, 12, 31),
                                        reverse=False)
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    startmoney = 70000.0
    cerebro.broker.setcash(startmoney)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # Set the commission
    cerebro.broker.setcommission(commission=0.003)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('最终市值: %.2f' % cerebro.broker.getvalue())
    allmoney = cerebro.broker.getvalue() - startmoney
    print('最终盈利: %.2f' % allmoney)
    ab = float(allmoney / startmoney * 100)
    print('盈亏率: %.2f' % ab + '%')

    # Plot the result
    cerebro.plot()
