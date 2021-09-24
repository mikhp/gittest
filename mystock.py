
#本文主要记录保护点卖出策略，给买入的股票设立保护点，随着股票收盘价的提升，保护点不断提高，股价一旦跌破保护点，即卖出股票。
# 示例的买入条件为，5日线金叉60日线，且股价进行小幅回踩（较金叉日收盘价下跌1%）。卖出条件为，股价跌破保护点。
# 保护点首先设置为买入当天收盘价减去一个资金回撤值（率），示例把回撤率设置为5%。后续如果股票的收盘价上升，
# 则用新的收盘价更新保护点，如果股票的收盘价下跌，则保留原有保护点。回测初始资金100000元，单笔操作单位1000股，
# 佣金千分之一
# ————————————————
# 版权声明：本文为CSDN博主「码农甲V」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/m0_46603114/article/details/105014498

# 创建策略
from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime  # 用于datetime对象操作
import os.path  # 用于管理路径
import sys  # 用于在argvTo[0]中找到脚本名称
import backtrader as bt # 引入backtrader框架

class St(bt.Strategy):
    params = dict(
        buy_limit_percent = 0.01,
        buy_valid_date = 5,
        stoptype=bt.Order.StopTrail,
        trailamount=0.0,
        trailpercent=0.05,
        p_high_period = 5,
        p_fast = 5,
        p_slow = 60,
    )
    def __init__(self):
        slowSMA = bt.ind.SMA(period = self.p.p_slow)
        self.buy_con = bt.And(
            bt.ind.CrossUp(
            bt.ind.SMA(period = self.p.p_fast), slowSMA),
            #slowSMA == bt.ind.Highest(slowSMA, period = self.p.p_high_period, plot = False)
        )
        self.order = None
    def notify_order(self, order):
        if order.status in [order.Completed]:
            print('Completed order: {}: Order ref: {} / Type {} / Status {} '.format(
                self.data.datetime.date(0),
                order.ref, 'Buy' * order.isbuy() or 'Sell',
                order.getstatusname()))
            self.order = None
        if order.status in [order.Expired]:
            self.order = None
        print('{}: Order ref: {} / Type {} / Status {}'.format(
            self.data.datetime.date(0),
            order.ref, 'Buy' * order.isbuy() or 'Sell',
            order.getstatusname()))
    def next(self):
        # 无场内资产
        if not self.position:
            # 未提交买单
            if None == self.order:
                # 金叉到达了买点
                if self.buy_con:
                    # 计算订单有效期时间，如果超过有效期，股价仍未回踩，则放弃下买入订单
                    valid = self.data.datetime.date(0)
                    if self.p.buy_valid_date:
                        valid = valid + datetime.timedelta(days=self.p.buy_valid_date)
                    # 计算回踩后的买入价格
                    price = self.datas[0].close[0] * (1.0 - self.p.buy_limit_percent)
                    print('Buy order created: {}: close: {} / limit price: {} / valid: {}'.format(
                        self.datetime.date(), self.datas[0].close[0], price, valid) )
                    # 用有效时间及回踩买点提交买入订单
                    self.order = self.buy(exectype = bt.Order.Limit, price = price, valid = valid)
                    #o = self.buy()
                    print('*' * 50)

        elif self.order is None:
            # 提交stoptrail订单
            self.order = self.sell(exectype=self.p.stoptype,
                                   trailamount=self.p.trailamount,
                                   trailpercent=self.p.trailpercent)
            if self.p.trailamount:
                tcheck = self.data.close - self.p.trailamount
            else:
                tcheck = self.data.close * (1.0 - self.p.trailpercent)
            print('Sell stoptrail order created: {}: \
                close： {} /  \
                Limit price: {} / check price {}'.format(
                self.datetime.date(), self.data.close[0],
                self.order.created.price, tcheck
            ))
            print('-' * 10)
        else:
            if self.p.trailamount:
                tcheck = self.data.close - self.p.trailamount
            else:
                tcheck = self.data.close * (1.0 - self.p.trailpercent)
            print('update limit price: {}: \
                close： {} /  \
                Limit price: {} / check price {}'.format(
                self.datetime.date(), self.data.close[0],
                self.order.created.price, tcheck
            ))




if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("需要stockid，如：600031.sh或者300348.sz")
        sys.exit()

    stockid_input = sys.argv[1]
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
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    
    # Add the Data Feed to Cerebro
    # 在Cerebro中添加价格数据
    cerebro.adddata(data)
    # 设置启动资金
    cerebro.broker.setcash(100000.0)
    # 设置交易单位大小
    cerebro.addsizer(bt.sizers.FixedSize, stake = 1000)
    # 设置佣金为千分之一
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addstrategy(St)  # 添加策略
    cerebro.run()  # 遍历所有数据
    # 打印最后结果
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot(style = 'candlestick')  # 绘图
    # cerebro.plot()  # 绘图

