#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian, isYinXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from stock.settings import BASE_DIR

''''
柳暗花明 底部反转模型
https://www.yuque.com/chaoren399/eozlgk/bl5cum

熊市末期急速下跌
连续3日以上的阴线
包含低开和大阴线
止跌阳线阳线的收盘价高过前一日阴线开盘价
以最低点作为止损

思路: 找到 4个数据

编写日期: 2021年10月15日
更新日期: 2021年10月19日
'''

def get_all_LiuAnHuaMing(localpath1):
    info1=  '--柳暗花明 底部反转模型 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:136]  # 前6行
        # data6_1 = df.iloc[1:136]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_LiuAnHuaMing_model(data6_1, stock_code)

'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_LiuAnHuaMing_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 4):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1=data[len_data-4:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        # print1( data1)
        riqi = data1.ix[0]['trade_date']  # 阳线的日期

        data2 = data[0:len_data - 4] #

        # 设置两个 key
        key_1=0; #判断 是不是 三个阴 一个阳线
        key_2=0; #判断有没有低开
        key_3=0; # 有没有大阴线


        key_4=0; # 止跌阳线阳线的收盘价高过前一日阴线开盘价

        key_5=1; # 近 3 个月必须是下跌状态

        count=0
        day3_open=0
        day4_close=0
        day1_shiti=0
        day2_shiti=0
        day3_shiti=0
        day3_low=0
        for index,row in data1.iterrows():

            if(index==0 and isYinXian(row)==1):
                count=count+1
                day1_shiti=getShiTiDaXiao(row)

            if(index==1 and isYinXian(row)==1):
                count=count+1
                day2_shiti=getShiTiDaXiao(row)
            if(index==2 and isYinXian(row)==1):
                count=count+1
                day3_open=row['open']
                day3_shiti=getShiTiDaXiao(row)
                day3_low = row['low']
            if(index==3 and isYangXian(row)==1):
                count=count+1
                day4_close= row['close']
        if(count==4):#判断 是不是 三个阴 一个阳线
            key_1=1

        if(key_1==1 and hasDiKai(data1)==1):
            key_2=1

        dayinxian_biaozhun=1.5 # 大阴线的标准 可以调节
        if(day1_shiti > dayinxian_biaozhun or day2_shiti > dayinxian_biaozhun or day3_shiti > dayinxian_biaozhun): #有没有大阴线
            key_3=1

        if(day4_close >= day3_open): #止跌阳线阳线的收盘价高过前一日阴线开盘价
            key_4=1




        # 近 3 个月必须是下跌状态
        if (key_1 == 1):
            for index, row in data2.iterrows():
                if (row['low'] < day3_low):
                    key_5 = 0
        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(day1_shiti)
        # print1(day2_shiti)
        # print1(day3_shiti)

        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1):
            info = "-----柳暗花明 底部反转 ----"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '柳暗花明.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

'''
判断是不是大阴线 
# chazhi = ((day2_close - day2_open) / day2_open) * 100 #  (开盘价-收盘价)÷开盘价＜0.5%
'''
def isDaYinXian(row):
    day_close=row['close']
    day_open=row['open']
    chazhi =  ((day_close - day_open) / day_open) * 100
    return chazhi
''''
如果有低开 那么 返回 1 
'''
def hasDiKai(data):
    day0_close=0
    day1_open=0
    day1_close=0
    day2_open=0

    count=0
    for index, row in data.iterrows():
        if (index == 0 ):
            day0_close=row['close']

        if (index == 1 ):
            day1_open = row['open']
            day1_close=row['close']
            if(day1_open < day0_close):
                count = count + 1

        if (index == 2 ):
            day2_open=row['open']
            if(day2_open < day1_close):
                count = count + 1


    if(count>=1):
        return 1

    return 0


'''
测试老师的案例
'''
def test_isAn_LiuAnHuaMing_laoshi():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例 1600200.SH ----20210128--江苏吴中
    df1 = ts.pro_bar(ts_code='600200.SH',adj='qfq', start_date='20200206', end_date='20210202')
    data7_1 = df1.iloc[0:136]  # 前7行
    isAn_LiuAnHuaMing_model(data7_1,'600200.SH')


    # 案例 2000157.SZ ----20181016--中联重科
    df1 = ts.pro_bar(ts_code='000157.SZ',adj='qfq', start_date='20180206', end_date='20181019')
    data7_1 = df1.iloc[0:136]  # 前7行
    # print df1.iloc[0:7]  # 前7行
    isAn_LiuAnHuaMing_model(data7_1,'000157.SZ')

'''
测试自己的案例
'''
def test_isAn_LiuAnHuaMing_ziji():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)

    #自己的 案例 -----柳暗花明 底部反转 ----000710.SZ ----20210820--贝瑞基因
    df1 = ts.pro_bar(ts_code='000710.SZ',adj='qfq', start_date='20180206', end_date='20210820')
    data7_1 = df1.iloc[0:136]  # 前7行
    # print df1.iloc[0:7]  # 前7行
    isAn_LiuAnHuaMing_model(data7_1,'000710.SZ')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        data7_4 = df.iloc[22:168]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 136 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_LiuAnHuaMing_model(data7_4[i:i + 136], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # test_isAn_LiuAnHuaMing_laoshi()
    get_all_LiuAnHuaMing(localpath1)
    # test_Befor_data()
    # test_isAn_LiuAnHuaMing_ziji()