#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from pandas.errors import EmptyDataError

from jishu_stock.Tool_jishu_stock import dingshi_ceshi, print1, writeLog_to_txt_path_getcodename, writeLog_to_txt_nocode
from stock.settings import BASE_DIR
import tushare as ts
import sys
import pandas as pd
import time
reload(sys)
from threading import Thread
from time import sleep

starttime = datetime.datetime.now()
today = starttime.strftime('%Y%m%d')

start_date = '20200701'
end_date = today
localpath = '/jishu_stock/z_stockdata/data1/' #数据存放路径

# ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
ts.set_token('0c9acbe761612301ff2baaa9b3e8ec4053150ad1c1fb0e7b6d53bd5d')
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
def get_all_codes_k_data():
    df1 = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20210801', end_date=end_date)
    if (df1.empty):
        print '--df1.empty--' + str('000001.SZ')
        return 0
    if (len(df1) > 0):
        print df1[0:2]
        writeLog_to_txt_nocode(df1.ix[0]['trade_date'])
        path = '00_测试定时任务.txt'
        stockcode = '000001.SZ'
        info = '下载数据开始=' + str(df1.ix[0]['trade_date'])
        writeLog_to_txt_path_getcodename(info, path, stockcode)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST-1.csv'


    data = pd.read_csv(path, dtype={'code': str})

    count = 0
    stock_codes = []
    for index, row in data.iterrows():
        count = count + 1
        # print row['ts_code']
        name = row['name']
        stock_code = row['ts_code']
        # if ('ST' not in name):
        if (1):
            stock_codes.append(stock_code)

    len_codes = len(stock_codes)
    # print len_codes/2
    a = stock_codes[0:len_codes / 2]
    b = stock_codes[len_codes / 2:len_codes]
    # c = stock_codes[(len_codes/3)*2 :len_codes]
    # # print1( a)
    # print1(b)
    getdata_from_token1(a)
    getdata_from_token2(b)



def get_download_onestock_token1(stock_code):
    # ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=end_date,
                    ma=[5, 13, 34, 144, 169, 75,10,20,30,60])
    stockdata_path = BASE_DIR + localpath
    print stock_code

    if (df is None or df.empty):

        print '--df.empty--' + str(stock_code)
        return 0
    else:
        df.to_csv(stockdata_path + stock_code + ".csv")

'''
备用测试, 目前不用
'''
def get_download_onestock_token2(stock_code):
    # ts.set_token('fbc7fca7dc94fb233285e8c14ce8e964e5a1c65a602ba87e3b5bc331')

    df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=end_date,
                    ma=[5, 13, 34, 144, 169, 75])
    stockdata_path = BASE_DIR + localpath
    print stock_code

    if (df is None or df.empty):

        print '--df.empty--' + str(stock_code)
        return 0
    else:
        try:
            df.to_csv(stockdata_path + stock_code + ".csv")
        except EmptyDataError:
                print  stock_code +'errow'


@async
def getdata_from_token1( a):
    print 1
    for index, item in enumerate(a):
      # print index, item
      get_download_onestock_token1(item)



def getdata_from_token2(b):
    print 2
    for index, item in enumerate(b):
      # print index, item
      get_download_onestock_token1(item)



if __name__ == '__main__':
    starttime = datetime.datetime.now()

    get_all_codes_k_data()

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds / 60