#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt
from stock.settings import BASE_DIR
import numpy as np
from dateutil.parser import parse
''''

10周均线 和 60 周均线,就是  MA50, MA  300 ,对不对呢?


60周均线的意思是60个星期的每周最后一天的收盘价（指股价）相加后除于60，即60周均线。

https://blog.csdn.net/qq_45103998/article/details/102521676

'''

def get10_60_WEEK_data():
    df = ts.pro_bar(ts_code='300068.SZ', start_date='20190628', end_date='20210823', ma=[50, 300])
    df.to_csv("10_60.csv")
    data7_1 = df.iloc[0:10]  # 前7行
    data7_1
    a1=data7_1.ix[0]['ma50']
    a2=data7_1.ix[0]['ma300']
    riqi=data7_1.ix[0]['trade_date']

    print str(a1)+"---" +str(a2)
    print riqi

def test1():
    # 加载数据前定义一个转换函数，将日均线转周线

    def convert_date(d):
        # print d
        # day = d
        # '20210820'
        # d1 = day[0:4]
        # d2 =day[4:6]
        # d3 = day[6:8]
        # d = d3+'/'+d2+'/'+d1
        return parse(d).weekday()
    # print convert_date('20210820')

    path1 = BASE_DIR+'/jishu_stock/stockdata/AMZN.csv'
    stock_info = np.loadtxt(path1, delimiter=',', skiprows=1, usecols=[0, 1, 2, 3, 4], dtype='S',
                            converters={0: convert_date})
    # 同样的颠倒日期顺序，并将数字转为浮点格式
    stock_info = stock_info[::-1, :].astype('f8')
    print stock_info

    # 找到星期一的索引
    week_split = np.where(stock_info[:, 1] == 0)[0]
    week_infos = np.split(stock_info, week_split)
    # 去掉一周非五天的数组
    week_info = [x for x in week_infos if len(x) == 5]
    # 将得到的列表转为array数组
    w = np.array(week_info)
    print week_info



if __name__ == '__main__':

    # get10_60_WEEK_data()
    test1()
