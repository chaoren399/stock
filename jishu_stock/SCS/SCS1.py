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

https://www.yuque.com/chaoren399/eozlgk/ptugwf
创建日期:2021年11月26日
更新日期
思路： 拿出 6天数据， 找到 最后一天 判断是不是小K线 并且 缩量。 然后在找有没有光脚阴线。 再判断有没有 跳空下杀， 还有 阳线失败案例。

最后 2 天 一个阴线,一个小阳线,  小阳线缩量最好.


'''

def get_all_SCS_1(localpath1):
    info1=  '--SCS_1 start--   '
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
        isAn_SCS_1_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_SCS_1_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        data2 = data[len_data - 6:len_data]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        #拿出 6天数据， 找到 最后一天 判断是不是小K线 并且 缩量。
        # 然后在找有没有光脚阴线。 再判断有没有 跳空下杀， 还有 阳线失败案例。

        # 设置两个 key
        key_1=0; # 1是不是小 K 线
        key_2=0; # 2.低位缩量
        key_3=0; #3. 光脚阴线
        key_4=0; #4 . 跳空下杀
        key_5=0; # 5. 阳线失败

        # 1是不是小 K 线
        #2.低位缩量
        day1_amount=0
        day2_amount=0
        day1_k_shiti=0
        day2_k_shiti=0
        count=0
        for index, row in data1.iterrows():
            if(index==0 ):
                day1_amount=row['amount']
                day1_k_shiti = getShiTiDaXiao(row)
                if( isYinXian(row)==1):
                    count=count+1
            if(index==1 ):
                day2_amount=row['amount']
                day2_k_shiti=getShiTiDaXiao(row)
                if(isYangXian(row)==1):
                    count=count+1

        if(count==2):
            #1是不是小 K 线
            day2_k_shiti=day2_k_shiti+0.00001
            day1_day2_shiti_beishu=day1_k_shiti / day2_k_shiti
            if(day1_day2_shiti_beishu > 2):
                key_1=1
            # 2.低位缩量
            if(day2_amount < day1_amount):
                key_2=1

            # 3. 光脚阴线
            for index, row in data2.iterrows():
                if(getyinxian_xiayingxian(row)<0.5):
                    key_3=1
            # 4 . 跳空下杀
            len_data2 = len(data2)
            for i in range(0, len_data2 - 2 + 1):
                # print "i" + str(i )+ "j"+str(i+3)
                if(isTiaoKongXiaSha(data2[i:i + 2])==1):
                    key_4=1
            # 5. 阳线失败
            for i in range(0, len_data2 - 3 + 1):
                if (isYangXianShiBai(data2[i:i + 3]) == 1):
                    key_5 = 1

            # print1(key_1)
            # print1(key_2)
            # print1(key_3)
            # print1(key_4)
            # print1(key_5)
            # print1(day1_day2_shiti_beishu)
            if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1):
                info = ''

                info = info + "-----SCS1 成功了"  + str(riqi)
                # print info
                writeLog_to_txt(info, stockcode)
                path = 'SCS1.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
判断是否有 阳线失败:
https://xueqiu.com/3476656801/204267227
总结, 只要3根 K 线, 阴阳阴, 就说明是阳线失败 (自己总结)

晓波老师在第一节强势题材股里讲得调整特征里，第五点的阳线失败，指的在这个模型下，
下杀过程中出现了阳线，阳线后收出阴线，
这个模型下属于阳线失败；
在第一讲里老师讲了10几个案例图哦，可以反复观看这个模型并进行按图索骥去模拟以及实战哈。


如果是阳线失败,返回 1 , 否则返回 0
'''
def isYangXianShiBai(data):
    data = data.reset_index(drop=True)  # 重新建立索引 ,
    count=0
    for index, row in data.iterrows():
        if(index==0 and isYinXian(row)==1):
            count=count+1
        if(index==1 and isYangXian(row)==1):
            count=count+1
        if(index==2 and isYinXian(row)==1):
            count=count+1
    if(count==3):
        return 1
    return 0

'''
判断是还不是跳空下杀, 是 返回 1 
'''
def isTiaoKongXiaSha(data):
    data = data.reset_index(drop=True)  # 重新建立索引 ,
    day1_open=0
    day1_close=0
    day2_open=0
    day2_close=0
    for index, row in data.iterrows():
        if(index==0):
            day1_open= row['open']
            day1_close= row['close']
        if(index==1):
            day2_open= row['open']
            day2_close= row['close']

    if(day2_open < day1_open and day2_open < day1_close):
        if(day2_close < day1_open and day2_close < day1_close):
            return 1

    return 0

'''
判断是不是 光脚阴线 ,是返回 1 , 暂时放弃使用词函数, 太严谨.
'''
def is_guangjiaoyinxian(row):
    if(isYinXian(row)==1):
        if(row['close'] == row['low']):
            return 1

    return 0

'''
获取下影线的长度   主要用来 判断 光脚阴线, 放大了范围
因为每个K 线 计量大小不一样,我们用比值的方式来统一
'''
def getyinxian_xiayingxian (row):
    if(isYinXian(row)==1):
        shitidaxiao = row['open'] -row['close'] + 0.00001
        xiayignxiandaxiao = row['close'] -row['low']

        return xiayignxiandaxiao / shitidaxiao

    return 10

'''
测试老师的案例2
'''
def test_isAn_SCS_1_laoshi1():
    # 案例 1
    df1 = ts.pro_bar(ts_code='000889.SZ',adj='qfq', start_date='20200206', end_date='20200401')

    data7_1 = df1.iloc[0:6]  # 前7行
    # print data7_1
    isAn_SCS_1_model(data7_1,'000889.SZ')

    # 案例 2

    # 案例 3
'''
测试老师的案例2 
课件案例的倒数 3 个案例

2-晓波老师强势题材股战法11.24笔记(1)
'''
def test_isAn_SCS_1_laoshi2():
    # 案例 1  (保力新)坚瑞沃能
    df1 = ts.pro_bar(ts_code='300116.SZ',adj='qfq', start_date='20200206', end_date='20200831')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_SCS_1_model(data7_1,'300116.SZ')

    # 案例 2 大连重工  002204
    df1 = ts.pro_bar(ts_code='002204.SZ',adj='qfq', start_date='20200206', end_date='20200525')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_SCS_1_model(data7_1,'002204.SZ')

    # 案例 3 百联股份600827
    df1 = ts.pro_bar(ts_code='600827.SH', adj='qfq', start_date='20200206', end_date='20200629')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_SCS_1_model(data7_1, '600827.SH')
    # 案例 4 聚龙股份 300202 20200413
    df1 = ts.pro_bar(ts_code='300202.SZ', adj='qfq', start_date='20200206', end_date='20200413')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_SCS_1_model(data7_1, '300202.SZ')

'''
测试自己的案例
'''
def test_isAn_SCS_1_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_SCS_1_model(data7_1,'002507.SZ')

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
        data7_4 = df.iloc[22:30]  # 前10个交易日
        len_1=len(data7_4)
        for i in range(0, len_1 - 6 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_SCS_1_model(data7_4[i:i + 6], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_SCS_1(localpath1)
    # test_isAn_SCS_1_laoshi1()
    # test_isAn_SCS_1_laoshi2()
    test_Befor_data()