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
获取指数池的最近 1 年的 数据 tushare  ts.get_hist_data('600848', ktype='W') #获取周k线数据

'''
def getdatafrom_ts(index_code):

    enddate = str(datetime.date.today()) #获取股票池的最近 1 年的 数据
    # df =  ts.get_hist_data(index_code,start='2019-01-01',end=enddate)
    # df =  ts.get_hist_data('600848', ktype='W') #获取周k线数据
    df =  ts.get_hist_data(index_code, start='2014-01-01', end='2020-01-26', ktype='W') #获取周k线数据
    # df =  ts.get_hist_data('sz50', start='2014-01-01', end='2020-01-26', ktype='W') #获取周k线数据

    f = open(BASE_DIR + '/st_pool/get_index_data/index_old_data/data/' + index_code + '.csv', 'w')
    # 开盘(open)，收盘(close)，最低(lowest)，最高(highest)
    for index, row in df.iterrows():
        f.write(index + ',' + str(row['open']) +','+str(row['close']) +','+str(row['low'])+','+str(row['high'])+ '\n')
    f.close()
    logging.info('--'+str(index_code) + '--done')

'''
获取股票池的5年历史数据  (一般情况不会用到.)

'''


def getdatafrom_ts_5years(stock_code):
    # df =  ts.get_hist_data('600887',start='2014-01-01',end='2019-01-01') #获取 5 年的历史数据
    df = ts.get_hist_data(stock_code, start='2014-01-01', end='2019-01-01')
    f = open(BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data_2014_2019/' + stock_code + '.csv', 'w')
    for index, row in df.iterrows():
        f.write(index + ',' + str(row['open']) + '\n')
    f.close()
    logging.info('--' + str(stock_code) + '--done')



if __name__ == '__main__':

    getdatafrom_ts ('hs300')







