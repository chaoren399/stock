#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.is5_13_34_ShangZhang import is5_13_34_XiangShang
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
隔山打牛 放量中阳线 捕捉涨停
https://www.yuque.com/chaoren399/eozlgk/xokvyg/


① 前提是上涨初期或中期，即处于上涨结构（底底抬高顶顶抬高） 放量
② 明显的中阳线（和近期阴线比较，阳线实体要较大）
③ 成交量比前一个交易日明显放量
④ 后3个交易日的收盘价比中阳线的开盘价高，并且成交量都比中阳线的成交量低

需要 5 个数据
GeShanDaNiu

'''

def get_all_GeShanDaNiu(localpath1):
    info1=  '--隔山打牛 放量中阳线 捕捉涨停 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:5]  # 前6行
        data6_1 = df.iloc[0:35]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_GeShanDaNiu_model(data6_1, stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_GeShanDaNiu_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 5):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-5:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)
        data2=data[len_data-5-22:len_data-5]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #明显的中阳线（和近期阴线比较，阳线实体要较大）
        key_2=0;#成交量比前一个交易日明显放量
        key_3=0;  #后3个交易日的收盘价比中阳线的开盘价高，
        key_4=0; # 后3个交易日并且成交量都比中阳线的成交量低

        key_5=0; # 5-13-34 都是上涨的

        key_6=0; # 上涨初期, 阳线的收盘价 高于近 1 个月的 22 交易数据的 最高值


        day1_amount=0
        day2_amount=0
        day2_yangxian_shiti=0
        day2_open=0
        day2_close=0
        day3_close=0
        day3_amount=0
        day4_close=0
        day4_amount=0
        for index, row in data1.iterrows():
            if (index==0):
                day1_amount=row['amount']
            if(index==1 ): #中阳线

                day2_amount=row['amount']
                day2_yangxian_shiti=getShiTiDaXiao(row)
                is_day2_yangxian=isYangXian(row)
                day2_open=row['open']
                day2_close=row['close']

            if(index==2):
                day3_close=row['close']
                day3_amount=row['amount']
            if(index==3):
                day4_close=row['close']
                day4_amount=row['amount']
            if(index==4):
                day5_close=row['close']
                day5_amount=row['amount']

        if(is_day2_yangxian==1 and  day2_yangxian_shiti >1.6) :  #明显的中阳线（和近期阴线比较，阳线实体要较大）
            key_1=1

        if(day2_amount > day1_amount): #成交量比前一个交易日明显放量
            key_2=1
        #后3个交易日的收盘价比中阳线的开盘价高，
        if(day3_close > day2_open and day4_close > day2_open and day5_close > day2_open):
            key_3=1

        #后3个交易日并且成交量都比中阳线的成交量低
        if(day3_amount < day2_amount and day4_amount < day2_amount and day5_amount < day2_amount):
            key_4=1

        key_6 = 1;  # 上涨初期, 阳线的收盘价 高于近 1 个月的 22 交易数据的 最高值
        for index, row in data2.iterrows():
            high= row['high']
            if(high > day2_close):
                key_6=0
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_6==1):
            count3=is5_13_34_XiangShang(data1,0)
            if(count3>1):
                info=''
                info=info+'5-13-34 有 '+str(count3)+'个上升-'
                info = info + "-----隔山打牛 放量中阳线 捕捉涨停 " + ' ----' + stockcode + ' ----' + str(riqi)
                # print info
                writeLog_to_txt(info, stockcode)

                #单独处理 隔山打牛的 每天运行的结果, 后期回测使用 .
                #/Users/mac/PycharmProjects/gitproject/stock/

                # path = BASE_DIR + '/jishu_stock/jishu_stock/GeShanDaNiu/隔山打牛.txt'
                path = '隔山打牛.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试老师的案例
'''
def test_isAn_GeShanDaNiu_laoshi():
    # 案例 1
    df1 = ts.pro_bar(ts_code='002010.SZ',adj='qfq', start_date='20210206', end_date='20210607',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_GeShanDaNiu_model(data7_1,'002010.SZ')

    # 案例 2 600171
    df1 = ts.pro_bar(ts_code='600171.SH',adj='qfq', start_date='20210206', end_date='20210524',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_GeShanDaNiu_model(data7_1,'600171.SH')

    # 案例 3 000429  案例 3 和4 出现的日期不一样  放量中阳线 捕捉涨停  ----000429.SZ ----20210208--粤高速A**000429.SZ
    df1 = ts.pro_bar(ts_code='000429.SZ',adj='qfq', start_date='20200206', end_date='20210219 ',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_GeShanDaNiu_model(data7_1,'000429.SZ')

    # 案例 4 000429   案例 3 和4 出现的日期不一样  -----000429.SZ ----20210129--粤高速A**000429.SZ
    df1 = ts.pro_bar(ts_code='000429.SZ',adj='qfq', start_date='20200206', end_date='20210204',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_GeShanDaNiu_model(data7_1,'000429.SZ')

'''
测试自己的案例
'''
def test_isAn_GeShanDaNiu_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_GeShanDaNiu_model(data7_1,'002507.SZ')

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
            isAn_GeShanDaNiu_model(data7_4[i:i + 3], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_GeShanDaNiu(localpath1)
    test_isAn_GeShanDaNiu_laoshi()