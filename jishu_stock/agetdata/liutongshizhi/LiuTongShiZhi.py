#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts
import sys
import pandas as pd
from jishu_stock.Tool_jishu_stock import dingshi_ceshi

from jishu_stock.z_tool.PyDateTool import getDayNumberYMD
from stock.settings import BASE_DIR

'''
流通市值 获取

https://tushare.pro/document/2?doc_id=32


circ_mv		流通市值（万元）

'''

localpath = '/jishu_stock/stockdata/'  # 数据存放路径
LiuTongshizhibiao_path = BASE_DIR + localpath +'流通市值表.csv'

df = pd.read_csv(LiuTongshizhibiao_path, index_col=0)
len_df = len(df)

def get_LiuTongShiZhi():
    pro = ts.pro_api()

    today= getDayNumberYMD()
    # today ='20220218'
    df = pro.daily_basic(ts_code='', trade_date=today,
                         fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb,circ_mv')

    len_df = len(df)
    if(len_df> 4000): # 如果是周末 数据是空的
        #把数据 存入 csv, 方便后期使用.
        df.to_csv(LiuTongshizhibiao_path )

        # print df
'''
根据tscode 获取 流通市值 （万元）
'''
def get_oneStock_LTSZ(stock_code):
    # stock_code = '000627.SZ'

    if(len_df>4000):
        for index,row in df.iterrows():
            ts_code= row['ts_code']
            if(ts_code==stock_code):
                # print row['circ_mv']
                return row['circ_mv']


'''
流通市值 （万元）是不是小于 100 亿 是 返回 1
'''
def LTSZ_IS_Small_100YI(stock_code):
    ts_ltsz= get_oneStock_LTSZ(stock_code)
    # print str( ts_ltsz )+'--'+stock_code
    # print
    if(ts_ltsz < 1000000):
        return 1
    return 0

'''
从 股票池中 得到流通市值小于 100 亿的股票池
'''
def get_my_gupiaochi_xioayu_100_yi():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        ts_code= row['ts_code']
        if(LTSZ_IS_Small_100YI(ts_code)==1):
            print ts_code


if __name__ == '__main__':
    print  "定时测试"
    # get_LiuTongShiZhi()
    # print get_today_str()
    # print LTSZ_IS_Small_100YI('300005.SZ')
    get_my_gupiaochi_xioayu_100_yi()
    # print float(20) / float(26)