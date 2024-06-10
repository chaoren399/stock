#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, \
    writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan


import pandas as pd

# 显示所有列
from stock.settings import BASE_DIR

pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
峰回路转 -超短线 3 天涨停


https://www.yuque.com/chaoren399/eozlgk/cgc8qt

第1天上涨结构 放量涨停
第2天下跌(收盘价低于涨停板收盘价)且缩量
第3天盘中高过涨停板的收盘价挂单买入
以第1天开盘作为止损

卖出点参考飞龙在天


'''

infolists=[]
chengongs=[]
modelname='峰回路转'
def get_all_FengHuiLuZhuan(localpath1):
    info1=  '--峰回路转 -超短线 3 天涨停 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:24]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_FengHuiLuZhuan_model(data6_1, stock_code)

    return infolists


'''
#2 单独一个函数 判断 6 个数据是不是符合模型  24行
'''
def isAn_FengHuiLuZhuan_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 24):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1=data[len_data-3:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,


        data2= data[len_data-2-22:len_data-2]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,
        # print1(data2)
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi=0
        zhisundian=0

        # 设置两个 key
        key_1=0; # 涨停板 并且 放量
        key_2=0;#第2天下跌(收盘价低于涨停板收盘价)且缩量

        key_3=1; # 判断上涨结构  涨停板的收盘价 高于 前 1 个月的 最高价

        day1_amount=0
        day2_amount=0
        day3_amount=0
        day2_close=0
        day3_close=0
        # print1(data1)

        for index,row in data1.iterrows():
            if(index==0):
                day1_amount=row['amount']
            if(index==1 and isZhangTingBan(row)==1):
                day2_amount=row['amount']
                day2_close=row['close']
                zhisundian=row['open']
                riqi=row['trade_date']
                if(day2_amount > day1_amount):
                    key_1=1
            if(index==2):
            #第二天阴线阳线都行，要求其收盘价低于涨停板收盘价，并且比前一天缩量；
                day3_close=row['close']
                day3_amount=row['amount']
                mairuriqi = row['trade_date']
                if(day3_close < day2_close and day3_amount < day2_amount) :
                    key_2=1


        # 判断上涨结构  涨停板的收盘价 高于 前 1 个月的 最高价
        # day2_close
        for index, row in data2.iterrows():
            if(row['high'] > day2_close):
                key_3=0

        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        if(key_1==1 and  key_2 ==1 and key_3==1):
            info = "峰回路转第3天用软件条件挂单,挂涨停板的收盘价-- "  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '峰回路转.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            chengongs.append(chenggong_code)



'''
测试老师的案例
'''
def test_isAn_FengHuiLuZhuan_laoshi():

    # 案例 1

    df1 = ts.pro_bar(ts_code='000400.SZ',adj='qfq', start_date='20190206', end_date='20200228')

    data7_1 = df1.iloc[0:24]  # 前7行
    # print data7_1
    isAn_FengHuiLuZhuan_model(data7_1,'000400.SZ')

'''
测试自己的案例
'''
def test_isAn_FengHuiLuZhuan_ziji():


    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:24]  # 前7行
    isAn_FengHuiLuZhuan_model(data7_1,'002507.SZ')

def test_xueyuan_anli():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='000929.SZ',adj='qfq', start_date='20210206', end_date='20211020')
    data7_1 = df1.iloc[0:24]  # 前7行
    print1(data7_1)
    isAn_FengHuiLuZhuan_model(data7_1,'000929.SZ')



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


        data7_4 = df.iloc[23:56]  # 前10个交易日
        data7_4 = df.iloc[22:22+24+22]  # 前 1 个月
        len_1=len(data7_4)

        for i in range(0, len_1 - 24 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_FengHuiLuZhuan_model(data7_4[i:i + 24], stock_code)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    jisuan_all_shouyilv(chengongs, modelname, 1.30)

if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_FengHuiLuZhuan(localpath1)
    # test_isAn_FengHuiLuZhuan_laoshi()
    test_Befor_data()
    # test_xueyuan_anli()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"