# -*- coding: utf-8 -*-
import datetime
from mimetypes import init  # For datetime objects
import os.path  # To manage paths
import sys
# from tkinter.constants import S  # To find out the script name (in argv[0])
import tushare as ts
import backtrader as bt
import backtrader.feeds as btfeeds


class mmStrategy(bt.Strategy):
    print("建立策略mmStrategy")
    parmes = {
        "fm": 10,
        "sm": 30,
        "sizes": 100
    }

    def __init__(self):
        self.order = None
        self.sma10 = bt.ind.SMA(period=10)
        self.sma30 = bt.ind.SMA(period=30)

    def next(self):
        if self.order:
            return
        # if self.position:
        #     return
        if self.sma10 >= self.sma30:
            self.order = self.buy()
        else:
            self.order = self.sell()

        self.order = None


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
    cc.getbroker().set_cash(10000)
    cc.getbroker().setcommission(0.002)
    startMoney = cc.getbroker().getvalue()
    print('开始金额: %.2f' % startMoney)
    cc.run()
    endMoney = cc.getbroker().getvalue()
    vMoney = startMoney - endMoney
    vPercent = vMoney/startMoney
    print('最终金额: %.2f' % endMoney)
    print('盈亏金额: %.2f' % vMoney)
    print('盈亏百分比: {:.2%}  '.format(vPercent))
    cc.plot()
