#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

import tushare as ts
import pandas as pd
import os
import logging

from stock.settings import BASE_DIR

'''
获取股票池的最近 1 年的 数据 tushare get_hist_data

'''
def getdatafrom_ts(stock_code):

    enddate = str(datetime.date.today()) #获取股票池的最近 1 年的 数据
    df =  ts.get_hist_data(stock_code,start='2019-01-01',end=enddate)
    f = open(BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data/' + stock_code + '.csv', 'w')
    for index, row in df.iterrows():
        f.write(index + ',' + str(row['close']) + '\n')
    f.close()
    logging.info('--'+str(stock_code) + '--done')

'''
获取股票池的5年历史数据  (一般情况不会用到.)

'''


def getdatafrom_ts_5years(stock_code):
    # df =  ts.get_hist_data('600887',start='2014-01-01',end='2019-01-01') #获取 5 年的历史数据
    df = ts.get_hist_data(stock_code, start='2014-01-01', end='2019-01-01')
    f = open(BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data_2014_2019/' + stock_code + '.csv', 'w')
    for index, row in df.iterrows():
        f.write(index + ',' + str(row['close']) + '\n')
    f.close()
    logging.info('--' + str(stock_code) + '--done')

'''
获取当日 的 股票价格 

'''
def getdata(stock_pool_path):
#1. 处理 我的估值表格
    df_1 = pd.read_csv(stock_pool_path,dtype=object)
    df_1.columns = ['code', 'name','lowprice','upprice','order','tar_value','now_price','jiazhilv','date']
    for index ,row in df_1.iterrows():
        code = row['code'].zfill(6)
        df_1.iloc[index, 0] = code # 把 776转成 000776
        print code
        stockdata = ts.get_realtime_quotes(row['code']) #df[['code','name','price','bid','ask','volume','amount','time']]
        # data3.trade - data3.lowprice
        df_1.iloc[index, 7] = float(stockdata['price'][0])-  float(row['lowprice']) # 生成价值率 jiazhilv
        df_1.iloc[index, 6] = stockdata['price'][0]
        # df_1.iloc[index, 7] = df_1['']
        df_1.iloc[index, 8] = stockdata['date'][0]
    # print df_1
    return df_1

if __name__ == '__main__':
#1
    path1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path2 = path1 + '/get_stock_data/get_today_all.csv'
    # download_data(path2) #下载之后关闭

#2

    path3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stock_pool_path = path3 + '/get_stock_data/股票池.csv'
    # getdata(stock_pool_path)

    # getdatafrom_ts('600848')
    getdatafrom_ts_5years('512010')






