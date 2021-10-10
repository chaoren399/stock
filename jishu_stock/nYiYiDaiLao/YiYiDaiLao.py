#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1
from stock.settings import BASE_DIR

''''
以逸待劳主力洗盘模型
https://www.yuque.com/chaoren399/eozlgk/dl33zz
思路: 找 6 天数据的,  第 6 天单独做判断

下跌筑底后缓慢上涨
阳线之后3连阴最高价依次降低最低价依次降低
从阳线开始成交量依次降低阳量>2>3>4

第5天收阳
之后某天(最好第6天)
阳线收盘价高过第5天阳线收盘价买入
以前低一止损价
短期爆发卖点参考亢龙有悔

'''

def get_all_YiYiDaiLao(localpath1):
    info1=  '--以逸待劳主力洗盘模型 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:26]  # 前6行
        data6_1 = df.iloc[1:27]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_YiYiDaiLao_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YiYiDaiLao_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    # print1(len_data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data > 6):

        # data1= data[7:len_data-1]  #  阳线之前的数据
        data1= data[6:len_data]  #  阳线之前的数据
        data = data[0:6]
        # print1(data1)
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data
        riqi = data.ix[0]['trade_date']  # 阳线的日期

        # 设置两个 key
        key_1=0;  #判断 1 个阳线 3 个阴线, 1 阳线  第 6 天的单独判断

        key_2=0; # 阳线之后3连阴最高价依次降低最低价依次降低
        key_3=0; #  是不是 从阳线开始成交量依次降低阳量>2>3>4
        key_4=0; # 第 6 天是不是阳线,做为附加条件

        key_5=1 # 这是我自己加上去的, 就是第一个阳线要高于前 20 天的数据

        count=0

        day2_high=0
        day3_high=0
        day4_high=0

        day2_low=0
        day3_low=0
        day4_low=0

        day1_close=0
        day2_open=0
        day3_open=0
        day4_open=0

        day5_open=0
        day6_open=0
        day1_amount=0
        day2_amount=0
        day3_amount=0
        day4_amount=0

        for index,row in data.iterrows():

            if(index==0 and isYangXian(row)==1): #阳线
                count= count+1
                day1_close=row['close']
                day1_amount=row['amount']

            if(index==1 and isYangXian(row)==0): # 3 连阴线
                count=count+1
                day2_open = row['open']
                day2_high=row['high']
                day2_low=row['low']

                day2_amount = row['amount']
            if(index==2 and isYangXian(row)==0): #3 连阴线
                count= count+1
                day3_open = row['open']
                day3_high = row['high']
                day3_low = row['low']
                day3_amount = row['amount']
            if(index==3 and isYangXian(row)==0): #3 连阴线
                count= count+1
                day4_open = row['open']
                day4_high = row['high']
                day4_low = row['low']
                day4_amount = row['amount']
            if(index==4and isYangXian(row)==1): #阳线
                count= count+1
                day5_open=row['open']

            if(index==5 and isYangXian(row)==1) : # 第 6 天阳线 附加条件
                day6_open=row['open']

        if(count==5):
            key_1=1

        # 阳线之后3连阴最高价依次降低最低价依次降低
        if(day2_high > day3_high and day3_high > day4_high  and day2_low> day3_low and day3_low > day4_low):
            if(day2_open > day3_open and day3_open > day4_open): # 为了限制一些比较杂的数据, 多加了这个条件

                key_2=1

        # 从阳线开始成交量依次降低阳量>2>3>4
        if(day1_amount > day2_amount and day2_amount > day3_amount and day3_amount > day4_amount):
            key_3 =1

        if(day6_open > day5_open):
            key_4=1

        data1
        #就是第一个阳线要高于前 20 天的数据
        for index, row in data1.iterrows():
           if(day1_close < row['open']):
               key_5=0


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_5)

        if(key_1==1 and  key_2 ==1  and key_3 ==1  and key_5==1):
            info=''
            if(key_4==1):
                info='明天可以买入'
                # info='----------'
            else:
                info='----------'
            info =info+ "-----以逸待劳主力洗盘模型  成功了" + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)




'''
测试老师的案例
'''
def test_isAn_YiYiDaiLao_laoshi():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例

    # df1 = ts.pro_bar(ts_code='300537.SZ',adj='qfq', start_date='20210106', end_date='20210312')#广信材料 300537
    # df1 = ts.pro_bar(ts_code='000005.SZ',adj='qfq', start_date='20210206', end_date='20210312') #世纪星源
    # df1 = ts.pro_bar(ts_code='000045.SZ',adj='qfq', start_date='20210106', end_date='20210127') # 深纺织 A  000045
    #自己的案例
    df1 = ts.pro_bar(ts_code='002172.SZ',adj='qfq', start_date='20210106', end_date='202108011') # 深纺织 A  000045

    # data7_1 = df1.iloc[0:6]  # 前7行
    data7_1 = df1.iloc[0:26]  # 前7行
    # print data7_1
    isAn_YiYiDaiLao_model(data7_1,'300537.SZ')

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


        data7_4 = df.iloc[22:60]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 26 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_YiYiDaiLao_model(data7_4[i:i + 26], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # test_get_5_13_34_RiJunXian_Pro3()
    # test_isAn_YiYiDaiLao_laoshi()
    get_all_YiYiDaiLao(localpath1)

    # test_Befor_data()