#!/usr/bin/python
# -*- coding: utf8 -*-
from stock.settings import BASE_DIR
import tushare as ts
import pandas as pd
from jishu_stock.z_tool.PyDateTool import getDayNumberYMD

'''
流通市值 获取

https://tushare.pro/document/2?doc_id=32


circ_mv		流通市值（万元）

'''

localpath = '/jishu_stock/z_stockdata/'  # 数据存放路径

LiuTongshizhibiao_path = BASE_DIR + localpath +'流通市值表.csv'
df = pd.read_csv(LiuTongshizhibiao_path, index_col=0)
len_df = len(df)



'''
更新 最新的流通市值的数据, 最好每周更新一次
'''
def get_LiuTongShiZhi():

    pro = ts.pro_api()

    today= getDayNumberYMD()
    today ='20220323'  #节假日或者周五 是没有数据的


    df = pro.daily_basic(ts_code='', trade_date=today,
                         fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb,circ_mv')

    len_df = len(df)
    # print len_df
    # if(len_df> 4000): # 如果是周末 数据是空的
    if(len_df> 0): # 如果是周末 数据是空的
        #把数据 存入 csv, 方便后期使用.
        df.to_csv(LiuTongshizhibiao_path )

        print df

'''
根据tscode 获取  基本面指标 

https://tushare.pro/document/2?doc_id=32
数据是本地的数据
'''
def get_stock_jibenmian(stock_code):
    if (len_df > 0):
        for index, row in df.iterrows():
            ts_code = row['ts_code']
            if (ts_code == stock_code):
                # print row['circ_mv']
                return row

'''
根据tscode 获取 流通市值 返回（亿元） 跟下边的get_oneStock_LTSZ 返回 万不一样

'''
def get_oneStock_liutongshizhi(stock_code):
    if (len_df > 0):
        for index, row in df.iterrows():
            ts_code = row['ts_code']
            if (ts_code == stock_code):
                # print row['circ_mv']

                liutongshizhi = row['circ_mv'] / 10000
                liutongshizhi = round(liutongshizhi,1)
                return str(liutongshizhi) + '亿'

'''
根据tscode 获取 流通市值 （万元）
'''
def get_oneStock_LTSZ(stock_code):
    # stock_code = '000627.SZ'
    liutongshizhi = 0
    # if(len_df>4000):
    if(len_df>0):
        for index,row in df.iterrows():
            ts_code= row['ts_code']
            if(ts_code==stock_code):
                # print row['circ_mv']

                liutongshizhi = row['circ_mv']
                return   liutongshizhi


'''
流通市值 （万元）是不是小于 100 亿 是 返回 1
shizhimax =100 表示 100 亿
'''
def LTSZ_IS_Small_100YI(stock_code,shizhimax):
    ts_ltsz= get_oneStock_LTSZ(stock_code)
    # print str( ts_ltsz )+'--'+stock_code
    # print
    # if(ts_ltsz < 1000000):
    if(ts_ltsz < shizhimax * 10000):
        return 1
    return 0

'''
从 股票池中 得到流通市值小于 100 亿的股票池
'''
def get_my_gupiaochi_xioayu_100_yi():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        ts_code= row['ts_code']
        if(LTSZ_IS_Small_100YI(ts_code)==1):
            print ts_code


if __name__ == '__main__':
    print  "定时测试"

    get_LiuTongShiZhi()
    # print get_today_str()
    # print LTSZ_IS_Small_100YI('300005.SZ')
    # get_my_gupiaochi_xioayu_100_yi()
    # print float(20) / float(26)