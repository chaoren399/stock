#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    is_small_to_big, writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''

创建日期:2021年10月26日
更新日期:

神奇日均线组合 5-13-34 

思路: 



'''

def get_all_5_13_34(localpath1):
    info1=  '--神奇日均线组合 5-13-34 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        df = df.round(2)
        df['ma5_13_cha'] = df['ma5'] - df['ma13']


        data6_1 = df.iloc[0:10]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_5_13_34_model(data6_1, stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_5_13_34_model(data,stockcode):
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
        riqi = data1.ix[1]['trade_date']  # 阳线的日期
        # print1(data1)

        # df = data1[['ts_code', 'trade_date', 'open', 'ma5', 'ma13', 'ma34','ma5_13_cha']]
        # print1(df)

        # 设置两个 key
        key_1=0; # 当天5-13 是不是为 0
        key_2=0; # 前一天是不是5-13  <0
        key_3=0; # 当天是不是 为中阳线

        key_4=1; # 34日均线 是不是 小于 k线
        key_5=0; #34 日均线是不是 上升趋势
        key_6=0; ## 死叉 后快速金叉

        day2_ma5_13_cha=0
        day2_yangxian_shiti=0
        for index,row in data1.iterrows():
            ma5_13_cha = row['ma5_13_cha']
            if(index==0):
                if(ma5_13_cha < 0):
                    key_2=1

            if(index==1 and isYangXian(row)==1): # 最新的一天
                day2_ma5_13_cha=ma5_13_cha
                # if(ma5_13_cha>=0  and ma5_13_cha < 0.039 ):
                # if( abs(ma5_13_cha) <0.09  ):
                if( abs(ma5_13_cha) <0.12 ):
                    key_1=1
                day2_yangxian_shiti=getShiTiDaXiao(row)

        if(day2_yangxian_shiti > 1.6):
            key_3=1

         # 34日均线 是不是 小于 k线

        for index,row in data.iterrows():
            daylow=row['low']
            ma34=row['ma34']
            if(daylow < ma34):
                key_4=0

        key_5 = 0;  # 34 日均线是不是 上升趋势
        ma34s=[]

        count6=0
        for index, row in data.iterrows():
            ma34s.append(row['ma34'])
            if( row['ma5_13_cha'] <0):
                count6=count6+1


        if(is_small_to_big(ma34s)==1):
            key_5=1

        if(count6 <10): # 死叉 后快速金叉 4个值最好
            key_6=1

        # print1(data1)
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(key_6)
        # print1(day2_ma5_13_cha)

        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1 and key_6==1):
            info = ''

            info = info + "-----神奇日均线组合 5-13-34 " + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '5-13-34.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试老师的案例
'''
def test_isAn_5_13_34_laoshi():
    # 案例 1-----神奇日均线组合 5-13-34  ----002006.SZ ----20210709--精功科技--强势股票**002006.SZ
    df = ts.pro_bar(ts_code='002006.SZ',adj='qfq', start_date='20210206', end_date='20210709',ma=[5, 13, 34])
    df = df.round(2)
    df['ma5_13_cha'] = df['ma5'] - df['ma13']
    data7_1 = df.iloc[0:10]  # 前7行
    isAn_5_13_34_model(data7_1,'002006.SZ')

    # 案例 2 300161 -----神奇日均线组合 5-13-34  -票**300161.SZ
    df = ts.pro_bar(ts_code='300161.SZ',adj='qfq', start_date='20210206', end_date='20210819',ma=[5, 13, 34])
    df = df.round(2)
    df['ma5_13_cha'] = df['ma5'] - df['ma13']
    data7_1 = df.iloc[0:10]  # 前7行
    isAn_5_13_34_model(data7_1,'300161.SZ')

    # 案例 3 600200 -----神奇日均线组合 5-13-34  ----600200.SH ----20210427--江苏吴中**600200.SH
    df = ts.pro_bar(ts_code='600200.SH',adj='qfq', start_date='20210206', end_date='20210427',ma=[5, 13, 34])
    df = df.round(2)
    df['ma5_13_cha'] = df['ma5'] - df['ma13']
    data7_1 = df.iloc[0:10]  # 前7行
    isAn_5_13_34_model(data7_1,'600200.SH')

    # 案例 4 -----神奇日均线组合 5-13-34  ----600238.SH ----20210526--海南椰岛**600238.SH
    df = ts.pro_bar(ts_code='600238.SH',adj='qfq', start_date='20210206', end_date='20210526',ma=[5, 13, 34])
    df = df.round(2)
    df['ma5_13_cha'] = df['ma5'] - df['ma13']
    data7_1 = df.iloc[0:10]  # 前7行
    isAn_5_13_34_model(data7_1,'600238.SH')

    # 案例 5 day2_ma5_13_cha = -0.11
    df = ts.pro_bar(ts_code='300068.SZ',adj='qfq', start_date='20210206', end_date='20210723',ma=[5, 13, 34])
    df = df.round(2)
    df['ma5_13_cha'] = df['ma5'] - df['ma13']
    data7_1 = df.iloc[0:10]  # 前7行
    isAn_5_13_34_model(data7_1,'300068.SZ')

    #
    # 案例 6  ----神奇日均线组合 5-13-34  ----000411.SZ ----20200723--英特集团**000411.SZ
    df = ts.pro_bar(ts_code='000411.SZ',adj='qfq', start_date='20200206', end_date='20200723',ma=[5, 13, 34])
    df = df.round(2)
    df['ma5_13_cha'] = df['ma5'] - df['ma13']
    data7_1 = df.iloc[0:10]  # 前7行
    isAn_5_13_34_model(data7_1,'000411.SZ')

'''
测试自己的案例
'''
def test_isAn_5_13_34_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    print data7_1
    isAn_5_13_34_model(data7_1,'002507.SZ')

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
        df = df.round(2)
        df['ma5_13_cha'] = df['ma5'] - df['ma13']

        data7_4 = df.iloc[22:42]  # 前10个交易日
        len_1=len(data7_4)
        for i in range(0, len_1 - 5 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_5_13_34_model(data7_4[i:i + 5], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_5_13_34(localpath1)
    # test_isAn_5_13_34_laoshi()
    # test_Befor_data()