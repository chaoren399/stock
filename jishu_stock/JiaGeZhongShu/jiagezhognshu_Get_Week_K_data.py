#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import print1
from stock.settings import BASE_DIR
import datetime
'''
价格中枢 获取 周数据,  因为 要周三 周四 看到 本周的周数据, tushare 没有办法获取, 
只能用此程序自己转化了.

https://www.jb51.net/article/213955.htm
价格中枢 专用   日K 转换为 周K

https://tushare.pro/register?reg=456282 
'''
def getAll_jiagezhongshu_WeekKdata(localpath1):
    print '价格中枢 专用  日K 转换为 周K'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        # localpath1 ='/jishu_stock/stockdata/data1/'
        stockdata_path1 = BASE_DIR + localpath1 + stock_code + ".csv"
        localpath2 = '/jishu_stock/stockdata/data2020/'   #
        stockdata_path2 = BASE_DIR + localpath2 + stock_code + ".csv"

        df1 = pd.read_csv(stockdata_path1, index_col=0)
        df = pd.read_csv(stockdata_path2, index_col=0)
        df = df.append(df1,sort=True)  # 合并 2020 年之前的数据
        # print df

        if (df.empty):
            return
        outpath= BASE_DIR + '/jishu_stock/stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code +'_Week'+ ".csv"
        print str(count) + '--' + stock_code

        cover_day_K_to_Week_K(df,outpath)
        count = count+1
        # print count


def cover_day_K_to_Week_K(df,outpath):
    # print1(len(df))
    if(len(df)==0):
        return 0
    # print  df['trade_date']
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d', errors='coerce')

    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序
    # print df
    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)


    # print df

    # 获取周k
    df_week = pd.DataFrame()
    # df_week['ts_code']=df['ts_code']
    # df_week['trade_date']=df['trade_date']
    #2021-11-14
    df_week['open'] = df['open'].resample('W').first()
    df_week['close'] = df['close'].resample('W').last()
    df_week['high'] = df['high'].resample('W').max()
    df_week['low'] = df['low'].resample('W').min()



    df_week = df_week.dropna(how='any', axis=0)#删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)

    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序

    # print1(len(df_week))
    df_week.to_csv(outpath)

    return 1

'''
测试一个股票转化为 周 K 
'''
def test_000001():
    # stock_code='002319.SZ'
    # stock_code='002297.SZ'
    stock_code='000001.SZ'
    localpath1 = '/jishu_stock/stockdata/data1/'
    stockdata_path1 = BASE_DIR + localpath1 + stock_code + ".csv"
    localpath2 = '/jishu_stock/stockdata/data2020/'  #
    stockdata_path2 = BASE_DIR + localpath2 + stock_code + ".csv"

    df1 = pd.read_csv(stockdata_path1, index_col=0)
    df = pd.read_csv(stockdata_path2, index_col=0)
    df = df.append(df1,sort=True)  # 合并 2020 年之前的数据
    # print df
    # print1(len(df))
    if (df.empty):
        return
    outpath = BASE_DIR + '/jishu_stock/stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    print '--' + stock_code


    cover_day_K_to_Week_K(df, outpath)



if __name__ == '__main__':
    starttime = datetime.datetime.now()

    localpath1 = '/jishu_stock/stockdata/data1/'
    getAll_jiagezhongshu_WeekKdata(localpath1)
    # test_000001() #测试一个股票转化为 周 K













    endtime = datetime.datetime.now()
    print  "总共运行时长:" +str((endtime - starttime).seconds)
