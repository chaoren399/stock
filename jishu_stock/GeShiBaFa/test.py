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

def test_get_WeekMa10_Ma60():
    stock_code='000001.SZ'
    path1= BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"

    data = pd.read_csv(path1, dtype={'code': str})
    data['WeekMa10'] =  data['close'].rolling(10).mean()
    data['WeekMa60'] =  data['close'].rolling(60).mean()
    data['Week60-10'] = data['WeekMa60']- data['WeekMa10']
    # data=data.dropna(axis=0, how='all', inplace=True)
    data = data.dropna(how='any', axis=0)
    # print data

    print  data[1]['trade_date']



if __name__ == '__main__':

    # get10_60_WEEK_data()
    test_get_WeekMa10_Ma60()
    # print abs(-44)