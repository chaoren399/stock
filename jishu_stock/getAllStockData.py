#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts
import sys
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR

import time
reload(sys)

sys.setdefaultencoding('utf8')

'''
日线行情
https://tushare.pro/document/2?doc_id=27
'''

def getAllStockData(start_date , end_date, localpath):
    info = " 下载数据开始运行 ----------start_date="+str(start_date)+'--end_date='+str(end_date)

    writeLog_to_txt_nocode(info)

    print "下载 更新数据  start 每天 4:10 分更新了"
    # ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    mytoken='731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be'
    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api(mytoken,timeout=60)

# 打印最新的数据
    if(end_date >='20210101'):
        df1 = ts.pro_bar(ts_code='000001.SZ',adj='qfq', start_date='20210801', end_date=end_date)
        if (df1.empty):
            print '--df1.empty--' + str('000001.SZ')
            return 0
        if(len(df1)>0):
            print df1[0:2]
            writeLog_to_txt_nocode(df1.ix[0]['trade_date'])
            path = '00_测试定时任务.txt'
            stockcode = '000001.SZ'
            info='下载数据开始='+str(df1.ix[0]['trade_date'])
            writeLog_to_txt_path_getcodename(info, path, stockcode)
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # print "ssss"
    print path
    data = pd.read_csv(path, dtype={'code': str})
    start_date = start_date
    end_date = end_date
    count = 0
    df = pd.DataFrame()
    if(len(data.columns)==1): # 只有一列股票代码,没有股票名称
        for index, row in data.iterrows():
            count = count + 1
            stock_code = row['ts_code']
            if (1):
                # 下载股票信息 近一个月的
                time.sleep(0.05)  # //睡觉
                df = ts.pro_bar(ts_code=stock_code,adj='qfq', start_date=start_date, end_date=end_date, ma=[5, 13, 34])
                stockdata_path = BASE_DIR + localpath
                df.to_csv(stockdata_path + stock_code + ".csv")
                print count
                # print df
    else:

        for index, row in data.iterrows():
            count = count + 1
            # print row['ts_code']
            name = row['name']
            stock_code = row['ts_code']
            if ('ST' not in name):
                # 下载股票信息 近一个月的
                # time.sleep(0.005)  # //睡觉
                # time.sleep(0.03)  # //睡觉2021
                sleep(0.03)  # //睡觉2021

                # time.sleep(0.01)  # //睡觉 2015
                #  2021年08月16日 增加 ma5 ma13 ma 34
                df = ts.pro_bar(ts_code=stock_code,adj='qfq', start_date=start_date, end_date=end_date, ma=[5, 13, 34,144,169,75])
                stockdata_path = BASE_DIR + localpath
                print str(count) + '--' + stock_code
                if (df is None or df.empty):

                    print '--df.empty--' + str(stock_code)
                    return 0
                else:
                    df.to_csv(stockdata_path + stock_code + ".csv")


'''
测试 得到一直股票的 数据
'''
def testGet_one_stockData():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')


    # 打印最新的数据
    df = ts.pro_bar(ts_code='000001.SZ', adj='qfq',start_date='20180801', end_date='20210904',ma=[5, 13, 34])
    print df[0:2]
    localpath2 = '/jishu_stock/stockdata/data1/'
    stockdata_path = BASE_DIR + localpath2
    df.to_csv(stockdata_path + '000001.SZ' + ".csv")
    print df

'''
2020 年到 2018 年的 所有 K 线数据
'''
def get_all_2020_data():
    print '2020 年到 2018 年的 所有 K 线数据'
    localpath = '/jishu_stock/stockdata/data2020/'
    getAllStockData(start_date='20180101', end_date='20201231', localpath=localpath)


'''
2015 年到 2018 年的 所有 K 线数据  为月线做准备的, 结果 tushare 官方提供月线
'''
def get_all_2015_2018_data():
    print '得到 2015 年到 2018 年的 所有 K 线数据  为月线做准备的, 结果 tushare 官方提供月线'
    localpath = '/jishu_stock/stockdata/data2015_2017/'
    getAllStockData(start_date='20150101', end_date='20171231', localpath=localpath)

'''
得到 从 20210101 开始到现在的日线数据
'''
def get_all_2021_to_now_data(localpath):
    print '得到 从 20210101 开始到现在的日线数据'
    # today = starttime.strftime('%Y%m%d')
    starttime = datetime.datetime.now()
    today = starttime.strftime('%Y%m%d')
    getAllStockData(start_date = '20210101',end_date = today,localpath=localpath)


def test_get_all_2015_2018_data():
    localpath = '/jishu_stock/stockdata/data2015_2017/'
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # df = ts.pro_bar(ts_code='000001.SZ', start_date='20171231', end_date='20171231')
    df = ts.pro_bar(ts_code='000002.SZ', start_date='20171201', end_date='20171231')
    print df[0:2]
    stockdata_path = BASE_DIR + localpath
    print df
    print '-----222-----'
    # df.to_csv(stockdata_path + '201701201' + ".csv")
    df = ts.pro_bar(ts_code='000002.SZ', start_date='20181201', end_date='20181231')
    print df

    df = ts.pro_bar(ts_code='000002.SZ', start_date='20210901', end_date='20210912')
    print df


def test_002923():
    stock_code='002923.SZ'


    start_date='20150101'
    end_date='20171231'
    # df = pd.DataFrame()

    df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=end_date, ma=[5, 13, 34])
    stockdata_path = BASE_DIR + localpath
    print  '--' + stock_code
    # print df.empt

    if (df is None or df.empty):
        print '--df.empty--' + str(stock_code)
        return 0
    df.to_csv(stockdata_path + stock_code + ".csv")

if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath= '/jishu_stock/stockdata/data1/'


    get_all_2021_to_now_data(localpath)
    # testGet_one_stockData()
    # get_all_2020_data()
    # get_all_2015_2018_data()
    # test_002923()
    # test_get_all_2015_2018_data()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"