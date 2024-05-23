#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from pandas.errors import EmptyDataError

from jishu_stock.Tool_jishu_stock import dingshi_ceshi, print1, writeLog_to_txt_path_getcodename, writeLog_to_txt_nocode
from jishu_stock.z_tool.email import webhook
from stock.settings import BASE_DIR
import tushare as ts
import sys
import pandas as pd
import time

import sys
reload(sys)
sys.setdefaultencoding( 'utf-8' )

from threading import Thread
from time import sleep
from time import *
starttime = datetime.datetime.now()
today = starttime.strftime('%Y%m%d')

start_date = '20180101'
end_date = '20221231'
localpath = '/jishu_stock/stockdata/data2020/' #数据存放路径



def get_all_codes():
    # webhook.sendData("开始下载数据")

    starttime = time()

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

        print  info
        # writeLog_to_txt_path_getcodename(info, path, stockcode)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'


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

    t1 = Thread(target=getdata_task1, args=(a,))  # 定义线程t1，线程任务为调用task1函数，task1函数的参数是6
    t2 = Thread(target=getdata_task2,args=(b,))  # 定义线程t2，线程任务为调用task2函数，task2函数无参数
    t1.start()  # 开始运行t1线程
    t2.start()  # 开始运行t2线程
    #join()只有在你需要等待线程完成时候才是有用的。
    t1.join()
    t2.join()
    print 't2.join() 我来了'

    endtime = time()

    info=''
    info = info+'-------------------------------------------'

    print info+ "get_all_codes 下载数据总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟" +info
    webhook.sendData("数据下载完成")

def download_onestock_token1(stock_code):
    # ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    import time
    time.sleep(0.15)

    df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=end_date,
                    ma=[5, 13, 34, 144, 169, 75,10,20,30,60,120])
    stockdata_path = BASE_DIR + localpath
    print stock_code

    if (df is None or df.empty):

        print '--df.empty--' + str(stock_code)
        return 0
    else:
        df.to_csv(stockdata_path + stock_code + ".csv")




def getdata_task1( a):
    print 1
    for index, item in enumerate(a):
      # print index, item
      download_onestock_token1(item)



def getdata_task2(b):
    print 2
    for index, item in enumerate(b):
      # print index, item
      download_onestock_token1(item)



if __name__ == '__main__':
    starttime = datetime.datetime.now()

    get_all_codes()

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds / 60