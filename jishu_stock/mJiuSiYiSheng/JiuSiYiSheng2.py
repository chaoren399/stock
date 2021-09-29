#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1
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

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:24]  # 前24行


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
        data2= data[0:len_data-4]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,
        # print data2

        # 设置两个 key
        key_1=0; #  是阴线
        key_2=0; # 是阳线
        key_3=0; #最后一天是

        key_4=1; # 前 20 天是不是下跌过程

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

        for index,row in data2.iterrows():
            close_price= row['close']
            if(close_price < day_xiadie_close_min):
                key_4=0


        if(day3_yang_close > day1_yin_open ):  #  第 4 天阳线的收盘价 必须高于 第 1天阴线的开盘价
            key_3=1

        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        if(key_1 ==1 and  key_2==1 and key_3==1 and key_4==1 ):


            # print  "第一次符合模型"
            info = "----九死一生2 底部弱势反转" + ' --' + stockcode + ' --' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)


def test_isAn_JiuSiYiSheng_2_model():

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # 打印最新的数据

    #测试案例 1
    # df1 = ts.pro_bar(ts_code='300151.SZ', start_date='20210630', end_date='20210729')
    # data7_1 = df1.iloc[0:24]  # 前4行
    # isAn_JiuSiYiSheng_2_model(data7_1,'300151.SZ')

    # 测试案例 2
    # df2 = ts.pro_bar(ts_code='600100.SH', start_date='20210603', end_date='20210803')
    # data7_2 = df2.iloc[0:24]  # 前4行
    # isAn_JiuSiYiSheng_2_model(data7_2, '600100.SH')

    # 测试案例 3
    df3 = ts.pro_bar(ts_code='688008.SH', start_date='20210403', end_date='20210513')
    data7_3 = df3.iloc[0:24]  # 前4行
    isAn_JiuSiYiSheng_2_model(data7_3, '688008.SH')


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
        # data6_1 = df.iloc[0:24]  # 前24行  # 必须 24 个数据
        # data6_1 = df.iloc[24:48]  # 前24行
        # data6_1 = df.iloc[24:70]  # 前24行
        data6_1 = df.iloc[46:72]  # 前24行
        # isAn_JiuSiYiSheng_2_model(data6_1, stock_code)

        len_1=len(data6_1)

        for i in range(0, len_1 - 24 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JiuSiYiSheng_2_model(data6_1[i:i + 24], stock_code)

if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_JiuSiYiSheng_2(localpath1)
    # test_isAn_JiuSiYiSheng_2_model()
    test_Befor_data()