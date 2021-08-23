#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time
import tushare as ts
import pandas as pd
'''


https://www.jb51.net/article/213955.htm
日K 转换为 周K


'''

def test1():

    df = ts.pro_bar(ts_code='300068.SZ', start_date='20190628', end_date='20210823', ma=[50, 300])

    # 进行转换，周线的每个变量都等于那一周最后一个交易日的变量值
    # period_stock_data = stock_data.resample(period_type, how = 'last')
    # 日期 格式  转为为 2019-11-22
    import pandas as pd
    # stock_data['trade_date'] = pd.to_datetime(stock_data['trade_date'], unit='s', origin=pd.Timestamp('2018-07-01'))
    df['trade_date'] =pd.to_datetime(df['trade_date'], format='%Y%m%d', errors='coerce')

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)

    #获取周k
    df_week = pd.DataFrame()
    df_week ['open'] = df['open'].resample('W').first()
    df_week['close'] = df['close'].resample('W').last()
    df_week['high'] = df['high'].resample('W').max()
    df_week['low'] = df['low'].resample('W').min()
    print df_week[0:10]
    df_week.to_csv('1.csv')


def convert_date(d):
    # print d
    day = d
    '20210820'
    d1 = day[0:4]
    d2 =day[4:6]
    d3 = day[6:8]
    d = d3+'/'+d2+'/'+d1
    # return parse(d).weekday()
    return d

if __name__ == '__main__':
    test1()