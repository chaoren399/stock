#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.z_tool.isXiongShiMoQi import isXiongShiMoQi
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
死灰复燃
https://www.yuque.com/chaoren399/eozlgk/meu5lk
创建日期:2021年11月21日
修改日期:
急速下跌熊市末期
(连续至少3根阴线有低开有中/大阴线)
小阳线止跌(最低价不能创新低)
次日小阴线(最低价不能创新低)
次日中阳线且收盘价高过小阴线的开盘价
以近期最低价做止损

写一个工具 专门判断 急速下跌  (连续至少3根阴线有低开有中/大阴线)

还需要判断 是不是 最近半年最低值 

SiHuiFuRan

'''

def get_all_SiHuiFuRan(localpath1):
    info1=  '--死灰复燃 要看出现的位置2start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:66]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_SiHuiFuRan_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_SiHuiFuRan_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        # print data
        data1= data[len_data-3:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        data2= data[len_data-6:len_data-3]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        #还需要判断 是不是 最近半年最低值

        data3= data[0:len_data-6]
        data3 = data3.reset_index(drop=True)  # 重新建立索引 ,

        # print1(data2)

        if( isXiongShiMoQi(data2) ==1 ): #熊市末期
            mini_price= getMin_low_fromDataFrame(data2) # 最低价


            # 设置两个 key
            key_1=0; #第一天小阳线止跌(最低价不能创新低)
            key_2=0;#次日小阴线(最低价不能创新低)
            key_3=0;#次日中阳线且收盘价高过小阴线的开盘价
            key_4=0; # 还需要判断 是不是 最近半年最低值

            count=0
            day1_low=0
            day2_low=0
            day2_open=0
            day3_close=0
            for index,row in data1.iterrows():
                if(index==0 and isYangXian(row)==1 ):
                    count=count+1
                    day1_low= row['low']
                if(index==1 and isYinXian(row)==1 ):
                    count=count+1
                    day2_low = row['low']
                    day2_open=row['open']
                if(index==2 and isYangXian(row)==1 ):
                    count=count+1
                    day3_close=row['close']

            if(count==3): #

                #1#第一天小阳线止跌(最低价不能创新低)
                if(day1_low > mini_price) :
                    key_1=1
                #2#次日小阴线(最低价不能创新低)
                if(day2_low >= mini_price):
                    key_2=1
                #次日中阳线且收盘价高过小阴线的开盘价
                if(day3_close > day2_open):
                    key_3=1

                # 还需要判断 是不是 最近半年最低值
                if (key_1 == 1 and key_2 == 1 and key_3 == 1):
                    data3_min= getMin_low_fromDataFrame(data3)
                    if(data3_min > mini_price):
                        key_4=1


            #
            # print1(key_1)
            # print1(key_2)
            # print1(key_3)
            # print1(key_4)
            # print1(mini_price)
            # print1(day2_low)


            if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1):
                # 还需要判断 是不是 最近半年最低值

                info = ''

                info = info + "--死灰复燃--"  + str(riqi)
                # print info
                writeLog_to_txt(info, stockcode)
                path = '死灰复燃.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例
'''
def test_isAn_SiHuiFuRan_laoshi():
    # 案例 1  000420
    df1 = ts.pro_bar(ts_code='000420.SZ',adj='qfq', start_date='20200206', end_date='20210114')
    data7_1 = df1.iloc[0:106]  # 前7行
    isAn_SiHuiFuRan_model(data7_1,'000420.SZ')

    # 案例 2
    df1 = ts.pro_bar(ts_code='600187.SH',adj='qfq', start_date='20200206', end_date='20210802')
    data7_1 = df1.iloc[0:106]  # 前7行
    isAn_SiHuiFuRan_model(data7_1,'600187.SH')

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_SiHuiFuRan_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_SiHuiFuRan_model(data7_1,'002507.SZ')

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
        data7_4 = df.iloc[22:98]  # 前128个交易日
        data7_4 = df.iloc[44:120]  # 前128个交易日
        len_1=len(data7_4)
        for i in range(0, len_1 - 66 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_SiHuiFuRan_model(data7_4[i:i + 66], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_SiHuiFuRan(localpath1)
    # test_isAn_SiHuiFuRan_laoshi()
    # test_Befor_data()