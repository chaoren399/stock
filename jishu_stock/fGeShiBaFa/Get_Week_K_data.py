#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR

'''


https://www.jb51.net/article/213955.htm
日K 转换为 周K


https://tushare.pro/register?reg=456282 
'''

def cover_day_K_to_Week_K(df,outpath):
    if(len(df)==0):
        return 0

    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d', errors='coerce')

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)


    # 获取周k
    df_week = pd.DataFrame()

    df_week['open'] = df['open'].resample('W').first()
    df_week['close'] = df['close'].resample('W').last()
    df_week['high'] = df['high'].resample('W').max()
    df_week['low'] = df['low'].resample('W').min()

    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    # data=data.dropna(axis=0, how='all', inplace=True)
    df_week = df_week.dropna(how='any', axis=0)
    df_week.sort_index(axis=1, ascending=True)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序

    df_week.to_csv(outpath)

    return 1

def getAllWeekKdata(localpath1):
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        # localpath1 ='/jishu_stock/stockdata/data1/'
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        # df =  pd.read_csv(stockdata_path, dtype={'code': str})
        df = pd.read_csv(stockdata_path, index_col=0)
        # print df
        if (df.empty):
            return
        outpath= BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code +'_Week'+ ".csv"
        cover_day_K_to_Week_K(df,outpath)
        count = count+1
        print count


if __name__ == '__main__':
    import datetime
    starttime = datetime.datetime.now()


    # test1()
    localpath1 = '/jishu_stock/stockdata/data1/'
    getAllWeekKdata(localpath1)

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds