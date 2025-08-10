#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''


想法来源: 


涨停板后 放巨量的大阴险+ 然后反包 的票（可以不涨停）


ZTB_JuLiangYinXian_ZTB

'''
chengongs=[]
modelname='涨停后放巨量的大阴险'



def get_all_ZTB_JuLiangYinXian_ZTB(localpath1):
    info1=  '-- start-- 涨停板后 放巨量的大阴险+ 然后反包 的票（可以不涨停）  '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ZTB_JuLiangYinXian_ZTB_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ZTB_JuLiangYinXian_ZTB_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        data2= data[len_data-2-1:len_data-2]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #1-昨天 是一个涨停板, 今天来了一个跳空高开的大阴线

        key_2=0; # 2阴线


        key_4=0; #阴线放量
        key_5=0;#阴线收盘价 < 上个涨停板价格



        count=0
        day0_close=0
        day1_close=0
        day2_open=0
        day2_close=0
        day0_amount=0
        day1_amount=0
        day2_amount=0

        for index,row in data1.iterrows():


            if(index==0 and isZhangTingBan(row)==1):

                day0_amount=row['amount']
                day0_close=row['close']
                key_1=1

            if(index==1 and isYinXian(row)==1):
                day1_amount=row['amount']
                day1_close=row['close']
                key_2=1
                mairuriqi = row['trade_date']

        if(day0_amount < day1_amount):
            key_4=1
        if(day0_close > day1_close):
            key_5=1

        if(key_1==1 and key_2==1  and key_4==1and key_5==1):
        # if(key_1==1 and key_2==1):
            info = ''

            info = info + "--涨停后放巨量的大阴险 成功了"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = modelname+'.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            # print1(day2_shizixing_low)
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_ZTB_ZTB_TiaoKong_laoshi():
    # 案例 1
    df1 = ts.pro_bar(ts_code='000408.SZ',adj='qfq', start_date='20210206', end_date='20210518')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_ZTB_JuLiangYinXian_ZTB_model(data7_1,'002174.SZ')

    # 案例 2

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_ZTB_ZTB_TiaoKong_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_ZTB_JuLiangYinXian_ZTB_model(data7_1,'002507.SZ')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        n=3


        data7_4 = df.iloc[22:22+n+22]  #1 个月
        # data7_4 = df.iloc[22:22+n+120]  # 半年
        # data7_4 = df.iloc[22:22+132+250]  # 1年

        len_1=len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ZTB_JuLiangYinXian_ZTB_model(data7_4[i:i + n], stock_code)




if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_ZTB_ZTB_TiaoKong(localpath1)
    # get_all_ZTB_JuLiangYinXian_ZTB(localpath1)
    test_Befor_data()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"