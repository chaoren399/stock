#!/usr/bin/python
# -*- coding: utf8 -*-
# from django.conf.urls import include, url
import os
import pandas as pd
import tushare as ts

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
    code = '300999'
    df = pd.read_csv(oldstockdatapath_5year + code + '.csv', dtype=object, header=None)
    df.columns = ['date', 'value']
    df1 = pd.read_csv(oldstockdatapath_1year + code + '.csv', dtype=object, header=None)
    df1.columns = ['date', 'value']
    # print df
    res = df.append(df1)
    res = res.sort_values(by='date', axis=0, ascending=True)  # 按照日期排序
    print res

if __name__ == '__main__':
    # print   ts.get_hist_data("sh000300", start='2014-01-01', end='2019-01-01',ktype='W')

    # ts.get_hist_data('600848', ktype='W')  # 获取周k线数据

    # print ts.get_hist_data('600848', ktype='W') #获取周k线数据
    # print ts.get_hist_data('512010', ktype='W') #获取周k线数据
    # print ts.get_hist_data('hs300',start='2014-01-01', end='2019-01-01',ktype='W')
    # print ts.get_hist_data('300999',start='2019-01-01', end='2021-01-01',ktype='W')
    # print ts.get_hist_data('300999', ktype='W') #获取周k线数据

    # print ts.get_hist_data('600848', start='2015-01-05', end='2015-01-09')
    # print ts.get_hist_data('600848', ktype='W')  # 获取周k线数据
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    pro = ts.pro_api()


    df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')

    df = pro.daily(ts_code='300750.SZ', start_date='20210101', end_date='20210718')

    print df
    # print ts.get_hist_data('300750.SZ', ktype='W') #获取周k线数据