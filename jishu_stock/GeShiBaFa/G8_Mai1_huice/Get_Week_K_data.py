#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import print1
from stock.settings import BASE_DIR

'''


https://www.jb51.net/article/213955.htm
日K 转换为 周K

https://tushare.pro/register?reg=456282 
'''
def getAllWeekKdata(localpath1):
    print '日K 转换为 周K'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
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
        df = df.append(df1)  # 合并 2020 年之前的数据
        # print df
        if (df.empty):
            return
        outpath= BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code +'_Week'+ ".csv"
        print str(count) + '--' + stock_code

        cover_day_K_to_Week_K(df,outpath)

        count = count+1
        # print count


def cover_day_K_to_Week_K(df,outpath):
    if(len(df)==0):
        return 0
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d', errors='coerce')
    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    # print df
    df = df.dropna(how='any', axis=0)#删除 列数据为空的 的行
    # df = df[0:450]

    # 获取周k
    df_week = pd.DataFrame()

    df_week['open'] = df['open'].resample('W').first()
    df_week['close'] = df['close'].resample('W').last()
    df_week['high'] = df['high'].resample('W').max()
    df_week['low'] = df['low'].resample('W').min()
    # print1(len(df_week))
    df_week = df_week.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    df_week['Week10-60'] = df_week['WeekMa10'] - df_week['WeekMa60'] # G8 买 2 用到


    df_week = df_week.dropna(how='any', axis=0)#删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print  df_week
    df_week.to_csv(outpath)

    return 1


def test_002319():
    # stock_code='002319.SZ'
    # stock_code='002297.SZ'
    stock_code='000001.SZ'
    localpath1 = '/jishu_stock/stockdata/data1/'
    stockdata_path1 = BASE_DIR + localpath1 + stock_code + ".csv"
    localpath2 = '/jishu_stock/stockdata/data2020/'  #
    stockdata_path2 = BASE_DIR + localpath2 + stock_code + ".csv"

    df1 = pd.read_csv(stockdata_path1, index_col=0)
    df = pd.read_csv(stockdata_path2, index_col=0)
    df = df.append(df1)  # 合并 2020 年之前的数据
    # print df
    print1(len(df))
    if (df.empty):
        return
    outpath = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    print '--' + stock_code


    cover_day_K_to_Week_K(df, outpath)
'''
测试一个股票转化为 周 K 
'''
def test_cover_day_K_to_Week_K():


    stock_code='000001.SZ'
    outpath = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"

    localpath1 = '/jishu_stock/stockdata/data1/'
    stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    print df
    cover_day_K_to_Week_K(df, outpath)


if __name__ == '__main__':
    import datetime
    starttime = datetime.datetime.now()


    # test1()
    localpath1 = '/jishu_stock/stockdata/data1/'
    getAllWeekKdata(localpath1)
    # test_002319()
    # test_cover_day_K_to_Week_K() #测试一个股票转化为 周 K

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds