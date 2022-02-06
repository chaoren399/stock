#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR
'''
双龙取水
思路: 判断 2 跟 k 线是不是满足 涨停板, 一个是放量, 另一个是缩量

原理: 庄家的空间洗盘

自己总结 
1-之前 有 跳空的要注意
2-横盘的不要
3- 放量不明显的不要

2021年09月01日 经过回测, 失败的概率很高 , 7月份 成功率只有 0.2

ShuangLongQushui

'''

infolists=[]
chengongs=[]
modelname='双龙取水 '

def get_all_ShuangLongQushui(localpath1):
    info1= "--双龙取水  start-- "
    writeLog_to_txt_nocode(info1)
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/xiadiecodes.csv'

    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})

    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        # df =  pd.read_csv(stockdata_path, dtype={'code': str})

        df = pd.read_csv(stockdata_path, index_col=0)
        # print df
        if (df.empty):
            continue


        data7_1 = df.iloc[0:2]  #
        # data7_1 = df.iloc[2:4]  #
        # data7_1 = df.iloc[3:5]  #
        # data7_1 = df.iloc[:5]  #

        isAn_ShuangLongQushui_model(data7_1, stock_code)




'''
判断 2 跟 k 线是不是满足 涨停板, 一个是放量, 另一个是缩量


               60  00 开头的 10%  30 68 开头的 20%
    
               
'''
def isAn_ShuangLongQushui_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if (len_data >= 3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1 = data[len_data - 3:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0

        # 设置两个 key
        key_1 = 0;  # 第一天放量
        key_2 = 0;  # 第2天缩量


        count=0
        day1_amount=0
        day2_amount=0
        day3_amount=0

        for index, row in data1.iterrows():
            if(index==0 ):
                day1_amount=row['amount']
            if(index==1 and isZhangTingBan(row)==1):
                day2_amount=row['amount']
                count=count+1
            if(index==2 and isZhangTingBan(row)==1):
                day3_amount=row['amount']
                count = count + 1
                mairuriqi= row['trade_date']
                zhisundian=row['low']

        if(count==2):
            if(day2_amount > day1_amount):
                key_1=1
            if(day3_amount < day2_amount): #缩量
                key_2=1

        if (key_1 == 1 and key_2 == 1 ):
            info =  "-- 双龙取水  --" + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '双龙取水.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
            chengongs.append(chenggong_code)



'''
测试老师的案例
'''
def test_isAn_ShuangLongQushui_laoshi():

    # 案例 1民丰特纸--强势股票**600235.SH
    df1 = ts.pro_bar(ts_code='600235.SH',adj='qfq', start_date='20180106', end_date='20181106')
    data7_1 = df1.iloc[0:24]  # 前7行
    isAn_ShuangLongQushui_model(data7_1,'600235.SH')

    # 案例 2 300809
    df1 = ts.pro_bar(ts_code='300809.SZ',adj='qfq', start_date='20200823', end_date='20210823')
    data7_1 = df1.iloc[0:24]  # 前7行
    isAn_ShuangLongQushui_model(data7_1,'300809.SZ')

    # 案例 3 002248
    df1 = ts.pro_bar(ts_code='002248.SZ', adj='qfq', start_date='20200823', end_date='20210823')
    data7_1 = df1.iloc[0:24]  # 前7行
    isAn_ShuangLongQushui_model(data7_1, '002248.SZ')

    # 案例 4 603260
    df1 = ts.pro_bar(ts_code='603260.SH',adj='qfq', start_date='20200823', end_date='20210823')
    data7_1 = df1.iloc[0:24]  # 前7行
    isAn_ShuangLongQushui_model(data7_1,'603260.SH')



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

        n=3
        data7_4 = df.iloc[23:56]  # 前10个交易日
        data7_4 = df.iloc[22:22+n+22]  # 前 1 个月
        len_1=len(data7_4)

        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ShuangLongQushui_model(data7_4[i:i + n], stock_code)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    # jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    jisuan_all_shouyilv(chengongs, modelname, 1.30)


if __name__ == '__main__':
    from time import *

    starttime = time()
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_ShuangLongQushui(localpath1)

    # test_isAn_ShuangLongQushui_laoshi()
    test_Befor_data()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"
