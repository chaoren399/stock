#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, getRiQi_Befor_Ater_Days, \
    isYangXian, writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.PyDateTool import get_date1_date2_days
from stock.settings import BASE_DIR

''''
否极泰来

https://www.yuque.com/chaoren399/eozlgk/wvq01u

熊市末期，长期下跌筑底，跌出一个低点，把该低点叫 A 点
低点之后反弹，不再创新低，然后横盘，这段时间叫 B
之后再次下探，再次形成一个低点，该低点叫 C，注意 C 点要比 A 点低
A 点与 C 点至少相隔 40 个交易日（即2个月以上）
C 点之后马上收阳线，称为 D 点，收盘价高于 A 的最低价
D 点后第二天买入，达到约30%的收益即可卖出
后面的 D 点不一定要求是熊市末期
最好 C 点最低点当天能收回来一根阳线，收盘价高于 A 最低价

长期下跌 我们确定为 1 年 , 250 个交易日 365 天

思路:  找到 最近大于 40 天的最低点, 然后从最低点找左边 20 个, 右边 20 , 两边都比他大,那么就是V 字型.

1. 先找到 C 点,是最近 40 天内的最低点才可以,  然后排除 C 点附近的 5 个点, 找 C-5 之后 的 3 个月数据, 找一个最低点A,
且最低点必须大于 C 点, 然后 A 与 C 之间的距离必须 大于 40 

2 . 判断 A 是不是 V 字型


增加 阳线的判断

'''

def get_all_PiJiTaiLai(localpath1):
    info1=  '--否极泰来高达97%胜率  start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:130]  # 前130行
        # data6_1 = df.iloc[1:131]  # 前6行

        len1 = len(data6_1)
        isAn_PiJiTaiLai_model(data6_1, stock_code)




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
        data1 = data[5:len_data]  # 阳线之前的数据
        data2=data[0:1] # 用来判断第一天是不是收阳
        data = data[1:30]
        # data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print1 (data)
        # print1 (data1)

        riqi = data.ix[0]['trade_date']  # 阳线的日期
        c_riqi=0

        # 设置两个 key
        key_1=1; # 找到 C 点 是不是最低点
        key_2=0; #  找 C-5 之后 的 3 个月数据, 找一个最低点A,最低点必须大于 C 点
        key_3=0; #  然后 A 与 C 之间的距离必须 大于 40
        key_4=1; # 判断 A 是不是 V 字型

        key_5=0; # 最好 C 点最低点当天能收回来一根阳线，收盘价高于 A 最低价

        key_6=0; # 第一天 是不是收阳线 单独判断, C 点之后马上收阳线，称为 D 点，收盘价高于 A 的最低价

        c_low_price= 0
        for index,row in data.iterrows():
            if(index==0):
                c_low_price = row['low']
                c_riqi=row['trade_date']
                riqi=row['trade_date']
                # print1(c_low_price)
                # print1(c_riqi)

                # 最好 C 点最低点当天能收回来一根阳线，收盘价高于 A 最低价
                if(isYangXian(row)==1):
                    key_5 =1
            else:
                low = row['low']
                if(c_low_price > low) : #如果 C 点不是最低的就终止循环
                    key_1=0
                    # print1(key_1)
                    return

         # 找 C-5 之后 的 3 个月数据, 找一个最低点A,

        if(key_1 ==1) :
            a_low_price=0
            a_riqi=0
            for index, row in data1.iterrows():
                if(index==0):
                    a_low_price=row['low']
                    a_riqi=row['trade_date']
                if(index > 0):
                    low1=row['low']
                    if(a_low_price > low1):
                        a_low_price= low1
                        a_riqi=row['trade_date']

            # print1(a_riqi)
            # print1(c_riqi)
            # print1(a_low_price)
            if(a_low_price > c_low_price): # 找一个最低点A,最低点必须大于 C 点
                key_2 =1

            days=get_date1_date2_days(a_riqi,c_riqi)
            if( days> 40): # A 与 C 之间的距离必须 大于 40
                key_3 =1

            if(key_3 ==1 and key_2==1):
                # 判断 A 是不是 V 字型
                #1 得到 a_riqi 之前的 10 个数据
                a_riqi_befor_10=getRiQi_Befor_Ater_Days(a_riqi,-1000)  #长期下跌 我们确定为 1 年 , 250 个交易日 365 天
                # print1(a_riqi_befor_10)
                # print1(a_riqi)
                #000004  10月 28 之前的数据就跑到了 9 月 28 , 数据不知道为什么没了, 所以增加到 前 50 天
                df1 = ts.pro_bar(ts_code=stockcode, adj='qfq', start_date=str(a_riqi_befor_10), end_date=str(a_riqi))
                # print1(df1)

                for index,  row in df1.iterrows():
                    if( a_low_price > row['low']):
                        key_4=0


                #2 得到 a_riqi 之后的 10 个数据
                a_riqi_after_10 = getRiQi_Befor_Ater_Days(a_riqi, 20)
                df2 = ts.pro_bar(ts_code=stockcode, adj='qfq', start_date=str(a_riqi), end_date=str(a_riqi_after_10))

                # print1(df2)
                for index,  row in df2.iterrows():
                    if( a_low_price > row['low']):
                        key_4=0
             # 第一天 是不是收阳线 单独判断, C 点之后马上收阳线，称为 D 点，收盘价高于 A 的最低价
            for index , row in data2.iterrows():
                if(index==0 and isYangXian(row)==1 and row['close']  > a_low_price):
                    key_6=1




        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(key_6)
        if(key_1==1 and  key_2 ==1  and key_3==1 and key_4==1):
            info = '-----'
            info1 = "---a与c天数:" + str(days)
            if(key_5==1):
                info='C点阳线'

                info = info + "-----否极泰来高达97%胜率 成功了 ----" +  ' --A 点:' + str(a_riqi) + ' ---C点:' + str(
                    c_riqi) + info1
                writeLog_to_txt(info, stockcode)

            elif(key_6==1):

                info = info + "-----否极泰来高达97%胜率 成功了" + ' ----' + stockcode + ' ---A 点:' + str(a_riqi) + ' ---C点:' + str(
                    c_riqi) + info1
                writeLog_to_txt(info, stockcode)
            path = '否极泰来.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例
'''
def test_isAn_PiJiTaiLai_laoshi():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例 1-000004.SZ ----20190131--国华网安

    df1 = ts.pro_bar(ts_code='000004.SZ',adj='qfq', start_date='20170206', end_date='20190201')
    data7_1 = df1.iloc[0:130]  # 前7行
    isAn_PiJiTaiLai_model(data7_1, '000004.SZ')
    # 案例 2 纽威股份603699
    df1 = ts.pro_bar(ts_code='603699.SH',adj='qfq', start_date='20170206', end_date='20181023')
    data7_1 = df1.iloc[0:130]  # 前7行
    # print data7_1
    isAn_PiJiTaiLai_model(data7_1,'603699.SH')


    # 案例 3: 美丽生态 000010，

    df1 = ts.pro_bar(ts_code='000010.SZ',adj='qfq', start_date='20170206', end_date='20190516')
    data7_1 = df1.iloc[0:130]  # 前7行
    isAn_PiJiTaiLai_model(data7_1, '000010.SZ')


    #C点阳线-----否极泰来高达97%胜率 成功了 ----603390.SH ---A 点:20210728 ---C点:20210930---a与c天数:64--通达电气
    df1 = ts.pro_bar(ts_code='603390.SH',adj='qfq', start_date='20170206', end_date='20210930')
    data7_1 = df1.iloc[0:130]  # 前7行
    isAn_PiJiTaiLai_model(data7_1, '603390.SH')
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


        data7_4 = df.iloc[0:130]  # 前10个交易日
        data7_4 = df.iloc[0:230]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 130 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_PiJiTaiLai_model(data7_4[i:i + 130], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_PiJiTaiLai(localpath1)
    # test_isAn_PiJiTaiLai_laoshi()
    # test_Befor_data()