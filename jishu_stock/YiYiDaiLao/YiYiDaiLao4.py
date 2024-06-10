#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1, \
    writeLog_to_txt_path_getcodename, isYinXian
from jishu_stock.z_tool.getMin_Max import getMin_fromDataFrame
from stock.settings import BASE_DIR

import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
''''
以逸待劳4 主力洗盘模型 第 9天 阳线收盘价高过第 5 天收盘价
一份数据,多个方法 测试 2021年11月30日

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


这里为了严禁一些,  第 6 天收阳线, 比较确定一些, 宁可错杀 1000 不可选错一个.

6,7 ,8,9,10
'''
chengongs=[]
modelname='以逸待劳4'
def get_all_YiYiDaiLao(localpath1):
    info1=  '--以逸待劳4 完美符合模型, 第 9 天阳线收盘主力洗盘模型 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:26]  # 前6行
        # data6_1 = df.iloc[1:27]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_YiYiDaiLao_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 20 个数据是不是符合模型

需要 20 天数据
'''
def isAn_YiYiDaiLao_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    # print1(len_data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >11):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,




        data1_4 = data[len_data - 9:len_data]  # 测试 9天数据
        data1_4 = data1_4.reset_index(drop=True)  # 重新建立索引 ,



        data2_4 = data[len_data -9-5:len_data-9]
        data2_4 = data2_4.reset_index(drop=True)  # 重新建立索引 ,


        #4 模型 4

        YiYiDaiLao4(data1_4, data2_4, stockcode) #测试 9天数据,  第6,7,8 天 收盘价 都低于第 5 天收盘价,  # 第 89天 阳线收盘价高过第 5 天收盘价,




'''
测试 9天数据,  第6,7 ,8天 收盘价 都低于第 5 天收盘价,  
第 9 天 阳线收盘价高过第 5 天收盘价, 
'''
def YiYiDaiLao4(data1_1,data2,stockcode):
    riqi = data1_1.ix[0]['trade_date']  # 阳线的日期
    mairuriqi=0
    zhisundian=0
    # 设置两个 key
    key_1 = 0;  # 判断 1 个阳线 3 个阴线, 1 阳线  第 6 天的单独判断

    key_2 = 0;  # 阳线之后3连阴最高价依次降低最低价依次降低
    key_3 = 0;  # 是不是 从阳线开始成交量依次降低阳量>2>3>4
    key_4 = 0;  # 第 6 天是不是阳线,做为附加条件

    key_5 = 1  # 这是我自己加上去的, 就是第一个阳线要高于前 20 天的数据

    count = 0

    day2_high = 0
    day3_high = 0
    day4_high = 0

    day2_low = 0
    day3_low = 0
    day4_low = 0

    day1_close = 0
    day2_open = 0
    day3_open = 0
    day4_open = 0

    day5_close = 0
    day6_close=0
    day7_close=0
    day8_close=0
    day9_close=0
    day9_is_yangxian=0
    day1_amount = 0
    day2_amount = 0
    day3_amount = 0
    day4_amount = 0


    for index, row in data1_1.iterrows():
        if (index == 0 and isYangXian(row) == 1):  # 阳线
            count = count + 1
            day1_close = row['close']
            day1_amount = row['amount']
        if (index == 1 and isYinXian(row) == 1):  # 3 连阴线
            count = count + 1
            day2_open = row['open']
            day2_high = row['high']
            day2_low = row['low']
            day2_amount = row['amount']
        if (index == 2 and isYinXian(row) == 1):  # 3 连阴线
            count = count + 1
            day3_open = row['open']
            day3_high = row['high']
            day3_low = row['low']
            day3_amount = row['amount']
        if (index == 3 and isYinXian(row) == 1):  # 3 连阴线
            count = count + 1
            day4_open = row['open']
            day4_high = row['high']
            day4_low = row['low']
            day4_amount = row['amount']
        if (index == 4 and isYangXian(row) == 1):  # 阳线
            count = count + 1
            day5_close = row['close']
        if (index == 5 ):  # 第 6 天 无论阴线还是阳线, 收盘价 都比 第 5 天阳线开盘价 低
            day6_close = row['close']
        if (index == 6 ):  # 第 7天 无论阴线还是阳线, 收盘价 都比 第 5 天阳线开盘价 低
            day7_close = row['close']
        if (index == 7 ):  # 第 8天 无论阴线还是阳线, 收盘价 都比 第 5 天阳线开盘价 低
            day8_close = row['close']
        if (index == 8 ):  # 第 9天 阳线,收盘价 比第 5 天第 5 天阳线开盘价高
            day9_close = row['close']
            day9_is_yangxian=isYangXian(row)
            mairuriqi = row['trade_date']

    if (count == 5):
        key_1 = 1
    # 阳线之后3连阴最高价依次降低最低价依次降低
    if (day2_high > day3_high and day3_high > day4_high and day2_low > day3_low and day3_low > day4_low):
        # if (day2_open > day3_open and day3_open > day4_open):  # 为了限制一些比较杂的数据, 多加了这个条件
            key_2 = 1
    # 从阳线开始成交量依次降低阳量>2>3>4
    if (day1_amount > day2_amount and day2_amount > day3_amount and day3_amount > day4_amount):
        key_3 = 1
    if(day6_close <= day5_close and day7_close <= day5_close and day8_close <= day5_close and  day9_close > day5_close and  day9_is_yangxian==1):
        key_4=1
    # 就是第一个阳线要高于前 5 天的数据
    for index, row in data2.iterrows():
        if (day1_close < row['open']):
            key_5 = 0
    # print1(key_1)
    # print1(key_2)
    # print1(key_3)
    # print1(key_4)
    # print1(key_5)

    zhisundian = getMin_fromDataFrame(data1_1)['low']

    if (key_1 == 1 and key_2 == 1 and key_3 == 1  and key_4 == 1and key_5 == 1):
        info = ''

        info = info + "-----以逸待劳9天数据,主力洗盘 短期爆发 筑底后 缓慢上涨----" + str(riqi)
        # print info
        writeLog_to_txt(info, stockcode)
        path = '以逸待劳4.txt'
        writeLog_to_txt_path_getcodename(info, path, stockcode)

        chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
        chengongs.append(chenggong_code)






'''
测试老师的案例 6天数据案例
'''
def test_isAn_YiYiDaiLao_laoshi_6():

#案例 2,是符合 6 天的条件,
    # 案例2
    df1 = ts.pro_bar(ts_code='000005.SZ',adj='qfq', start_date='20210206', end_date='20210312') #世纪星源
    data7_1 = df1.iloc[0:26]  # 前7行
    isAn_YiYiDaiLao_model(data7_1,'000005.SZ')




'''
测试老师的案例 9天数据案例
'''
def test_isAn_YiYiDaiLao_laoshi_9():
    # 案例1   符合9 天 #广信材料 300537
    df1 = ts.pro_bar(ts_code='300537.SZ',adj='qfq', start_date='20210106', end_date='20210317')
    data7_1 = df1.iloc[0:26]  # 前7行
    isAn_YiYiDaiLao_model(data7_1,'300537.SZ')


    # 案例3 # 深纺织 A  000045
    df1 = ts.pro_bar(ts_code='000045.SZ',adj='qfq', start_date='20210106', end_date='20210201')
    data7_1 = df1.iloc[0:26]  # 前7行
    isAn_YiYiDaiLao_model(data7_1,'000045.SZ')


def test_ziji():
    #天奥电子 是不是符合以逸待劳
    df1 = ts.pro_bar(ts_code='002935.SZ',adj='qfq', start_date='20210106', end_date='20211123')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_YiYiDaiLao_model(data7_1,'002935.SZ')

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


        data7_4 = df.iloc[22:60]  # 前10个交易日
        # data7_4 = df.iloc[22:22 + 26 + 2]  # 前 1 个月
        data7_4 = df.iloc[22:22 + 26 + 22]  # 前 1 个月
        data7_4 = df.iloc[22:22 + 26 + 22+22]  # 前 2个月
        data7_4 = df.iloc[22:22 + 26 + 120]  # 半年
        len_1=len(data7_4)

        for i in range(0, len_1 - 26 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_YiYiDaiLao_model(data7_4[i:i + 26], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv

    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    jisuan_all_shouyilv(chengongs, modelname, 1.30)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'

    # test_isAn_YiYiDaiLao_laoshi_9()
    # test_isAn_YiYiDaiLao_laoshi_6()
    # get_all_YiYiDaiLao(localpath1)

    test_Befor_data()
    # test_ziji()