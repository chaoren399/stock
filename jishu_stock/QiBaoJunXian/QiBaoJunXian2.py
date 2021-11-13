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
起爆均线2
https://www.yuque.com/chaoren399/eozlgk/gnyngx/

思路: 找到 144, 169 这两条均线  先测试一下 这 2 条均线 


找4 个数据, 前 2 个 是阴线, 而且最低值要高于 144,169. 这样判断是不是下跌趋势.

 后两个数据 第一个是阴线, 穿越 144-169 , 第 2 个是阳线, 而且收盘价 要高于 144-169 
之后 几天要观察是不是出现 向上的中阳线.



QiBaoJunXian2

创建日期:2021年11月01日
更新日期: 
'''

def get_all_QiBaoJunXian2(localpath1):
    info1=  '--起爆均线2 start--   '
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
        isAn_QiBaoJunXian2_model(data6_1, stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_QiBaoJunXian2_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 4):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-4:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        data2= data[len_data-10:len_data]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; # 判断 前 2 个数据 是不是阴线,并且最低值高于 144-169
        key_2=0; # 第 3 天阴线下穿 144 169
        key_3=0; # 判断第 4天 阳线收盘价是不是在 144-169 之上

        count=0
        day1_low=0
        day1_144=0
        day1_169=0
        day2_low=0
        day2_144=0
        day2_169=0
        day3_low=0
        day3_high=0
        day3_144=0
        day3_169=0
        day4_close=0
        day4_144=0
        day4_169=0
        for index, row in data1.iterrows():
            if(index==0 and isYinXian(row)==1): #第一个阴线
                count=count+1
                day1_low=row['low']
                day1_144=row['ma144']
                day1_169=row['ma169']

            if(index==1 and isYinXian(row)==1):#第2个阴线
                count=count+1
                day2_low=row['low']
                day2_144=row['ma144']
                day2_169=row['ma169']

            if(index==2 and isYinXian(row)==1): #第 3 天阴线下穿 144 169
                count=count+1
                day3_low=row['low']
                day3_high=row['high']
                day3_144=row['ma144']
                day3_169=row['ma169']

            if(index==3 and isYangXian(row)==1): #阳线
                count=count+1
                day4_close=row['close']

                day4_144=row['ma144']
                day4_169=row['ma169']

        if(count==4):
            # 判断 前 2 个数据 是不是阴线,并且最低值高于 144-169
            if(day1_low > day1_144 and day1_low > day2_169 and day2_low > day2_144 and day2_low>day2_169):
                key_1=1
            # 第 3 天阴线下穿 144 169
            if(day3_low < day3_144 and day3_low < day3_169 and day3_high > day3_144 and day3_high > day3_169):
                key_2=1

            # 判断第 4天 阳线收盘价是不是在 144-169 之上
            if(day4_close > day4_144 and day4_close > day4_169):
                key_3=1



            #
            # print1(key_1)
            # print1(key_2)
            # print1(key_3)

            if(key_1==1 and  key_2 ==1 and key_3==1):
                info = ''
                if (is144_169_shangzhang(data) == 2):
                    info = info + '144-169满足上涨'
                else:
                    info = info + '144-169不满足上涨'

                info = info + "-----起爆均线2----"  + str(riqi)
                # print info
                writeLog_to_txt(info, stockcode)
                path = '起爆均线2.txt'
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
测试老师的案例
'''
def test_isAn_QiBaoJunXian2_laoshi():

    # 案例 1 起爆均线 2 海源复材--强势股票**002529.SZ
    df1 = ts.pro_bar(ts_code='002529.SZ',adj='qfq', start_date='20200206', end_date='20210428',ma=[5, 13, 34,144,169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian2_model(data7_1,'002529.SZ')


    # 案例 2  起爆均线 2  600103
    df1 = ts.pro_bar(ts_code='600103.SH',adj='qfq', start_date='20200206', end_date='20210729',ma=[5, 13, 34,144,169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian2_model(data7_1,'600103.SH')

'''
测试自己的案例
'''
def test_isAn_QiBaoJunXian2_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_QiBaoJunXian2_model(data7_1,'002507.SZ')

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
            isAn_QiBaoJunXian2_model(data7_4[i:i + 3], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_QiBaoJunXian2(localpath1)
    # test_isAn_QiBaoJunXian2_laoshi()