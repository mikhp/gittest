import numpy as np
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from pylab import mpl
from datetime import datetime
import talib
from sklearn.ensemble import RandomForestClassifier  #分类决策树模型
from sklearn.metrics import accuracy_score  #预测准确度评分函数
import warnings
warnings.filterwarnings("ignore")

#pd.set_option()就是pycharm输出控制显示的设置
pd.set_option('expand_frame_repr', False)#True就是可以换行显示。设置成False的时候不允许换行
pd.set_option('display.max_columns', None)# 显示所有列
#pd.set_option('display.max_rows', None)# 显示所有行
pd.set_option('colheader_justify', 'centre')# 显示居中

pro = ts.pro_api('要到tushare官网注册个账户然后将token复制到这里,可以的话请帮个忙用文章末我分享的链接注册，谢谢')
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

#1.数据准备
df = pro.daily(ts_code='002505.SZ', start_date='20200101', end_date='20200818')
df.set_index('trade_date', inplace=True)  #设置date列为索引，覆盖原来索引,这个时候索引还是 object 类型，就是字符串类型。
df.index = pd.DatetimeIndex(df.index)  #将object类型转化成 DateIndex 类型，pd.DatetimeIndex 是把某一列进行转换，同时把该列的数据设置为索引 index。
df = df.sort_index(ascending=True)  #将时间顺序升序，符合时间序列
print(df)
df['close-open'] = (df['close']-df['open'])/df['open']
df['high-low'] = (df['high']-df['low'])/df['low']
df['pre_close'] = df['close'].shift(1)  #昨日收盘价
df['price_change'] = df['close']-df['pre_close']
df['p_change'] = (df['close']-df['pre_close'])/df['pre_close']*100
df['MA5'] = df['close'].rolling(5).mean()
df['MA10'] = df['close'].rolling(10).mean()
df.dropna(inplace=True)

# df['RSI'] = talib.RSI(df['close'], timeperiod=12)
# df['MOM'] = talib.MOM(df['close'], timeperiod=5)
# df['EMA12'] = talib.EMA(df['close'], timeperiod=12)
# df['EMA26'] = talib.EMA(df['close'], timeperiod=26)
# df['MACD'], df['MACDsignal'], df['MACDhist'] = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
df.dropna(inplace=True)

#2.提取特征变量和目标变量，用当天收盘后获取完整的数据为特征变量，下一天的涨跌情况为目标变量这样来训练分类决策树模型
X = df[['close', 'vol', 'close-open', 'MA5', 'MA10', 'high-low', 'RSI', 'MOM', 'EMA12', 'EMA26', 'MACD', 'MACDsignal', 'MACDhist']]
y = np.where(df['price_change'].shift(-1)>0, 1, -1)  #下一天股价涨，赋值1，下跌或平，赋值-1
#3设置训练集跟测试集
X_length = X.shape[0]  #获取X的行数和列数，shape[0]为行数
split = int(X_length * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

#4设置模型
model = RandomForestClassifier(max_depth=4, n_estimators=10, min_samples_leaf=5, random_state=1)
model.fit(X_train, y_train)

#5预测股价涨跌，根据X_test给出的'close', 'vol', 'close-open', 'MA5'等数据进行预测第二天股价的涨跌情况
y_pred = model.predict(X_test)
#print(y_pred)
a = pd.DataFrame()
a['预测值'] = list(y_pred)
a['实际值'] = list(y_test)
print(a)

#6预测属于各个分类的概率
y_pred_proba = model.predict_proba(X_test)
b = pd.DataFrame(y_pred_proba, columns=['分类为-1的概率', '分类为1的概率'])
print(b)

#7整体模型的预测准确度
from sklearn.metrics import accuracy_score
score = accuracy_score(y_pred, y_test)
print('准确率： ' + str(round(score*100, 2)) + '%')

#8分析特征变量的特征重要性
features = X.columns
importances = model.feature_importances_
b = pd.DataFrame()
b['特征'] = features
b['特征重要性'] = importances
b = b.sort_values('特征重要性', ascending=False)
print(b)

#参数调优
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':[5, 10, 20], 'max_depth':[2, 3, 4, 5], 'min_samples_leaf':[5, 10, 20, 30]}
new_model = RandomForestClassifier(random_state=1)
grid_search = GridSearchCV(new_model, parameters, cv=6, scoring='accuracy')
grid_search.fit(X_train, y_train)
grid_search.best_params_
print('最优模型参数： ' + str(grid_search.best_params_))
#————————————————
#版权声明：本文为CSDN博主「Wilburzzz」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
#原文链接：https://blog.csdn.net/Wilburzzz/article/details/108105709