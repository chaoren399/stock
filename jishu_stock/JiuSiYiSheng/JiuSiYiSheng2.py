#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1, \
    writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR

''''
九死一生 2 底部弱势反转
https://www.yuque.com/chaoren399/eozlgk/rq72h1/


熊市未期急速下跌
收第1根止跌阳线计数为
3日内再收阳线
第3天收盘价高于连续阴线最后1根阴线的开盘价

思路:   前 4 天数据 固定,  后边的选出 20 天的数据 第 20 天为最小值


'''

def get_all_JiuSiYiSheng_2(localpath1):
    info1=  '--九死一生 2 底部弱势反转  熊市未期急速下跌 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:24]  # 前24行
        data6_1 = df.iloc[0:68]  # 前68行



        isAn_JiuSiYiSheng_2_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JiuSiYiSheng_2_model(data,stockcode):
    # print len(data)
    len_data=len(data)
    if(len_data==0):
        print str(stockcode)+'--data --is null'
    if(len_data >= 4):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data
        riqi = data.ix[len_data-1]['trade_date']

        data1 = data[len_data-4:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        # print data1
        data2= data[len_data-4-64:len_data-4]
        data2 = data2.reset_index(drop=True)  #  前 20 个数据重新建立索引 ,
        # print data2
        data3 = data[len_data - 14:len_data-4] # 10 个数据
        data3 = data3.reset_index(drop=True)

        # 设置两个 key
        key_1=0; #  是阴线
        key_2=0; # 是阳线
        key_3=0; #最后一天是

        key_4=1; # 前 20 天是不是下跌过程
        key_5=0; # 前 10 天 需要出现跳空  这样才能判断是不是急速下跌

        day1_yin_open=0
        day3_yang_close=0

        for index,row in data1.iterrows():
            # print 1
            if(index==0 and isYangXian(row)==0) : #第一天是阴线
                key_1=1
                day1_yin_open=row['open']
            if(index==1 and isYangXian(row)==1): #第 2 天是阳线
                key_2=1
            if(index==3 and isYangXian(row)==1): # 第 3 天不管, 第 4 天是阳线
                day3_yang_close=row['close']

        day_xiadie_close_min = data2.ix[len(data2)-1]['close']

        for index,row in data2.iterrows(): #前 2个月 下跌过程
            close_price= row['close']
            if(close_price < day_xiadie_close_min):
                key_4=0


        if(day3_yang_close > day1_yin_open ):  #  第 4 天阳线的收盘价 必须高于 第 1天阴线的开盘价
            key_3=1

        # print(data3)
        #前 10 天 需要出现跳空  这样才能判断是不是急速下跌  找第一天的最低点和 第 2 天的 最高点

        if(hasTiaoKong(data3)==1):
            key_5=1

        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)

        if(key_1 ==1 and  key_2==1 and key_3==1 and key_4==1 and key_5==1 ):


            # print  "第一次符合模型"
            info = "----九死一生2 底部弱势反转 --"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '九死一生2.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

'''
#前 10 天 需要出现跳空  这样才能判断是不是急速下跌  找第一天的最低点和 第 2 天的 最高点
'''
def hasTiaoKong(data3):
    count3 = 0
    for index, row in data3.iterrows():
        if (index == 0):
            day0_low = row['low']
        if (index == 1):
            day1_high = row['high']
            day1_low = row['low']
            if (day0_low > day1_high):
                count3 = count3 + 1
        if (index == 2):
            day2_high = row['high']
            day2_low = row['low']
            if (day1_low > day2_high):
                count3 = count3 + 1
        if (index == 3):
            day3_high = row['high']
            day3_low = row['low']
            if (day2_low > day3_high):
                count3 = count3 + 1
        if (index == 4):
            day4_high = row['high']
            day4_low = row['low']
            if (day3_low > day4_high):
                count3 = count3 + 1
        if (index == 5):
            day5_high = row['high']
            day5_low = row['low']
            if (day4_low > day5_high):
                count3 = count3 + 1
        if (index == 6):
            day6_high = row['high']
            day6_low = row['low']
            if (day5_low > day6_high):
                count3 = count3 + 1
        if (index == 7):
            day7_high = row['high']
            day7_low = row['low']
            if (day6_low > day7_high):
                count3 = count3 + 1
        if (index == 8):
            day8_high = row['high']
            day8_low = row['low']
            if (day7_low > day8_high):
                count3 = count3 + 1
        if (index == 9):
            day9_high = row['high']
            day9_low = row['low']
            if (day8_low > day9_high):
                count3 = count3 + 1
    if(count3>0):
        return 1
    # print1(count3)

    return 0



def test_isAn_JiuSiYiSheng_2_model_laoshi():

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # 打印最新的数据

    #测试案例 1
    df1 = ts.pro_bar(ts_code='300151.SZ', start_date='20210630', end_date='20210729')
    data7_1 = df1.iloc[0:24]  # 前4行
    isAn_JiuSiYiSheng_2_model(data7_1,'300151.SZ')

    # 测试案例 2
    df2 = ts.pro_bar(ts_code='600100.SH', start_date='20210603', end_date='20210803')
    data7_2 = df2.iloc[0:24]  # 前4行
    isAn_JiuSiYiSheng_2_model(data7_2, '600100.SH')

    # 测试案例 3
    df3 = ts.pro_bar(ts_code='688008.SH', start_date='20210403', end_date='20210513')
    data7_3 = df3.iloc[0:24]  # 前4行
    isAn_JiuSiYiSheng_2_model(data7_3, '688008.SH')


def test_isAn_JiuSiYiSheng_2_model_ziji():

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # 打印最新的数据

    #测试案例 1 ----九死一生2 底部弱势反转 --002232.SZ --20211011--启明信息

    df1 = ts.pro_bar(ts_code='002232.SZ', start_date='20210630', end_date='20211011')
    data7_1 = df1.iloc[0:24]  # 前4行
    isAn_JiuSiYiSheng_2_model(data7_1,'002232.SZ')


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
        # data6_1 = df.iloc[0:24]  # 前24行  # 必须 24 个数据
        # data6_1 = df.iloc[24:48]  # 前24行
        data6_1 = df.iloc[22:112]  # 前24行 22+68 +22
        # data6_1 = df.iloc[22:72]  # 前24行
        # isAn_JiuSiYiSheng_2_model(data6_1, stock_code)

        len_1=len(data6_1)

        for i in range(0, len_1 - 68 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JiuSiYiSheng_2_model(data6_1[i:i + 68], stock_code)

if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_JiuSiYiSheng_2(localpath1)
    test_isAn_JiuSiYiSheng_2_model_laoshi()
    # test_isAn_JiuSiYiSheng_2_model_ziji()
    # test_Befor_data()