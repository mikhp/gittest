# -*- coding: utf-8 -*-
import tushare as ts
import pandas as pd
import os
import sys
import configparser
import datetime


# 获取前1天或N天的日期，beforeOfDay=1：前1天；beforeOfDay=N：前N天
def getdate(beforeOfDay):
    today = datetime.datetime.now()
    # 计算偏移量
    offset = datetime.timedelta(days=-beforeOfDay)
    # 获取想要的日期的时间
    re_date = (today + offset).strftime('%Y%m%d')
    return re_date


# 从配置文件中读取token等参数
realdir = os.path.realpath(__file__)
realdir = os.path.dirname(realdir)
realfile = os.path.join(realdir, "test.ini")
print("参数文件绝对路径：", realfile)
cf = configparser.ConfigParser()
cf.read(realfile)
token = cf.get("tushare", "token")
pro = ts.pro_api(token)

if len(sys.argv) < 2:
    print("参数：股票代码，开始时间、结束时间")
    sys.exit()
else:
    stockid_input = sys.argv[1]
    startT = getdate(int(sys.argv[2]))
    stopT = getdate(0)


# 缺省读取股票代码在ini文件中
# STOCKID = cf.get("stock", "stockid")
# print("stockid:{}".format(STOCKID))

print("stockid:{}, starttime:{},endtime:{}".format(stockid_input, startT, stopT))

STOCKID = stockid_input
# 1.数据准备
df = pro.daily(ts_code=STOCKID, start_date=startT, end_date=stopT)
# 设置date列为索引，覆盖原来索引,这个时候索引还是 object 类型，就是字符串类型。
# df.set_index('trade_date', inplace=True)
# 将object类型转化成 DateIndex 类型，pd.DatetimeIndex 是把某一列进行转换，同时把该列的数据设置为索引 index。
# df.index = pd.DatetimeIndex(df.index)
# df = df.sort_index(ascending=True)  # 将时间顺序升序，符合时间序列
# Date,Open,High,Low,Close,Adj Close,Volume

df1 = pd.DataFrame()
df1['Date'] = df['trade_date']
df1['Open'] = df['open']
df1['High'] = df['high']
df1['Low'] = df['low']
df1['Close'] = df['close']
df1['Adj Close'] = df['close']
df1['Volume'] = df['vol']
df1.set_index('Date', inplace=True)
df1.index = pd.DatetimeIndex(df1.index)  # 时间xxxx-xx-xx显示
df1 = df1.sort_index(ascending=True)  # 将时间顺序升序，符合时间序列
df1.dropna(inplace=True)
# df1.sort_index('date',ascending=false)
df1.to_csv('{}.csv'.format(STOCKID))

print(df1)

# df['high-low'] = (df['high']-df['low'])/df['low']
# df['pre_close'] = df['close'].shift(1)  # 昨日收盘价
# df['price_change'] = df['close']-df['pre_close']
# df['p_change'] = (df['close']-df['pre_close'])/df['pre_close']*100
# df['MA5'] = df['close'].rolling(5).mean()
# df['MA10'] = df['close'].rolling(10).mean()
# df.dropna(inplace=True)
