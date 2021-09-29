#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import print1
from jishu_stock.fGeShiBaFa.GeShiBaFa_Pro import isAn_GEShi8_model
from stock.settings import BASE_DIR


'''
https://tushare.pro/document/2?doc_id=109

前复权  周数据 


-----葛式八法---000685.SZ ----9.45--强势股票----中山公用


'''
def test_fuquan():

    df = ts.pro_bar(ts_code='000685.SZ', adj='qfq',freq	='W',start_date='20180101', end_date='20210922')

    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序
    # df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    # df.set_index('trade_date', inplace=True)

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

    # print df[0:10]

    df = df_week

    df1 = df.iloc[0:4]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据
    df2 = df.iloc[0:8]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据

    isAn_GEShi8_model(df1,df2, '000685.SZ')

if __name__ == '__main__':
    test_fuquan()