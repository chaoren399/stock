#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.aShengLv.huice.ShengLv_10_5 import jisuan_all_shouyilv_10_5
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''

见龙在田1 判断 3个 K 线 , 一阳一阴一阳
https://www.yuque.com/chaoren399/eozlgk/hrz8ri/


上涨结构
阳线后出现跳空高开的小阴线
第3天阳线收盘价高过模型所有实体
第四天买入

上涨初期 中阳线，后面高开小阴线，再加一个中阳线高过所有价，买入
小阴线成交量要小




跳空高开是指开盘价格高过昨日收盘价
JianLongZaiTian1

创建日期: 2021年11月06日
更新日期: 还没有测出好的结果, 目前只有 2 个案例,没有办法执行
'''
chengongs=[]
modelname='见龙在田'
def get_all_JianLongZaiTian1(localpath1):
    info1=  '--见龙在田 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_JianLongZaiTian1_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JianLongZaiTian1_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 13):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=False)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-3:len_data]
        data1 = data1.reset_index(drop=False)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)
        mairuriqi=0
        zhisundian=0

        data2 = data[len_data-18:len_data-3]
        data2 = data2.reset_index(drop=False)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #1后面跳空高开小阴线
        key_2=0;# 2小阴线 缩量
        key_3=0;# 3小阴线
        key_4=0; # 4再加一个中阳线高过所有价

        key_5=1; # 5 第一天阳线的最高价要搞过 近期所有收盘价和开盘价





        count = 0
        day1_close=0
        day1_high=0
        day2_close=0
        day1_amount=0
        day2_amount=0
        day2_open=0
        day3_close=0
        day1_yangxian_shitidaxiao=0
        day2_yinxian_shitidaxiao=0
        day2_yinxian_shangyingxian=0
        day2_yinxian_xiayingxian=0
        day2_low=0
        day2_high=0

        for index,row in data1.iterrows():
            if(index==0 and isYangXian(row)==1):
                count=count+1
                day1_close = row['close']
                day1_amount=row['amount']
                day1_high=row['high']
                day1_yangxian_shitidaxiao=getShiTiDaXiao(row)
            if(index==1 and isYinXian(row)==1):
                count=count+1
                day2_yinxian_shitidaxiao=getShiTiDaXiao(row)
                day2_close=row['close']
                day2_open=row['open']
                day2_high=row['high']
                day2_low=row['low']

                day2_amount = row['amount']
                zhisundian=day2_low

            if(index==2 and isYangXian(row)==1):
                count=count+1
                day3_close=row['close']
                mairuriqi=row['trade_date']

        if(count==3):

            # 1 后面跳空高开小阴线
            if(day2_close > day1_close and day2_open >day1_close):
                key_1 =1

            #2小阴线 缩量
            if(day2_amount < day1_amount ):
                key_2=1
            # 3小阴线
            if(day2_yinxian_shitidaxiao >0 and day2_yinxian_shitidaxiao < 2):
                key_3=1

            # 4再加一个中阳线高过所有价
            if(day3_close > day1_close and day3_close > day2_open):
                key_4=1

            yinxian_zhenfu = round(((day2_high - day2_low) / day1_close) * 100, 2)

            day2_yinxian_shangyingxian=day2_high-day2_open
            day2_yinxian_xiayingxian=day2_close-day2_low

            day2_yinxian_xiayingxian= day2_yinxian_xiayingxian + 0.00001
            day2_yinxian_beishu= day2_yinxian_shangyingxian/day2_yinxian_xiayingxian

            # 5 第一天阳线的最高价要搞过 近期所有收盘价和开盘价

            for index, row in data2.iterrows():
                if(day1_high < row['open']):
                    key_5=0
                    # print row
                if(day1_high < row['close']):
                    key_5=0

        #
        # if(stockcode=='002594.SZ'):
        if(0):

            print1(key_1)
            print1(key_2)
            print1(key_3)
            print1(key_4)
            print1(key_5)
            # print1(day1_high)
            # print1(data1)
            # print data2
        # print1(yinxian_zhenfu)



        # if(key_1==1 and key_2 ==1 and key_3 ==1 and key_4 ==1 and key_5==1):
        if(key_1==1  and key_3 ==1 and key_4 ==1 and key_5==1):
        # if( key_2 ==1 and key_3 ==1 and key_4 ==1):
            info = ''
            if(key_2==1):
                info = info + "--阴线缩量--"

            # info = info + "--阳线大小="  + str(day1_yangxian_shitidaxiao)
            # info = info + "--小阴线大小="  + str(day2_yinxian_shitidaxiao)
            # info = info + "--小阴线振幅="  + str(yinxian_zhenfu)
            # info = info + "--小阴线上下影线倍数="  + str(day2_yinxian_beishu)
            info = info + "--见龙在田1--"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '见龙在田1.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_JianLongZaiTian1_laoshi():
    # 案例 1 603799 华友钴业
    df1 = ts.pro_bar(ts_code='603799.SH',adj='qfq', start_date='20210206', end_date='20210707')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_JianLongZaiTian1_model(data7_1,'603799.SH')

    # 案例 2 000420
    df1 = ts.pro_bar(ts_code='000420.SZ',adj='qfq', start_date='20200206', end_date='20210205')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_JianLongZaiTian1_model(data7_1,'000420.SZ')

    # 案例 3比亚迪 1
    df1 = ts.pro_bar(ts_code='002594.SZ',adj='qfq', start_date='20200206', end_date='20210608')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_JianLongZaiTian1_model(data7_1,'002594.SZ')





'''
测试自己的案例
'''
def test_isAn_JianLongZaiTian1_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='000635.SZ',adj='qfq', start_date='20210206', end_date='20211202')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_JianLongZaiTian1_model(data7_1,'000635.SZ')

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
        data7_4 = df.iloc[22:22+30+22]  # 1 月
        # data7_4 = df.iloc[22:22+30+120]  # 半年
        # data7_4 = df.iloc[22:22+30+250]  # 1 年
        len_1=len(data7_4)
        for i in range(0, len_1 - 30 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JianLongZaiTian1_model(data7_4[i:i + 30], stock_code)

    # jisuan_all_shouyilv(chengongs, modelname, 1.03)
    # jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    # jisuan_all_shouyilv(chengongs, modelname, 1.15)

    jisuan_all_shouyilv_10_5(chengongs, modelname, 1.10, 0.95)
    jisuan_all_shouyilv_10_5(chengongs, modelname, 1.05, 0.95)


if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_JianLongZaiTian1(localpath1)
    # test_isAn_JianLongZaiTian1_laoshi()
    test_Befor_data()
    # test_isAn_JianLongZaiTian1_ziji()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"