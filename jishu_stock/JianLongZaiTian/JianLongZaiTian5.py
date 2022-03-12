#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.aShengLv.huice.ShengLv_10_5 import jisuan_all_shouyilv_10_5
from jishu_stock.z_tool.is5_13_34_ShangZhang import is5_10_20_XiangShang_dayou
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''

见龙在田3 判断 3个 K 线 , 一阳一阴一阳  跳空高开的理解 2021年12月17日
https://www.yuque.com/chaoren399/eozlgk/hrz8ri/

第一天阳线, 第 2 天 高开的小阴线, 第 3天阳线 收盘价高过 第 2 天的 开盘价,  (没有跳空) 跳空高开是指开盘价格高过昨日收盘价

这 3 天的收盘价 和开盘价都在 5 日均线以上

修改: 2022年02月21日 跳空高开理解更正: 今天的开盘价 大于昨天的最高价




JianLongZaiTian5

创建日期: 2021年11月06日
更新日期: 2021年12月17日

'''
chengongs=[]
modelname='见龙在田5'
def get_all_JianLongZaiTian5(localpath1):
    info1=  '--见龙在田5 start--   '
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
        isAn_JianLongZaiTian5_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JianLongZaiTian5_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=False)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-3:len_data]
        data1 = data1.reset_index(drop=False)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)
        mairuriqi=0
        zhisundian=0

        data2 = data[len_data -10:len_data]
        data2 = data2.reset_index(drop=False)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #1 阳线后面跳空高开小阴线
        key_2=0;# 2 第 3 天跳空的阳线

        key_3=0; #上涨趋势
        key_4=1;  # 开盘价和收盘价是不是 在 5 日均线之上

        count=0
        day1_close=0
        day1_high=0
        day2_open=0
        day3_close=0

        for index, row in data1.iterrows():
            if(index==0 and isYangXian(row)==1):
                count=count+1
                day1_close=row['close']
                day1_high=row['high']
                zhisundian=row['low']
            if(index==1 and isYinXian(row)==1):
                count=count+1
                day2_open = row['open']
            if(index==2and isYangXian(row)==1):
                count=count+1
                day3_close = row['close']
                mairuriqi=row['trade_date']

        if(count==3):

            # if(day2_open > day1_close ): #修改: 2022年02月21日 跳空高开理解更正: 今天的开盘价 大于昨天的最高价
            if(day2_open > day1_high ): #修改: 2022年02月21日 跳空高开理解更正: 今天的开盘价 大于昨天的最高价
                key_1=1
            if(day3_close > day2_open):
                key_2=1

        # if(is5_10_20_XiangShang_dayou(data2,0) ==1):
        #     key_3=1

        for index, row in data1.iterrows():
            if (row['ma5'] > row['open'] or row['ma5'] > row['close']):
                key_4 = 0

        # print1(key_1)
        # print1(key_2)
        # # print1(key_3)
        # print1(key_4)

        # if(key_1==1 and key_2 ==1  and key_3==1):
        if(key_1==1 and key_2 ==1 and key_4==1 ):
        # if( key_2 ==1 and key_3 ==1 and key_4 ==1):
            info = ''

            info = info + "--见龙在田5--"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '见龙在田5.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_JianLongZaiTian5_laoshi():
    # 案例 1 603799 华友钴业
    df1 = ts.pro_bar(ts_code='603799.SH',adj='qfq', start_date='20210206', end_date='20210707',ma=[5, 10,20])
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_JianLongZaiTian5_model(data7_1,'603799.SH')

    # 案例 2 000420
    df1 = ts.pro_bar(ts_code='000420.SZ',adj='qfq', start_date='20200206', end_date='20210205',ma=[5, 10,20])
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_JianLongZaiTian5_model(data7_1,'000420.SZ')

    # 案例 3比亚迪 1
    df1 = ts.pro_bar(ts_code='002594.SZ',adj='qfq', start_date='20200206', end_date='20210608',ma=[5, 10,20])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_JianLongZaiTian5_model(data7_1,'002594.SZ')





'''
测试自己的案例
'''
def test_isAn_JianLongZaiTian1_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='000635.SZ',adj='qfq', start_date='20210206', end_date='20211202')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_JianLongZaiTian5_model(data7_1,'000635.SZ')

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

        # data7_4 = df.iloc[22:22+10+10]  # 前1个个月
        data7_4 = df.iloc[22:22+10+22]  # 前1个个月
        # data7_4 = df.iloc[22:22+10+120]  # 半年
        # data7_4 = df.iloc[22:22+10+250]  # 前1年
        len_1=len(data7_4)
        for i in range(0, len_1 - 10 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JianLongZaiTian5_model(data7_4[i:i + 10], stock_code)

    # jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    # jisuan_all_shouyilv(chengongs, modelname, 1.15)

    jisuan_all_shouyilv_10_5(chengongs, modelname, 1.10, 0.95)
    jisuan_all_shouyilv_10_5(chengongs, modelname, 1.05, 0.95)

if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_JianLongZaiTian5(localpath1)
    # test_isAn_JianLongZaiTian5_laoshi()
    test_Befor_data()
    # test_isAn_JianLongZaiTian5_ziji()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"