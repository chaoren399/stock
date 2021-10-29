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
缺口理论, 凌波微步
https://www.yuque.com/chaoren399/kb/ayfh2g

价格筑底 后  要有几天的横盘, 1-2 周吧, 3 天也可以

1, 找到 6 日的数据 

2 ,第一天 ,第 2 天是 缺口, 且第 2 天是阳线  第 3,4,5,6 天中  最小值 大于 第一天的 最大值


'''

def get_all_LingBoWeiBu(localpath1):
    info1=  '--缺口理论, 凌波微步 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[2:8]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_LingBoWeiBu_model(data6_1, stock_code)

        # print len1
        for i in range(0, len1 - 3 + 1):

            isKanglongyouhui_3Days_data(dataframe_df[i:i + 3], stockcode)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_LingBoWeiBu_model(data,stockcode):
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
        print1(data1)

        # 设置两个 key
        key_1=0;
        key_2=0;

        print1(key_1)
        print1(key_2)
        if(key_1==1 and  key_2 ==1):
            info = ''

            info = info + "-----缺口理论, 凌波微步  成功了"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)


'''
测试老师的案例
'''
def test_isAn_ShenLongBaiWei2_laoshi():
    # 案例 1
    df1 = ts.pro_bar(ts_code='000408.SZ',adj='qfq', start_date='20210206', end_date='20210518')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_model(data7_1,'002174.SZ')

    # 案例 2

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_DaYou_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_DaYou_model(data7_1,'002507.SZ')

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
            isAn_FeiLongZaiTian_model(data7_4[i:i + 3], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_LingBoWeiBu(localpath1)