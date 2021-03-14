# 通过tushare，获取数据，展示股票图形
import os
import pandas as pd
import tushare as ts
import tkinter as tk
import mplfinance as mpf
import tkinter.tix as tix
from tkinter import *
import configparser
# from tkinter.constants import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


# 从配置文件中读取token等参数
cf = configparser.ConfigParser()
inifile = os.path.realpath("test.ini")
print(inifile)
cf.read(inifile)  # 读取配置文件，如果写文件的绝对路径，就可以不用os模块

token = cf.get("tushare", "token")  # 获取[tushare]中token对应的值
print("token:" , token)

pro = ts.pro_api(token)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
 
root = Tk()  # 创建主窗口
screenWidth = root.winfo_screenwidth()  # 获取屏幕宽的分辨率
screenHeight = root.winfo_screenheight()
x, y = int(screenWidth / 4), int(screenHeight / 4)  # 初始运行窗口屏幕坐标(x, y),设置成在左上角显示
width = int(screenWidth / 2)  # 初始化窗口是显示器分辨率的二分之一
height = int(screenHeight / 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 窗口的大小跟初始运行位置
root.title('Wilbur量化分析软件')
# root.resizable(0, 0)  # 固定窗口宽跟高，不能调整大小,无法最大窗口化
# root.iconbitmap('ZHY.ico')  # 窗口左上角图标设置,需要自己放张图标为icon格式的图片文件在项目文件目录下
 
# 首先创建主框架
main_frame = tix.Frame(root, width=screenWidth, height=screenHeight,relief=tix.SUNKEN, bg='#353535', bd=5, borderwidth=4)
main_frame.pack(fill=BOTH, expand=0)
 
# 在主框架下创建股票代码输入子框架
code_frame = tix.Frame(main_frame, borderwidth=1, bg='#353535')
code_frame.pack()
# 创建标签‘股票代码’
stock_label = tix.Label(code_frame, text='股票代码', bd=1)
stock_label.pack(side=LEFT)
# 创建股票代码输入框
input_code_var = tix.StringVar()
code_widget = tix.Entry(code_frame, textvariable=input_code_var, borderwidth=1, justify=CENTER)
input_code_get = input_code_var.set(input_code_var.get())  # 获取输入的新值
code_widget.pack(side=LEFT, padx=4)
 
# 在主框架下创建股票日期输入框子框架
input_date_frame = tix.Frame(main_frame, borderwidth=1, bg='#353535')
input_date_frame.pack()
# 创建标签‘开始日期’
date_start_label = tix.Label(input_date_frame, text='开始日期', bd=1)
date_start_label.pack(side=LEFT)
# 创建开始日期代码输入框
input_startdate_var = tix.StringVar()
startdate_widget = tix.Entry(input_date_frame, textvariable=input_startdate_var, borderwidth=1, justify=CENTER)
input_startdate_get = input_startdate_var.set(input_startdate_var.get())  # 获取输入的新值
startdate_widget.pack(side=LEFT, padx=4)
# 创建标签‘结束日期’
date_end_label = tix.Label(input_date_frame, text='结束日期', bd=1)
date_end_label.pack(side=LEFT)
# 创建结束日期代码输入框
input_enddate_var = tix.StringVar()
enddate_widget = tix.Entry(input_date_frame, textvariable=input_enddate_var, borderwidth=1, justify=CENTER)
input_enddate_get = input_enddate_var.set(input_enddate_var.get())  # 获取输入的新值
enddate_widget.pack(side=LEFT, padx=4)
 
# 创建股票图形输出框架
stock_graphics = tix.Frame(root, borderwidth=1, bg='#353535', relief=tix.RAISED)
stock_graphics.pack(expand=1, fill=tk.BOTH, anchor=tk.CENTER)
 
 
def go():
    code_name = input_code_var.get()
    start_date = input_startdate_var.get()
    end_date = input_enddate_var.get()
    stock_data = pro.daily(ts_code=code_name, start_date=start_date, end_date=end_date)
    print(stock_data)
    data = stock_data.loc[:, ['trade_date', 'open', 'close', 'high', 'low', 'vol']]  # ：取所有行数据，后面取date列，open列等数据
    data = data.rename(columns={'trade_date': 'Date', 'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low',
                                'vol': 'Volume'})  # 更换列名，为后面函数变量做准备
    data.set_index('Date', inplace=True)  # 设置date列为索引，覆盖原来索引,这个时候索引还是 object 类型，就是字符串类型。
    # 将object类型转化成 DateIndex 类型，pd.DatetimeIndex 是把某一列进行转换，同时把该列的数据设置为索引 index。
    data.index = pd.DatetimeIndex(data.index)
    data = data.sort_index(ascending=True)  # 将时间顺序升序，符合时间序列
 
    fig, axlist = mpf.plot(data, type='candle', mav=(5, 10, 20), volume=True, show_nontrading=False, returnfig=True)
 
    canvas = FigureCanvasTkAgg(fig, master=stock_graphics)  # 设置tkinter绘制区
    canvas.draw()
    toolbar = NavigationToolbar2Tk(canvas, stock_graphics)
    toolbar.update()  # 显示图形导航工具条
    canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=1)
 
 
# 在主框架下创建查询按钮子框架
search_frame = tix.Frame(main_frame, borderwidth=1, bg='#353535', relief=tix.SUNKEN)
search_frame.pack()
# 创建查询按钮并设置功能
stock_find = tix.Button(search_frame, text='查询', width=5, height=1, command=go)
stock_find.pack()
 
root.mainloop()
