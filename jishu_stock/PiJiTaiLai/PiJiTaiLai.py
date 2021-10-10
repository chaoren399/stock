#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode,print1
from stock.settings import BASE_DIR

''''
否极泰来

https://www.yuque.com/chaoren399/eozlgk/wvq01u

思路:  找到 最近大于 40 天的最低点, 然后从最低点找左边 20 个, 右边 20 , 两边都比他大,那么就是V 字型.

1. 先找到 C 点,是最近 40 天内的最低点才可以,  然后排除 C 点附近的 5 个点, 找 C-5 之后 的 3 个月数据, 找一个最低点A,
且最低点必须大于 C 点, 然后 A 与 C 之间的距离必须 大于 40 

2 . 判断 A 是不是 V 字型



'''

def get_all_PiJiTaiLai(localpath1):
    info1=  '--否极泰来高达97%胜率  start--   '
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

            isAn_PiJiTaiLai_model(dataframe_df[i:i + 3], stockcode)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_PiJiTaiLai_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data1 = data[30:len_data]  # 阳线之前的数据
        data = data[0:30]
        # data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        # data = data.reset_index(drop=True)  # 重新建立索引 ,
        print1 (data)

        riqi = data.ix[3]['trade_date']  # 阳线的日期

        # 设置两个 key
        key_1=1; # 找到 C 点 是不是最低点
        key_2=0; #  找 C-5 之后 的 3 个月数据, 找一个最低点A,
        key_3=0; # 且最低点必须大于 C 点, 然后 A 与 C 之间的距离必须 大于 40
        key_4=0; # 判断 A 是不是 V 字型

        c_low_price= 0
        for index,row in data.iterrows():
            if(index==0):
                c_low_price = row['low']
                print1(c_low_price)
            else:
                low = row['low']
                if(c_low_price > low) : #如果 C 点不是最低的就终止循环
                    key_1=0
                    print1(key_1)
                    return

         # 找 C-5 之后 的 3 个月数据, 找一个最低点A,

        if(key_1 ==1) :
            tmp_low=0
            a_riqi=0
            for index, row in data.iterrows():
                if(index==5):
                    tmp_low=row['low']
                if(index > 5):
                    low1=row['low']
                    if(tmp_low < low1):
                        tmp_low= low1
                        a_riqi=row['trade_date']

            print1(a_riqi)
            print1(tmp_low)


        print1(key_1)
        print1(key_2)
        if(key_1==1 and  key_2 ==1):
            info = "-----否极泰来高达97%胜率 成功了" + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)




'''
测试老师的案例
'''
def test_isAn_PiJiTaiLai_laoshi():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例 1

    df1 = ts.pro_bar(ts_code='000004.SZ',adj='qfq', start_date='20170206', end_date='20190131')

    data7_1 = df1.iloc[0:30]  # 前7行
    data7_1 = df1.iloc[0:130]  # 前7行
    # print data7_1
    isAn_PiJiTaiLai_model(data7_1,'000004.SZ')

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

        for i in range(0, len_1 - 20 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ShenLongBaiwei4_model_pro(data7_4[i:i + 20], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # test_get_5_13_34_RiJunXian_Pro3()
    # get_all_LingBoWeiBu(localpath1)
    test_isAn_PiJiTaiLai_laoshi()