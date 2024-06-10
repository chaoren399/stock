#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR

import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

'''

https://www.yuque.com/chaoren399/eozlgk/xkdffs
神龙摆尾 3

价格筑底后缓慢运行
第一个涨停板
第二日阳线放量且振幅5%以上
第三日小实体阳线缩量
第四日买入
以涨停板开盘价做止损


'''

chengongs=[]
modelname='神3'

def get_all_ShenLongBaiWei3(localpath1):
    info1=''
    writeLog_to_txt_nocode(info1) #为了 跟上边的盯盘的峰回路转, 反客为主 辨别
    info1= "神龙摆尾3价格筑底后缓慢运行,第一个涨停板   start "
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        if (1):

            stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
            # df =  pd.read_csv(stockdata_path, dtype={'code': str})
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                return
                # 1 得到 第一个 7 交易日数据
                # iloc只能用数字索引，不能用索引名
            data7_1 = df.iloc[0:3]  # 前10个交易日
            data7_1 = df.iloc[0:30]  # 前10个交易日

            # print data7_1
            # 2 单独一个函数 判断是不是符合  神龙摆尾
            isyes = isAnShenLongBaiwei3_model(data7_1, stock_code)

def isAnShenLongBaiwei3_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >=25):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-3:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = data1.ix[0]['trade_date']  # 阳线的日期

        data2 = data[len_data - 3-22:len_data-3]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # print data1
        # 设置两个 key
        key_1=0; #先判断是不是 涨停板
        key_2=0; # 第二日放量 且振幅 5% 以上
        key_3=0; # 第二日放量
        key_4=0; # 小实体阳线 缩量
        key_5=0; # 第 3 日必须是小实体阳线 的小实体

        key_6=1; # 前 20 个交易日 不能有涨停板



        #振幅公式：(当日最高点的价格-当日最低点的价格)/昨天收盘价×100%
        day1_close=0
        zhenfu=0
        day3_shiti=0
        zhisundian=0
        for index,row in data1.iterrows():
            if(index==0 and isZhangTingBan(row)==1): #涨停板
                key_1=1
                day1_close=row['close']
                day1_amount=row['vol']
                # day1_vol=row['vol']
                # print1(day1_close)
                zhisundian=row['open']
            if(index==1 and isYangXian(row) == 1 and key_1==1):

                day2_high=row['high']
                day2_low=row['low']
                zhenfu = ((day2_high - day2_low) / day1_close) * 100

                day2_amount = row['vol']
                if(day2_amount > day1_amount):
                    key_3 =1
                # print1(zhenfu)
            if(index==2 and isYangXian(row)==1  and key_3==1):
                day3_amount=row['vol']
                day3_shiti=getShiTiDaXiao(row)
                mairuriqi=row['trade_date']
                # print1(day3_amount)
                # print1(day2_amount)
                if(day3_amount< day2_amount): # 第 3 天 缩量
                    key_4=1



        if(zhenfu >= 4.9):
            key_2=1

        if(day3_shiti < 2): #判断 第 3日阳线是不是小实体
            key_5=1

        #key_6=0; # 前 20 个交易日 不能有涨停板
        for index,row in data2.iterrows():
            if(isZhangTingBan(row)==1):
                key_6=0


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(day3_shiti)
        if (key_1 == 1  and key_2==1and key_3==1 and key_4==1 and key_5==1 and key_6==1):
        # if (key_1 == 1  and key_2==1and key_3==1 and key_4==1 and key_5==1 ):
            info=''
            info=info+ 'day3_shiti='+str(day3_shiti)
            info = info+ "--------- 神3---------"   +  '--涨停板日期:'+ str(riqi)
            # print  info
            writeLog_to_txt(info, stockcode)
            path = '神3.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            chengongs.append(chenggong_code)

            return 1

    return 0;


'''
测试老师的案例
'''
def test_isAn_ShenLongBaiWei2_laoshi():

     # 案例 1
    df1 = ts.pro_bar(ts_code='603888.SH',adj='qfq', start_date='20210106', end_date='20210511')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAnShenLongBaiwei3_model(data7_1,'603888.SH')

    # 案例 2
    df1 = ts.pro_bar(ts_code='600088.SH',adj='qfq', start_date='20210106', end_date='20210324')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAnShenLongBaiwei3_model(data7_1,'600088.SH')

    #002389

    # 案例 3
    df1 = ts.pro_bar(ts_code='002389.SZ',adj='qfq', start_date='20210206', end_date='20210804')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAnShenLongBaiwei3_model(data7_1,'002389.SZ')

    # 案例 4茂硕电源 002660 大家当案例去观察
    df1 = ts.pro_bar(ts_code='002660.SZ',adj='qfq', start_date='20210206', end_date='20210605')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAnShenLongBaiwei3_model(data7_1,'002660.SZ')

'''
测试自己的案例
'''
def test_isAn_ShenLongBaiWei3_ziji():
    # 自己实战 案例 002900 悦心健康
    df1 = ts.pro_bar(ts_code='000796.SZ', adj='qfq', start_date='20210206', end_date='20220208')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAnShenLongBaiwei3_model(data7_1,'000796.SZ')





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



        data7_4 = df.iloc[22:22+25+22]  # 前1个个月
        # data7_4 = df.iloc[22:22+25+120]  # 半年
        # data7_4 = df.iloc[22:22+25+250]  # 前1年
        len_1=len(data7_4)

        for i in range(0, len_1 - 25 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAnShenLongBaiwei3_model(data7_4[i:i + 25], stock_code)


    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)

if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_ShenLongBaiWei3(localpath1)
    # test_isAn_ShenLongBaiWei2_laoshi()

    # test_Befor_data()
    test_isAn_ShenLongBaiWei3_ziji()



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"