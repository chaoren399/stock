#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR

'''
单独 拿到月线数据的换手率,

https://tushare.pro/document/2?doc_id=145

从 tushare 下载 月线数据, 包含
'''

def getMonth_K_Data(start_date , end_date, localpath):
    print  str(end_date)+ "getMonth_K_Data 开始运行 --------------"
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    print path
    data = pd.read_csv(path, dtype={'code': str})
    start_date = start_date
    end_date = end_date
    count = 0
    if(len(data) > 0):
        for index, row in data.iterrows():
            count = count + 1
            name = row['name']
            stock_code = row['ts_code']
            if ('ST' not in name):
                # 下载股票信息 近一个月的
                # time.sleep(0.005)  # //睡觉
                time.sleep(0.5)  # //睡觉 运行很慢, 用移动网络 0.3 就会发生频发, 还是 0.5 好用

                # df = pro.monthly(ts_code='000001.SZ', start_date='20180101', end_date='20181101',
                #                  fields='ts_code,trade_date,open,high,low,close,vol,amount')

                df = pro.monthly(ts_code=stock_code, start_date=start_date, end_date=end_date,
                                 fields='ts_code,trade_date,open,high,low,close,vol,amount')

                stockdata_path = BASE_DIR + '/jishu_stock/stockdata/MONTH_DATA_K/' + stock_code + '_Month' + ".csv"
                df.to_csv(stockdata_path )
                print str(count) +'----'+ str(stock_code)

'''
https://waditu.com/document/2?doc_id=145

'''
def test_getTushare_Month_k():
    pro = ts.pro_api()
    today = starttime.strftime('%Y%m%d')
    df = pro.monthly(ts_code='000001.SZ', start_date='20150101', end_date=today,
                     fields='ts_code,trade_date,open,high,low,close,vol,amount')

    print df



    print df


def get_one_stock_monthdata():
    stock_code='000663.SZ'
    pro = ts.pro_api()
    df = pro.monthly(ts_code=stock_code, start_date='20150101', end_date=today,
                     fields='ts_code,trade_date,open,high,low,close,vol,amount')
    stockdata_path = BASE_DIR + '/jishu_stock/stockdata/MONTH_DATA_K/' + stock_code + '_Month' + ".csv"
    df.to_csv(stockdata_path)

def test():
    pro = ts.pro_api()

    df = pro.monthly(ts_code='000001.SZ', start_date='20180101', end_date='20181101',
                     fields='ts_code,trade_date,open,high,low,close,vol,amount,turnover_rate')
    print df

if __name__ == '__main__':
    import datetime
    starttime = datetime.datetime.now()


    # test1()
    localpath1 = '/jishu_stock/stockdata/data1/'

    today = starttime.strftime('%Y%m%d')
    # getMonth_K_Data(start_date = '20150101',end_date = today,localpath=localpath1)
    # get_one_stock_monthdata()

    # test_getTushare_Month_k()
    test()

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds