# -*- coding: utf-8 -*-
import datetime
from mimetypes import init  # For datetime objects
import os.path
from select import select  # To manage paths
import sys
from turtle import color, colormode
# from tkinter.constants import S  # To find out the script name (in argv[0])
import tushare as ts
import backtrader as bt
import backtrader.feeds as btfeeds



class mmStrategy(bt.Strategy):
    print("建立策略mmStrategy")
    params = (('p1', 5), ('p2', 12), ('p3', 30), ('size', 700))

    def __init__(self):
        self.order = None
        # self.sma1 = bt.ind.SMA(period=self.params.p1)
        # self.sma2 = bt.ind.SMA(period=self.params.p2)
        # self.sma3 = bt.ind.SMA(period=self.params.p3)
        self.b_top = bt.ind.BollingerBands().top
        self.b_mid = bt.ind.BollingerBands().mid
        self.b_bot = bt.ind.BollingerBands().bot
        self.close = self.datas[0].close
        self.high = self.datas[0].high
        self.low = self.datas[0].low

        self.dt = self.datas[0].datetime

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.low <= self.b_bot:
                # 执行买入
                self.order = self.buy(size=self.params.size)
        else:
            if self.high >= self.b_top:
                # 执行卖出
                self.order = self.sell(size=self.params.size)

        self.order = None

    def log(self, txt, dt=None):
        ''' 记录'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        # if order.status in [order.Submitted, order.Accepted]:
        #     # Buy/Sell order submitted/accepted to/by broker - Nothing to do
        #     return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    # def notify_trade(self, trade):
    #     if not trade.isclosed:
    #         return

    #     self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
    #              (trade.pnl, trade.pnlcomm))


if __name__ == '__main__':
    ai = len(sys.argv)
    print("............参数个数{}".format(ai))
    if ai < 2:
        print("需要stockid，如：600031.sh或者300348.sz")
        sys.exit()
    stockid_input = sys.argv[1]
    print("............股票代码{}...............".format(stockid_input))
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    STOCKID = stockid_input
    datapath = os.path.join(modpath, '{}.csv'.format(STOCKID))
    print("............读取文件{}".format(datapath))
    data = btfeeds.YahooFinanceCSVData(dataname=datapath,
                                       fromdate=datetime.datetime(1995, 1, 1),
                                       todate=datetime.datetime(2022, 12, 31),
                                       reverse=False)
    print('............开始测试...........')
    cc = bt.Cerebro()
    cc.adddata(data)
    cc.addstrategy(mmStrategy)
    cc.getbroker().set_cash(100000)
    cc.getbroker().setcommission(0.002)
    cc.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')
    # cc.addsizer(bt.sizers.FixedSize, stake=1000)
    startMoney = cc.getbroker().getvalue()
    print('开始金额: %.2f' % startMoney)
    cc.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio')
    cc.addanalyzer(bt.analyzers.DrawDown, _name='DW')
    cc.addanalyzer(bt.analyzers.)
    results=cc.run()
 
    strat = results[0]
    endMoney = cc.getbroker().getvalue()
    vMoney = endMoney-startMoney
    vPercent = vMoney/startMoney
    print('最终金额: %.2f' % endMoney)
    print('盈亏金额: %.2f' % vMoney)
    print('盈亏百分比: {:.2%}  '.format(vPercent))

    print('夏普比率:', strat.analyzers.SharpeRatio.get_analysis())
    print('回撤指标:', strat.analyzers.DW.get_analysis())
    cc.plot(style='bar')
