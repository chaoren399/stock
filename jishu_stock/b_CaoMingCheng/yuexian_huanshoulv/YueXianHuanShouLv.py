#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
月线换手率 

思路来源,  庄家的破绽 第 17 页, 

找到最近 5 个月换手率 累计大于 300%的股票
YueXianHuanShouLv
'''
chengongs=[]
modelname='月线换手率1'


def get_all_YueXianHuanShouLv(localpath1):
    info1=  '--5 个月换手率 累计大于 300 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'

    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    if (len(data) > 0):

        for index, row in data.iterrows():
            stock_code = row['ts_code']
            #/Users/mac/PycharmProjects/baostock/z_stockdata/
            bs_path='/Users/mac/PycharmProjects/baostock/z_stockdata/'
            stockdata_path = bs_path+ 'MONTH_DATA_K/' + stock_code + '_Month' + ".csv"
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                continue
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df

            df = df.iloc[0:20]  # 前10个交易日
            isAn_YueXianHuanShouLv_model(df, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YueXianHuanShouLv_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 5):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        # data1= data[len_data-5:len_data]
        data1= data[len_data-3:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        # riqi = data1.ix[0]['trade_date']  # 阳线的日期
        riqi = 0
        # print1(data1)

        # 设置两个 key
        key_1=0; #

        huanshoulv_all =0
        for index, row in data1.iterrows():
            # huanshoulv = row['turn']
            huanshoulv_all=huanshoulv_all+row['turn']


        if(huanshoulv_all >290):
            key_1=1

        # print1(key_1)
        # print1(huanshoulv_all)
        if(key_1==1 ):
            info = ''+stockcode

            info = info + "-----5 个月换手率 累计大于 300 成功了"  + str(riqi)+'-换手率:'+str(huanshoulv_all)

            info = info + '--' + get_Stock_Name(stockcode)
            print info



'''
测试老师的案例
'''
def test_isAn_YueXianHuanShouLv_laoshi():
    # 案例 1
    df1 = ts.pro_bar(ts_code='000408.SZ',adj='qfq', start_date='20210206', end_date='20210518')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_YueXianHuanShouLv_model(data7_1,'002174.SZ')

    # 案例 2

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_YueXianHuanShouLv_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_YueXianHuanShouLv_model(data7_1,'002507.SZ')

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
            isAn_YueXianHuanShouLv_model(data7_4[i:i + 3], stock_code)



if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_YueXianHuanShouLv(localpath1)


    endtime = time()
    print "总共运行时长:"+str(round((endtime - starttime) / 60 ,2))+"分钟"