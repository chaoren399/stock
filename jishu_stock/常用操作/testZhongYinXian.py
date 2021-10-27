#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR


''''
一般可这样区分：
 小阴线和小阳线的波动范围一般在0.6--1.5%；
 中阴线和中阳线的波动范围一般在1.6-3.5%；
 大阴线和大阳线的波动范围在3.6%以上。

'''
def testZhangtingban():
    # 案例 2南玻A 000012，
    df1 = ts.pro_bar(ts_code='000012.SZ', adj='qfq', start_date='20170206', end_date='20210208')
    data7_1 = df1.iloc[0:660]  # 前7行


    for index,row in data7_1.iterrows():
        if(isZhangTingBan(row)==1):
            chazhi1 = ((row['close'] - row['open']) / row['open']) * 100  # (开盘价-收盘价)÷开盘价＜0.5%
            print1(chazhi1)

if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    testZhangtingban()