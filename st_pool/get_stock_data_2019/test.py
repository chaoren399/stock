#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf.urls import include, url
import os
import pandas as pd

from st_pool.get_stock_data_2019.getstockdata import getdatafrom_ts_5years
from stock.settings import BASE_DIR

num_progress = 0 # 当前的后台进度值（不喜欢全局变量也可以很轻易地换成别的方法代替）
allcodenum =''

'''
3下载股票的历史数据 
'''
def down_stock_data_from_tushare():
    global num_progress
    global  allcodenum

    stock_pool_path = BASE_DIR + '/st_pool/get_stock_data_2019/股票池.csv'
    df_1 = pd.read_csv(stock_pool_path, dtype=object)
    i=0;
    codes= df_1.shape[0] # 行数
    print 'codes='+ str(codes)
    str1=''
    for index, row in df_1.iterrows():
        code = row[0].zfill(6)
        # getdatafrom_ts(code) #600887
        getdatafrom_ts_5years(code)  # 下载 5 年的历史股票数据
        str1 = str1 + '(' + str(i + 1) + '-' + code + ')'
        # print code
        i=i+1
        info = '完成  ' + str(i) + '只基金下载'

    allcodenum = str1
    num_progress = i * 100 / codes;  # 更新后台进度值，因为想返回百分数所以乘100
    print  'num_progress=' + str(num_progress)

if __name__ == '__main__':
    down_stock_data_from_tushare()