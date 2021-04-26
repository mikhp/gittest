import pandas as pd
import mplfinance as mpf
import tushare as ts
import backtrader as bt
import os
import configparser


# 从配置文件中读取token等参数
realdir = os.path.realpath(__file__)
realdir = os.path.dirname(realdir)
realfile = os.path.join(realdir, "test.ini")

cf = configparser.ConfigParser()
cf.read(realfile)
token = cf.get("tushare", "token")
pro = ts.pro_api(token)
# 1.数据准备
df = pro.daily(ts_code='600031.SH', start_date='20210101', end_date='20210311')

# 删除 tushare 提供的不需要的数据，保留 Date, Open, High, Low, Close, Volume
df = df.drop(labels=["ts_code", "pct_chg",
             "pre_close", "amount", "change"], axis=1)

# 对数据进行改名，mplfinance有要求
df.rename(
    columns={'trade_date': 'Date', 'open': 'Open', 'high': 'High',
             'low': 'Low', 'close': 'Close', 'vol': 'Volume'},
    inplace=True)

# 转换时间序列
df = df[::-1]

# 将Date设置为索引，并转换为 datetime 格式
df.set_index(["Date"], inplace=True)
df.index = pd.to_datetime(df.index)
mpf.plot(df, type='candle', mav=(5, 10, 15,30), volume=True)
