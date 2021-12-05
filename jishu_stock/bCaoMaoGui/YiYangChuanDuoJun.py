#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import *
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi
import pandas as pd
# 显示所有列
# pd.set_option('display.max_columns', None)
# 显示所有行
# pd.set_option('display.max_rows', None)

''''
一阳穿多均
https://www.yuque.com/chaoren399/byftms/rp1pzx

1、盘整或刚破位时，突然走出一-根大阳线
2、-次性突破了3根以上的常用均线
3、突破的均线数量越多越好
4、均线之间的距离越小越好
5、大阳线的收盘价离被突破的均线距离越远越好

YiYangChuanDuoJun

'''

def get_all_YiYangChuanDuoJun(localpath1):
    info1=  '--一阳穿多均 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_YiYangChuanDuoJun_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YiYangChuanDuoJun_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-1:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        # 设置两个 key
        key_1=0; #判断 阳线 穿越了几个阳线, 满足 3 根的就可以
        key_2=0; # 必须是中大阳线

        count=0
        day1_shiti=0
        for index,row in data1.iterrows():
            if(index==0 and isYangXian(row)==1):
                day1_shiti=getShiTiDaXiao(row)
                ma5=row['ma5']
                ma10=row['ma10']
                ma20=row['ma20']
                ma30=row['ma30']
                ma60=row['ma60']
                day1_open=row['open']
                day1_close=row['close']
                if(day1_open  < ma5 and day1_close > ma5):
                    count=count+1
                if(day1_open  < ma10 and day1_close > ma10):
                    count=count+1
                if(day1_open  < ma20 and day1_close > ma20):
                    count=count+1
                if(day1_open  < ma30 and day1_close > ma30):
                    count=count+1
                if(day1_open  < ma60 and day1_close > ma60):
                    count=count+1

            if(count >=4 ):
                key_1=1
            # if(day1_shiti > 1.6):
            if(day1_shiti > 3.5):
                key_2=1


        # print1(key_1)
        # print1(day1_shiti)

        if(key_1==1 and key_2==1 ):
            info = ''

            info = info + "---一阳穿多均 成功了"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '一阳穿多均.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试老师的案例
'''
def test_isAn_YiYangChuanDuoJun_laoshi():
    # 案例 1
    df1 = ts.pro_bar(ts_code='002384.SZ',adj='qfq', start_date='20180206', end_date='20190130',ma=[5, 13, 34, 144, 169, 75,10,20,30,60])
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_YiYangChuanDuoJun_model(data7_1,'002384.SZ')

    # 案例 2

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_YiYangChuanDuoJun_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_YiYangChuanDuoJun_model(data7_1,'002507.SZ')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        data7_4 = df.iloc[22:42]  # 前10个交易日
        len_1=len(data7_4)
        for i in range(0, len_1 - 3 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_YiYangChuanDuoJun_model(data7_4[i:i + 3], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_YiYangChuanDuoJun(localpath1)
    test_isAn_YiYangChuanDuoJun_laoshi()