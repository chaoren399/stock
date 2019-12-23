#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf.urls import include, url
import os
import pandas as pd
import tushare as ts
from st_pool.get_stock_data_2019.getstockdata import getdatafrom_ts_5years
from stock.settings import BASE_DIR

num_progress = 0 # 当前的后台进度值（不喜欢全局变量也可以很轻易地换成别的方法代替）
allcodenum =''

'''
3下载股票的历史数据 
'''
def down_stock_data_from_tushare():
    stock_pool_path = BASE_DIR + '/st_pool/get_stock_data_2019/股票池.csv'

    oldstockdatapath_5year = BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data_2014_2019/'
    oldstockdatapath_1year = BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data/'
    df_1 = pd.read_csv(stock_pool_path, dtype=object)
    code = '000001'
    df = pd.read_csv(oldstockdatapath_5year + code + '.csv', dtype=object, header=None)
    df.columns = ['date', 'value']
    df1 = pd.read_csv(oldstockdatapath_1year + code + '.csv', dtype=object, header=None)
    df1.columns = ['date', 'value']
    # print df
    res = df.append(df1)
    res = res.sort_values(by='date', axis=0, ascending=True)  # 按照日期排序
    print res









if __name__ == '__main__':
    # down_stock_data_from_tushare()

    print ts.get_hist_data('600887', start='2014-01-01', end='2019-01-01')