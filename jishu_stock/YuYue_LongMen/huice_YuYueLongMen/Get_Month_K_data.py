#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR

'''
萧先生实战

https://www.jb51.net/article/213955.htm
日K 转换为 月K
每月 运行一次, 本次运行时间 2021年09月11日 2021年10月17日

https://tushare.pro/register?reg=456282 
'''

def cover_day_K_to_Month_K(df,outpath):
    if(len(df)==0):
        return 0

    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d', errors='coerce')

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    print df

    # 获取月k
    df_month = pd.DataFrame()
    df_month['open'] = df['open'].resample('M').first()
    df_month['close'] = df['close'].resample('M').last()
    df_month['high'] = df['high'].resample('M').max()
    df_month['low'] = df['low'].resample('M').min()
    # print(df_month)

    # data=data.dropna(axis=0, how='all', inplace=True)
    df_month = df_month.dropna(how='any', axis=0)
    df_month.sort_index(axis=1, ascending=True)
    df_month = df_month.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print  len(df_month)
    df_month.to_csv(outpath)

    return 1

def getAllMonth_Kdata(localpath1):
    print '日K 转换为 月K'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']


        stockdata_path1 = BASE_DIR + localpath1 + stock_code + ".csv"
        localpath2 = '/jishu_stock/stockdata/data2020/'   #
        stockdata_path2 = BASE_DIR + localpath2 + stock_code + ".csv"
        localpath3 = '/jishu_stock/stockdata/data2015_2017/'   #
        stockdata_path3 = BASE_DIR + localpath3 + stock_code + ".csv"

        df1 = pd.read_csv(stockdata_path1, index_col=0)
        df2 = pd.read_csv(stockdata_path2, index_col=0)
        df = pd.read_csv(stockdata_path3, index_col=0)
        df = df.append(df2)  # 合并 2020 年之前的数据
        df = df.append(df1)  # 合并 2020 年之前的数据


        # print df
        if (df.empty):
            return
        outpath= BASE_DIR + '/jishu_stock/stockdata/MONTH_DATA_K/' + stock_code +'_Month'+ ".csv"
        cover_day_K_to_Month_K(df,outpath)
        count = count+1
        print count

'''
测试一个股票转化为 月 K 

 2015 - 2020 年 有 72 个数据
 
 2021 年 9 月份 有 9 个
 
 总共有 81 条数据.
'''
def test_cover_day_K_to_Month_K():
    stock_code='000002.SZ'

    stockdata_path1 = BASE_DIR + localpath1 + stock_code + ".csv"
    localpath2 = '/jishu_stock/stockdata/data2020/'  #
    stockdata_path2 = BASE_DIR + localpath2 + stock_code + ".csv"
    localpath3 = '/jishu_stock/stockdata/data2015_2017/'  #
    stockdata_path3 = BASE_DIR + localpath3 + stock_code + ".csv"

    df1 = pd.read_csv(stockdata_path1, index_col=0)
    df2 = pd.read_csv(stockdata_path2, index_col=0)
    df = pd.read_csv(stockdata_path3, index_col=0)
    df = df.append(df2)  # 合并 2020 年之前的数据
    df = df.append(df1)  # 合并 2020 年之前的数据
    df = df.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从旧到新 排序

    # print df
    if (df.empty):
        return
    outpath = BASE_DIR + '/jishu_stock/stockdata/MONTH_DATA_K/' + stock_code + '_Month' + ".csv"
    cover_day_K_to_Month_K(df, outpath)

'''
https://waditu.com/document/2?doc_id=145

'''
def test_getTushare_Month_k():
    pro = ts.pro_api()

    df = pro.monthly(ts_code='000001.SZ', start_date='20180101', end_date='20181101',
                     fields='ts_code,trade_date,open,high,low,close,vol,amount')

    print df




if __name__ == '__main__':
    import datetime
    starttime = datetime.datetime.now()


    # test1()
    localpath1 = '/jishu_stock/stockdata/data1/'
    # getAllMonth_Kdata(localpath1)
    # test_cover_day_K_to_Month_K()
    test_getTushare_Month_k()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds