#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1
from stock.settings import BASE_DIR

''''
熊市末期亢龙有悔 个股上的应用: 

https://www.yuque.com/chaoren399/eozlgk/qrbx7l

熊市末期的时候, 比较好用,

连续 3 天以上阴线 , 跳空低开(不一定是缺口) 

思路:  

1. 找到 4 个数据, for 循环 先判断  是不是 3 个阴, 1 个阳
2. 判断是不是有跳空 for循环 
3. 是不是 亢龙有悔的阳线
4. 阳线的最低价是不是近期 2 个月的最小值?


'''

def get_all_KangLongYouHuiXiongShiMoQi(localpath1):
    info1=  '--熊市末期,亢龙有悔 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:4]  # 前6行
        data6_2 = df.iloc[4:48]  # 2 个月的数据必须是下跌的
        # data6_1 = df.iloc[2:6]  # 前6行
        # data6_2 = df.iloc[6:50]  # 2 个月的数据必须是下跌的

        isAn_KangLongYouHuiXiongShiMoQi_model(data6_1,data6_2, stock_code)


'''
#2 单独一个函数 判断 4 个数据是不是符合模型
'''
def isAn_KangLongYouHuiXiongShiMoQi_model(data,data2,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data ==4):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data

        # 设置两个 key
        key_1=0; #先判断是不是 3 个阴一个阳
        key_2=0; # 判断 是不是 跳空低开(不一定是缺口)
        key_3=0; # 判断 最后一个阳线是不是  低开高收的阳线
        key_4=0; # 大趋势必须是下跌

        riqi=data.ix[len_data-1]['trade_date']


        #1 先判断是不是 3 个阴一个阳
        count=0
        for index, row in data.iterrows():
            if(index==0 and isYangXian(row)==0):
                count=count+1
            if(index==1 and isYangXian(row)==0):
                count=count+1
            if(index==2 and isYangXian(row)==0):
                count=count+1
            if(index==3 and isYangXian(row)==1):
                count=count+1
        if(count==4):
            key_1=1
        else:return

        #2 判断 是不是 跳空低开(不一定是缺口)

        day1_close=data.ix[0]['close']
        day2_open = data.ix[1]['open']
        day2_close = data.ix[1]['close']
        day3_open = data.ix[2]['open']

        if(day1_close> day2_open or  day2_close > day3_open):
            key_2=1

        #3 判断 最后一个阳线是不是  低开高收的阳线

        day3_close = data.ix[2]['close']
        day4_open= data.ix[3]['open']
        day4_close= data.ix[3]['close']

        if( day4_open <day3_close and day4_close > day3_close):
            key_3=1

        #4 大趋势必须是下跌
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,
        # print data2

        data2_min_open= data2.ix[0]['open']
        riqi1=None
        for index, row in data2.iterrows():
            a_open= row['open']
            if(a_open< data2_min_open):
                data2_min_open = a_open
                riqi1=row['trade_date']

        # print1(riqi1)
        # print1(stockcode)


        if(data2_min_open > data.ix[3]['open']):
            key_4=1

        # print1(key_1)
        # print1(key_2)
        # print1(key_3)


        if(key_1==1 and key_2==1 and key_3==1 and key_4==1):
            info = "-----熊市末期,亢龙有悔  成功了" + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)




'''
测试案例
'''
def test_isAn_KangLongYouHuiXiongShiMoQi_model():

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # 打印最新的数据

    # df1 = ts.pro_bar(ts_code='000066.SZ', start_date='20210430', end_date='20210510')
    # df2 = ts.pro_bar(ts_code='000066.SZ', start_date='20210230', end_date='20210429')
    df1 = ts.pro_bar(ts_code='300136.SZ', start_date='20210506', end_date='20210511')
    df2 = ts.pro_bar(ts_code='300136.SZ', start_date='20210306', end_date='20210506')


    data7_1 = df1.iloc[0:4]  # 前7行
    data7_2 = df2.iloc[0:48]  # 2 个月的数据必须是下跌的
    # print data7_2
    isAn_KangLongYouHuiXiongShiMoQi_model(data7_1,data7_2,'300136.SZ')


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
        # data = df.iloc[22:90]#  满足 大于 48
        data = df.iloc[44:112]#  满足 大于 48

        len_1=len(data)

        for i in range(0, len_1 - 48 + 1):
            # print "i" + str(i )+ "j"+str(i+3)

            data1= data.iloc[i:i+4]
            data2= data.iloc[i+4:i+48]
            isAn_KangLongYouHuiXiongShiMoQi_model(data1,data2, stock_code)






if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # test_isAn_KangLongYouHuiXiongShiMoQi_model()
    # get_all_KangLongYouHuiXiongShiMoQi(localpath1)
    test_Befor_data()