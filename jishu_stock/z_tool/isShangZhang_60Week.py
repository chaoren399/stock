#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1, is_big_to_small
from jishu_stock.z_tool.MyPath import getweekdata_path_with_stockcode
from stock.settings import BASE_DIR



'''
60周均线是不是一直上涨的 , 根据 实时在线获取,传入 指定的日期
'''
def is_60WEEK_ShangZhang_with_number(stock_code,riqi,number):
    # print1(riqi)
    df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20180101', end_date=str(riqi))

    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    # print df
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行

    # print df
    df_week = df

    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    df_week['Week10-60'] = df_week['WeekMa10'] - df_week['WeekMa60']  # G8 买 2 用到

    df_week = df_week.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print  df_week[0:10]
    df_week = df_week[0:number] #一年有 48 周
    WeekMa60=[]
    for index, row in df_week.iterrows():
        WeekMa60.append(row['WeekMa60'])

    if(is_big_to_small(WeekMa60)==1):
        return 1
    return 0



'''
60周均线是不是一直上涨的 , 根据 实时在线获取,传入 指定的日期
'''
def is_60WEEK_ShangZhang(stock_code,riqi):
    # print1(riqi)
    df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20180101', end_date=str(riqi))

    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    # print df
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行

    # print df
    df_week = df

    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    df_week['Week10-60'] = df_week['WeekMa10'] - df_week['WeekMa60']  # G8 买 2 用到

    df_week = df_week.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print  df_week[0:10]
    df_week = df_week[0:24] #一年有 48 周
    WeekMa60=[]
    for index, row in df_week.iterrows():
        WeekMa60.append(row['WeekMa60'])

    if(is_big_to_small(WeekMa60)==1):
        return 1
    return 0



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
