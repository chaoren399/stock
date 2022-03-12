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
def get_index_data_from_ts(index_code):

    enddate = str(datetime.date.today()) #获取股票池的最近 1 年的 数据
    # df =  ts.get_hist_data(index_code,start='2019-01-01',end=enddate)
    # df =  ts.get_hist_data('600848', ktype='W') #获取周k线数据
    df =  ts.get_hist_data(index_code, start='2001-01-01', end=enddate, ktype='W') #获取周k线数据
    # df =  ts.get_hist_data('sz50', start='2014-01-01', end='2020-01-26', ktype='W') #获取周k线数据

    f = open(BASE_DIR + '/st_pool/get_index_data/index_old_data/data/' + index_code + '.csv', 'w')
    # 开盘(open)，收盘(close)，最低(lowest)，最高(highest)
    for index, row in df.iterrows():
        f.write(index + ',' + str(row['open']) +','+str(row['close']) +','+str(row['low'])+','+str(row['high'])+ '\n')
    f.close()
    logging.info('--'+str(index_code) + '--done')


def get_zhishuchi_alldata():
    fundpool_path = BASE_DIR + '/st_pool/get_index_data/指数池.csv'
    df_1 = pd.read_csv(fundpool_path, dtype=object)
    codes = df_1.iloc[:, 0].values
    print codes
    i = 0;
    str1 = ''
    for code in codes:
        time.sleep(2)  # //睡觉
        print code
        x = get_index_data_from_ts(code)


if __name__ == '__main__':


    # getdatafrom_ts ('cyb')
    # get_zhishuchi_alldata()
    # getdatafrom_ts ('sz50')

    get_zhishuchi_alldata()

    # fundpool_path = BASE_DIR + '/st_pool/get_index_data/指数池.csv'
    # df_1 = pd.read_csv(fundpool_path, dtype=object)
    # codes = df_1.iloc[:, 0].values
    # print len(codes)








