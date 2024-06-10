#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import *
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
起爆均线3（自研）判断   https://xueqiu.com/3476656801/204163278
思路: 
首先 找1个大阳线 穿越 起爆均线144,169的， 

然后144,169 都是向上的，

之前的最小值都是低于144,169的





QiBaoJunXian3

创建日期:2021年11月01日
更新日期: 
'''

def get_all_QiBaoJunXian3(localpath1):
    info1=  '--起爆均线3 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:20]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_QiBaoJunXian3_model(data6_1, stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_QiBaoJunXian3_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 4):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-1:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        data2= data[len_data-20:len_data-1]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #1. 阳线 穿越 144,169
        key_2=1; # 之前的数据最小值 都是在 144,160 之下

        count=0
        day1_open=0
        day1_close=0
        day1_144=0
        day1_169=0
        # 1. 阳线 穿越 144,169
        for index ,row in data1.iterrows():
            if(index==0 and isYangXian(row)==1):
                count=count+1
                day1_open=row['open']
                day1_close=row['close']

                day1_144=row['ma144']
                day1_169=row['ma169']
        if(count==1):
            if(day1_open < day1_144 and day1_open < day1_169):
                if(day1_close > day1_144 and  day1_close > day1_169):
                    key_1=1

        if(key_1==1):
             # 之前的数据最小值 都是在 144,160 之下
             for index, row in data2.iterrows():
                 day_low=row['low']
                 day_144 = row['ma144']
                 day_169 = row['ma169']
                 if(day_low > day_144 or day_low > day_169):
                     key_2=0

        # print1(key_1)
        # print1(key_2)

        if(key_1==1 and  key_2 ==1 ):
            info = ''
            if (is144_169_shangzhang(data2) == 2):
                info = info + '144-169满足上涨'
            else:
                info = info + '144-169不满足上涨'

            info = info + "-----起爆均线3----"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '起爆均线3.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

''''
判断 144.169 是不是上涨趋势, 发现 144 会变化, 但是 169 稳定上涨. 取 10 天的数据就可以
'''
def is144_169_shangzhang(data):
    ma144s=[]
    ma169s=[]
    count=0
    for index, row in data.iterrows():
        ma144s.append(round(row['ma144'],2))
        ma169s.append(round(row['ma169'],2))

    if(is_small_to_big(ma144s)==1 ):
        count=count+1
    if(is_small_to_big(ma169s)==1 ):
        count=count+1
    # print1(ma144s)
    # print1(ma169s)
    return count



'''
测试自己的案例
'''
def test_isAn_QiBaoJunXian3_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='600647.SH', adj='qfq', start_date='20200206', end_date='20211124',
                     ma=[5, 13, 34, 144, 169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian3_model(data7_1, '600647.SH')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        data7_4 = df.iloc[22:42]  # 前10个交易日
        len_1=len(data7_4)
        for i in range(0, len_1 - 20 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_QiBaoJunXian3_model(data7_4[i:i + 20], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_QiBaoJunXian3(localpath1)

    # test_isAn_QiBaoJunXian3_ziji()
    # test_Befor_data()