#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from stock.settings import BASE_DIR
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''

九死一生1-底部强势反转
https://www.yuque.com/chaoren399/eozlgk/lp8wzh/
熊市未期急速下跌
连续阴线的最后一根阴线是中阴线/大阴线
(最好最后一根阴线实体最大)
中阳线/大阳线高开高收

思路:  选出最近 的 4 个数据,  前 3 个是 阴线, 最后一个是 中阳线/大阳线高开高收


九死一生 1 的模型, 如果在下跌过程中出现, 成功概率是 12 / (12+9) =0.57
九死一生 1 的模型, 如果在上涨过程中出现, 成功概率是 36/ (36+8) =0.81  (高胜率策略)


'''

def get_all_jiusiyisheng1(localpath1):
    info1=  '--九死一生1-底部强势反转 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:4]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_jiusiyisheng1_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_jiusiyisheng1_model(data,stockcode):
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

        # 设置两个 key
        key_1=0;# 3个阴线 1 个阳线
        key_2=0; #最后是一个大阴线
        key_3=0; # 大阳线
        key_4=0; #大阳线高开高收

        count=0
        day3_yinxian_shiti=0
        day4_yangxian_shiti=0
        for index, row in data1.iterrows():
            if(index==0 and isYinXian(row)==1):
                count=count+1
            if(index==1 and isYinXian(row)==1):
                count=count+1
            if(index==2 and isYinXian(row)==1):
                count=count+1
                day3_yinxian_shiti=getShiTiDaXiao(row)
                day3_open=row['open']
                day3_close=row['close']

            if(index==3 and isYangXian(row)==1):
                count=count+1
                day4_yangxian_shiti=getShiTiDaXiao(row)
                day4_open=row['open']
                day4_close=row['close']


        if(count==4):
            key_1=1

            if(day3_yinxian_shiti > 3.5):
                key_2 =1
            if(day4_yangxian_shiti > 1.6):
                key_3=1

            if(day4_open > day3_close and  day4_close > day3_open):
                key_4=1


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(day3_yinxian_shiti)



        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 ):
            info = ''
            info=info+'大阴线实体='+str(day3_yinxian_shiti)

            info = info + "-----九死一生1-底部强势反转 ----" + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '九死一生1.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例
'''
def test_isAn_jiusiyisheng1_laoshi():

    # 案例 1大阴线实体=5.4-----九死一生1-底部强势反转 ----20210726--山东威达**002026.SZ
    df1 = ts.pro_bar(ts_code='002026.SZ', start_date='20210726', end_date='20210729')
    data7_1 = df1.iloc[0:4]  # 前4行
    isAn_jiusiyisheng1_model(data7_1,'002026.SZ')

    # 案例 3 鲁阳节能 大阴线实体=3.86-----九死一生1-底部强势反转 ----20210726--鲁阳节能--强势股票**002088.SZ
    df1 = ts.pro_bar(ts_code='002088.SZ', start_date='20210630', end_date='20210729')
    data7_1 = df1.iloc[0:4]  # 前4行
    isAn_jiusiyisheng1_model(data7_1,'002088.SZ')


    # # 案例 4  最后一个阴线有点小day3_yinxian_shiti = 0.95
    df1 = ts.pro_bar(ts_code='600173.SH', start_date='20200630', end_date='20210218')
    data7_1 = df1.iloc[0:4]  # 前4行
    isAn_jiusiyisheng1_model(data7_1,'600173.SH')


    # # 案例 3 阳线实体太小, 不满足  day3_yinxian_shiti = 3.23
    df1 = ts.pro_bar(ts_code='600160.SH', start_date='20210630', end_date='20210705')
    data7_1 = df1.iloc[0:4]  # 前4行
    isAn_jiusiyisheng1_model(data7_1,'600160.SH')

    # 案例 2 day3_yinxian_shiti = 2.1
    df1 = ts.pro_bar(ts_code='300114.SZ', start_date='20210519', end_date='20210524')
    data7_1 = df1.iloc[0:4]  # 前4行
    isAn_jiusiyisheng1_model(data7_1,'300114.SZ')
'''
测试自己的案例
'''
def test_isAn_jiusiyisheng1_ziji():

    #自己的 案例
    df1 = ts.pro_bar(ts_code='000656.SZ',adj='qfq', start_date='20210206', end_date='20211021')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_jiusiyisheng1_model(data7_1,'000656.SZ')

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


        data7_4 = df.iloc[22:32]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 4 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_jiusiyisheng1_model(data7_4[i:i + 4], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_jiusiyisheng1(localpath1)
    # test_isAn_jiusiyisheng1_laoshi()
    # test_isAn_jiusiyisheng1_ziji()
    # test_Befor_data()