#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

from jishu_stock.Tool_jishu_stock import print1
from stock.settings import BASE_DIR
import pandas as pd
import tushare as ts


'''
从 dataframe 中 找到 每日K 线中最低值 中最小的 那个数值
返回 row
'''
def  getMin_fromDataFrame(data):
    len_data=len(data)
    # print1(len_data)
    if(len_data >0):
        Mindata= data.ix[0]['low']
        min_row=''
        for index ,row in data.iterrows():
            if(index==0):
                min_row=row
            if( Mindata > row['low']):  # 近 10 天的最小值
                Mindata = row['low']
                min_row=row
        # print min_row
        return min_row
    else:
        return None