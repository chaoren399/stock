#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
龙战于野2 找 2 天的数据, 第 3 天盯盘

https://www.yuque.com/chaoren399/eozlgk/hafzse

第一步先判断 模型
 获取近 3 天的数据, 

第一天 涨停
第二天 大阴线
第三天, 阳线收盘价 高过阴线开盘价  



'''

def get_all_LongZhanYuYe2(localpath1):
    info1=  '--龙战于野2 -第 3 天盯盘start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:3]  # 前6行
        data6_1 = df.iloc[0:10]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_LongZhanYuYe2_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_LongZhanYuYe2_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        # 设置两个 key
        key_1=0; #是不是涨停板
        key_2=0; #次日大阴线


        day2_open=0
        day3_close=0
        day2_shiti=0
        for index,row in data1.iterrows():
            if(index==0 and isZhangTingBan(row)==1):
                key_1=1
            if(key_1==1):
                if(index==1 and isYinXian(row)==1): #次日大阴线
                    day2_open = row['open']
                    day2_shiti=getShiTiDaXiao(row)
                    # print1(day2_shiti)
                    if(day2_shiti >2.9):
                        key_2=1

        # print1(key_1)
        # print1(key_2)

        # print1(day2_shiti)
        if(key_1==1 and  key_2 ==1):
            info = ''
            info= info+ '阴线实体大于3.6最好:'+str(day2_shiti)

            info = info + "-----龙战于野2-第 3 天盯盘---"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '龙战于野2.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)





'''
测试自己的案例
'''
def test_isAn_LongZhanYuYe_ziji():

    #自己的 案例
    # 案例 2 本钢板材
    df1 = ts.pro_bar(ts_code='000761.SZ', adj='qfq', start_date='20210206', end_date='20210411')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_LongZhanYuYe2_model(data7_1, '000761.SZ')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        # data7_4 = df.iloc[22:42]  # 前10个交易日
        data7_4 = df.iloc[10:42]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 6 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_LongZhanYuYe2_model(data7_4[i:i + 6], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_LongZhanYuYe2(localpath1)
    # test_Befor_data()
    # test_isAn_LongZhanYuYe_laoshi()
    # test_isAn_LongZhanYuYe_ziji()