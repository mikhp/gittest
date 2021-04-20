from datetime import datetime
import backtrader as bt
from backtrader import cerebro

class SmaCross(bt.Strategy):
    params=dict(
        pfast=10,
        pslow=30
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        # self.crossover= bt.ind.CrossOver(sma1,sma2)
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
    
    def next(self):
        if not self.position:
            if self.crossover>0:
                self.buy()               
        elif self.crossover<0:            
            self.close()

cerebro= bt.Cerebro()
cerebro.broker.setcash(100000)
cerebro.broker.setcommission(commission=0.003)
# 通过getdata.py获取股票数据文件cvs
data = bt.feeds.YahooFinanceCSVData(dataname="./600999.sh.csv")
cerebro.adddata(data)
cerebro.addstrategy(SmaCross)
cerebro.run()
cerebro.plot()