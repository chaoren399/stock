#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.PyDateTool import get_date1_date2_days
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from jishu_stock.z_tool.getMin_Max import getMin_fromDataFrame
from stock.settings import BASE_DIR
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
出水芙蓉 主力底部强势洗盘
https://www.yuque.com/chaoren399/eozlgk/tpxgic

下跌止跌缓慢上涨
阴线阳线组合
阳线的最高价高过阴线最高价
阳线的最低价高过阴线最低价
阳线的收盘价高过阴线的开盘价
以阴线的最低价作为止损
止盈参考亢龙有悔

思路 : 选出 2 个数据
ChuShuiFuRong

创建日期:2021年10月21日 

发现 很多数据, 都不是刚刚上涨, 怎么办?  
拿出 132 天的 半年的数据,  找到最低点, 然后判断 最低点 和 出水芙蓉的日期 相差几天,如果在 22 个交易日内 就可以.


'''

def get_all_ChuShuiFuRong(localpath1):
    info1=  '--出水芙蓉 主力底部强势洗盘--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:132]  # 前132行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ChuShuiFuRong_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ChuShuiFuRong_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        data2= data[0: len_data]

        # 设置两个 key
        key_1=0;  #首先是 判断是不是 阴阳组合
        key_2=0;

        #阳线的最高价高过阴线最高价
        # 阳线的最低价高过阴线最低价
        # 阳线的收盘价高过阴线的开盘价

        key_3=0; #阴线实体要大一些 0.5
        key_4=0;#出水芙蓉与最低值相差小于 22 日

        count=0
        day1_high = 0
        day1_low = 0
        day1_open = 0
        day2_high = 0
        day2_low = 0
        day2_close = 0
        day1_shiti=0

        for index, row in data1.iterrows():
            if(index==0 and isYinXian(row)==1):
                count=count+1
                day1_high = row['high']
                day1_low = row['low']
                day1_open= row['open']
                day1_shiti=getShiTiDaXiao(row)
            if(index==1 and isYangXian(row)==1):
                count = count + 1
                day2_high=row['high']
                day2_low=row['low']
                day2_close=row['close']

        if(count==2):
            key_1=1
        if(day2_high > day1_high and day2_low > day1_low and day2_close > day1_open):
            key_2=1

        if(day1_shiti > 0.08 ):
            key_3=1



        if(key_1==1 and key_2==1):
            # print1(data2)
            min_row = getMin_fromDataFrame(data2)
            if(min_row is  None):
                print 'min_row  is None'
            # print min_row
            # print min_row['open']
            min_row_riqi =  min_row['trade_date']

            # print1(min_row_riqi)
            days_chahzi=get_date1_date2_days(min_row_riqi,riqi) # 出水芙蓉与最低值相差几天
            # print days_chahzi
            if(int(days_chahzi) < 22 and int(days_chahzi) > 3 ):
                key_4=1

        # print1(key_1)
        # print1(key_2)
        # print1(day1_shiti)
        # if(key_1==1 and  key_2 ==1 and key_3==1):
        if(key_1==1 and  key_2 ==1 and key_4==1):
            info = ''
            info= info+'阴线实体='+str(day1_shiti)

            info = info + "-----出水芙蓉 主力底部强势洗盘 ----"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '出水芙蓉.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例 
'''
def test_isAn_ChuShuiFuRong_laoshi():

    # 案例 1 600000.SH ----20201113--浦发银行
    df1 = ts.pro_bar(ts_code='600000.SH',adj='qfq', start_date='20200206', end_date='20201116')
    data7_1 = df1.iloc[0:132]  # 前7行
    isAn_ChuShuiFuRong_model(data7_1,'600000.SH')

    # 案例 2 600004.SH ----20210208--白云机场
    df1 = ts.pro_bar(ts_code='600004.SH', adj='qfq', start_date='20200206', end_date='20210209')
    data7_1 = df1.iloc[0:132]  # 前7行
    isAn_ChuShuiFuRong_model(data7_1, '600004.SH')

    # 案例 3
    df1 = ts.pro_bar(ts_code='600007.SH', adj='qfq', start_date='20200206', end_date='20210219')
    data7_1 = df1.iloc[0:132]  # 前7行
    isAn_ChuShuiFuRong_model(data7_1, '600007.SH')

'''
测试自己的案例
'''
def test_isAn_ChuShuiFuRong_ziji():
    # 阴线实体=0.05-----出水芙蓉 主力底部强势洗盘 ----20211022--至正股份--强势股票**603991.SH

    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:136]  # 前7行
    isAn_ChuShuiFuRong_model(data7_1,'002507.SZ')

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


        data7_4 = df.iloc[22:42]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 2 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ChuShuiFuRong_model(data7_4[i:i + 2], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_ChuShuiFuRong(localpath1)
    # test_isAn_ChuShuiFuRong_laoshi()