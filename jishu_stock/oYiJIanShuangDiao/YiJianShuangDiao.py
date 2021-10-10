#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1
from stock.settings import BASE_DIR

''''
一箭双雕 主力中继洗盘模型  正课

https://www.yuque.com/chaoren399/eozlgk/xwhd4i



上涨结构初期或中期
第1天中阳线或大阳线后
第2、3天连续两个小实体阴线
阴线不能跌破阳线实体
第4天收阳线阳线收盘价高过前3天的所有实体上沿
以全部4天的最低价做止损
两个小阴线最好高开

思路 1

1. 先判断4 天数据是不是阳 阴 阴 阳 

2. 判断 第 4 天收盘价是不是高过前 3 天

3 . 2 个阴线不能跌破第一天的阳线实体.

4 . 两个小阴线最好高开
'''

def get_all_YiJianShuangDiao(localpath1):
    info1=  '--一箭双雕 主力中继洗盘模型 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:4]  # 前6行
        data6_1 = df.iloc[0:14]  # 前6行
        # data6_1 = df.iloc[3:17]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_YiJianShuangDiao_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YiJianShuangDiao_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    # print1(len_data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >=14):
        data1= data[4:len_data]
        data=data[0:4]
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,


        # print data
        riqi = data.ix[0]['trade_date']  # 阳线的日期

        # 设置两个 key
        key_1=0; #先判断4 天数据是不是阳 阴 阴 阳
        key_2=0;#判断 第 4 天收盘价是不是高过前 3 天
        key_3=0; #2 个阴线不能跌破第一天的阳线实体.
        key_4=0; # 两个小阴线最好高开

        key_5=0; # 中阳线的涨幅 大于 3%
        key_6=1; #  第一天阳线的收盘价 要高过之前 10 天的 数据, 这样是上涨行情



        count =0
        day1_close=0
        day1_open=0
        day1_pct_chg=0
        day2_open=0
        day2_close=0
        day3_open = 0
        day3_close=0
        day4_close=0
        for index,row in data.iterrows():
            # print1(count)
            if(index==0 and isYangXian(row)==1):
                count=count+1

                day1_open=row['open']
                day1_close=row['close']
                day1_pct_chg=row['pct_chg']
            if(index==1 and isYangXian(row)==0):
                count=count+1
                day2_open=row['open']
                day2_close=row['close']
            if(index==2 and isYangXian(row)==0):
                count=count+1
                day3_open = row['open']
                day3_close=row['close']
            if(index==3 and isYangXian(row)==1):
                count=count+1
                day4_close = row['close']
        if(count==4):
            key_1=1
        if(key_1==1):

            #判断 第 4 天收盘价是不是高过前 3 天
            if(day4_close > day3_open and day4_close> day2_open and day4_close > day1_close):
                key_2=1

            # 3, 2 个阴线不能跌破第一天的阳线实体.

            if(day3_close > day1_open  and day2_close > day1_open):
                # print1(day3_close)
                key_3=1
            if(day1_pct_chg > 3): #中阳线的涨幅 大于 3%
                # print1(day1_pct_chg)
                key_5=1

             # key_6 = 0;  第一天阳线的收盘价 要高过之前 10 天的 数据, 这样是上涨行情
            # print data1

            for index,row in data1.iterrows():
                if(day1_close < row['close'] or day1_close < row['open']):
                    key_6=0


        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_5)
        # print1(key_6)



        if(key_1==1 and  key_2 ==1  and key_3==1 and key_5==1 and key_6==1):
            info = "-----一箭双雕 主力中继洗盘模型  成功了" + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)




'''
测试老师的案例
'''
def test_isAn_YiJianShuangDiao_laoshi():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例 1

    # df1 = ts.pro_bar(ts_code='000150.SZ',adj='qfq', start_date='20210206', end_date='20210421')
    # df1 = ts.pro_bar(ts_code='000928.SZ',adj='qfq', start_date='20210206', end_date='20210429')
    # df1 = ts.pro_bar(ts_code='002466.SZ',adj='qfq', start_date='20200206', end_date='20210107')
    df1 = ts.pro_bar(ts_code='002229.SZ',adj='qfq', start_date='20200206', end_date='20210416')

    data7_1 = df1.iloc[0:14]  # 前4行
    # print data7_1
    isAn_YiJianShuangDiao_model(data7_1,'000150.SZ')


'''
测试我自己的
'''
def test_isAn_YiJianShuangDiao_ziji():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例 1-----一箭双雕 主力中继洗盘模型  成功了 ----000423.SZ ----20210930--东阿阿胶

    # df1 = ts.pro_bar(ts_code='000423.SZ',adj='qfq', start_date='20210206', end_date='20210930')
    #-----一箭双雕 主力中继洗盘模型  成功了 ----000159.SZ ----20210810--国际实业
    # df1 = ts.pro_bar(ts_code='000159.SZ',adj='qfq', start_date='20210206', end_date='20210814')
    #-----一箭双雕 主力中继洗盘模型  成功了 ----000989.SZ ----20210816--九芝堂
    # df1 = ts.pro_bar(ts_code='000989.SZ',adj='qfq', start_date='20210206', end_date='20210819')

    #-----一箭双雕 主力中继洗盘模型  成功了 ----603416.SH ----20210810--信捷电气
    df1 = ts.pro_bar(ts_code='603416.SH',adj='qfq', start_date='20210206', end_date='20210813')


    data7_1 = df1.iloc[0:14]  # 前4行
    print data7_1
    isAn_YiJianShuangDiao_model(data7_1,'603416.SH')

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


        data7_4 = df.iloc[22:52]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 14 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_YiJianShuangDiao_model(data7_4[i:i + 14], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'

    # test_isAn_YiJianShuangDiao_laoshi()
    get_all_YiJianShuangDiao(localpath1)
    # test_isAn_YiJianShuangDiao_ziji()
    # test_Befor_data()