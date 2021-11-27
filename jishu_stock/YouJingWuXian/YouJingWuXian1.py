#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
有惊无险1
https://www.yuque.com/chaoren399/eozlgk/vehqag
筑底后缓慢.上涨  (这里没说是 第一天是不是阳线, 但是案例都是阳线, 所以我的程序也是阳线)
高开中/大阴线(高开低走)
有惊无险1 ①之后3天价格不能跌破阴线的最低价,第4天买入


有惊无2②3天内阳线收盘价超过洗盘阴线的开盘价


思路: 
找到 5 天数据 判断是还不是 高开低走,  中/大阴线,  
YouJingWuXian1

'''

def get_all_YouJingWuXian1(localpath1):
    info1=  '--有惊无险1 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:5]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_YouJingWuXian1_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YouJingWuXian1_model(data,stockcode):
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



        # 设置两个 key
        key_1=0; # 判断是不是 高开低走,
        key_2=0; # 中/大阴线,
        key_3=0 # 之后 3 天的最低价 不跌破 大阴线的最低价

        day1_close=0
        day2_open=0
        day2_yinxian_shiti=0
        day2_low=0
        day3_low=0
        count=0 # 用来判断 第一天阳线,第 2 天阴线的计数
        for index,row in data1.iterrows():
            if(index==0 and isYangXian(row)==1):
                day1_close=row['close']
                count = count+1
            if(index==1 and isYinXian(row)==1):
                count = count + 1
                day2_yinxian_shiti=getShiTiDaXiao(row)
                day2_open=row['open']
                if(day2_open > day1_close):# 判断是还不是 高开低走,
                    key_1=1
                day2_low=row['low']
            if(index==2):
                day3_low=row['low']
            if(index==3):
                day4_low=row['low']
            if(index==4):
                day5_low=row['low']



        if(day2_yinxian_shiti > 3.6 and count==2):#中/大阴线,
            key_2=1

        #之后 3 天的最低价 不跌破 大阴线的最低价

        if( day3_low > day2_low and day4_low> day2_low and day5_low > day2_low):
            key_3=1

        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        if(key_1==1 and  key_2 ==1 and key_3==1):
            info = ''
            info=info+'阴线大小='+str(day2_yinxian_shiti)
            info = info + "-----有惊无险1" + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '有惊无险1.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试老师的案例
'''
def test_isAn_YouJingWuXian1_laoshi():
    # 案例 1------有惊无险1 ----000420.SZ ----20210813--吉林化纤--强势股票
    df1 = ts.pro_bar(ts_code='000420.SZ',adj='qfq', start_date='20210206', end_date='20210819')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_YouJingWuXian1_model(data7_1,'000420.SZ')

    # 案例 2-----有惊无险1 ----600188.SH ----20210831--兖州煤业
    df1 = ts.pro_bar(ts_code='600188.SH',adj='qfq', start_date='20210206', end_date='20210906')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_YouJingWuXian1_model(data7_1,'600188.SH')

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_YouJingWuXian1_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_YouJingWuXian1_model(data7_1,'002507.SZ')

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
        for i in range(0, len_1 - 5 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_YouJingWuXian1_model(data7_4[i:i + 5], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_YouJingWuXian1(localpath1)
    # test_isAn_YouJingWuXian1_laoshi()
    test_Befor_data()