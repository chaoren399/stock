#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
N型反转
https://www.yuque.com/chaoren399/byftms/rwe85y

1、出现在上涨初期或中期
2、由5根K线组成，第1根为大阳线
3、当中3根为小阴线，未吞没第一根阳线
4、最后一根为大阳线，吃掉3小阴跌幅
NXingFanZhuan

'''
chengongs=[]
modelname='N型反转'

def get_all_NXingFanZhuan(localpath1):
    info1=  '--N型反转 必须明显的有底部 start--   '
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
        isAn_NXingFanZhuan_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_NXingFanZhuan_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-5:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0

        # print1(data1)

        data2= data[len_data-5-1:len_data-5]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,


        # 设置两个 key
        key_1=0; #第一根是 大阳线
        key_2=0; # 3 个小阴线  最好是实体比较小
        key_3=0; #  当中3根为小阴线，未吞没第一根阳线
        key_4=0; # 第 4 根是大阳线, 收盘价高过 所有

        key_5=0; # 第 1 个阳线比前一天 放量
        key_6=0; # 3根小阴线逐渐缩量

        key_7=0; # 第一根是大阳线, 第 5 跟 也是大阳线



        count=0
        day1_yangxian_shiti=0
        day2_yinxian_shiti=0
        day3_yinxian_shiti=0
        day4_yinxian_shiti=0
        day5_yangxian_shiti=0
        day4_open=0
        day1_yangxian_amount=0
        day2_yinxian_amount=0
        day3_yinxian_amount=0
        day4_yinxian_amount=0
        day1_high=0
        day2_high=0
        day3_high=0
        day4_high=0
        day5_close=0

        day1_low=0
        day1_open=0
        day2_low=0
        day3_low=0
        day4_low=0

        for index, row in data1.iterrows():
            if(index==0 and isYangXian(row)==1): #阳线
                count=count+1
                day1_yangxian_shiti=getShiTiDaXiao(row)
                day1_yangxian_amount=row['amount']
                day1_low=row['low']
                zhisundian = day1_low
                day1_high = row['high']
                day1_open=row['open']
            if(index==1 and isYinXian(row)==1): #阴线
                count=count+1
                day2_yinxian_shiti=getShiTiDaXiao(row)
                day2_yinxian_amount = row['amount']
                day2_high = row['high']
                day2_low=row['low']

            if(index==2 and isYinXian(row)==1):#阴线
                count=count+1
                day3_yinxian_shiti = getShiTiDaXiao(row)
                day3_yinxian_amount = row['amount']
                day3_high = row['high']
                day3_low = row['low']
            if(index==3 and isYinXian(row)==1):#阴线
                count=count+1
                day4_yinxian_shiti = getShiTiDaXiao(row)
                day4_open=row['open']
                day4_yinxian_amount = row['amount']
                day4_high= row['high']
                day4_low = row['low']
            if(index==4 and isYangXian(row)==1): #阳线
                count=count+1
                mairuriqi=row['trade_date']
                day5_close= row['close']
                day5_yangxian_shiti = getShiTiDaXiao(row)

        if(count==5):
            if(day1_yangxian_shiti >1.6):
                key_1=1
            xiaoyinxian_biaozhun=3

            #   key_2=0; # 3 个小阴线  最好是实体比较小
            if(day2_yinxian_shiti < xiaoyinxian_biaozhun  and day3_yinxian_shiti < xiaoyinxian_biaozhun and day4_yinxian_shiti< xiaoyinxian_biaozhun):
                key_2=1
            # print1(day2_yinxian_shiti)
            # print1(day3_yinxian_shiti)
            # print1(day4_yinxian_shiti)
            # print1(day4_open)

            # key_3=0; #  当中3根为小阴线，未吞没第一根阳线
            # if( day1_open  < day2_low and  day1_open < day3_low and day1_open < day4_open ):
            #     key_3=1
            if( day1_low  < day2_low and  day1_low < day3_low and day1_low < day4_low ):
                key_3=1

            #key_4=0; # 第 5 根是大阳线, 收盘价高过 所有
            if(day5_close > day4_high and day5_close > day3_high and day5_close > day2_high and day5_close > day1_high):
                key_4=1


            #key_5=0; # 第 1 个阳线比前一天 放量

            day0_amount=data2.ix[0]['amount']
            if(day1_yangxian_amount > day0_amount ):
                key_5=1

            # key_6=0; # 3根小阴线逐渐缩量

            if(day1_yangxian_amount >day2_yinxian_amount and day2_yinxian_amount > day3_yinxian_amount and day3_yinxian_amount > day4_yinxian_amount ):
                key_6=1

            # key_7=0; # 第一根是大阳线, 第 5 跟 也是大阳线

            if(day1_yangxian_shiti > 3.4 and day5_yangxian_shiti > 3.4): #大阳线标准 3.5 以上
                key_7=1



        #
        if(0):
            print1(key_1)
            print1(key_2)
            print1(key_3)
            print1(key_4)
            print1(key_5)
            print1(key_7)
            print1(day1_yangxian_shiti)
            print1(day5_yangxian_shiti)

        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1 and key_7==1 ):
        # if(key_1==1 and  key_2 ==1 and key_5==1 and key_6==1):
            info = ''

            info = info + "-----N型反转 成功了 必须明显的有底部 "  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = 'N型反转.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            chengongs.append(chenggong_code)


'''
测试老师的案例

https://xueqiu.com/3476656801/206376910

'''
def test_isAn_NXingFanZhuan_laoshi():


    # 案例 1 垒知集团**002398.SZ
    df1 = ts.pro_bar(ts_code='002398.SZ',adj='qfq', start_date='20190407', end_date='20200407')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_NXingFanZhuan_model(data7_1,'002398.SZ')

    # 案例 2 002291 星期六
    df1 = ts.pro_bar(ts_code='002291.SZ',adj='qfq', start_date='20180407', end_date='20191213')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_NXingFanZhuan_model(data7_1,'002291.SZ')

    # 案例 3 603883
    df1 = ts.pro_bar(ts_code='603883.SH',adj='qfq', start_date='20180407', end_date='20190222')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_NXingFanZhuan_model(data7_1,'603883.SH')

    # 案例 4  002541
    df1 = ts.pro_bar(ts_code='002541.SZ',adj='qfq', start_date='20180407', end_date='20200713')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_NXingFanZhuan_model(data7_1,'002541.SZ')

    # 案例 5  纽威股份--强势股票**603699.SH
    df1 = ts.pro_bar(ts_code='603699.SH',adj='qfq', start_date='20180407', end_date='20200511')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_NXingFanZhuan_model(data7_1,'603699.SH')

    #

'''
测试自己的案例
'''
def test_isAn_NXingFanZhuan_ziji():
    #自己的 -----N型反转 成功了20210803--海欣食品**002702.SZ
    # df1 = ts.pro_bar(ts_code='600784.SH',adj='qfq', start_date='20210206', end_date='20211104')
    # data7_1 = df1.iloc[0:6]  # 前7行
    # isAn_NXingFanZhuan_model(data7_1,'600784.SH')

    #-----N型反转 成功了20210601--亚太药业**002370.SZ
    df1 = ts.pro_bar(ts_code='002370.SZ',adj='qfq', start_date='20180407', end_date='20210607')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_NXingFanZhuan_model(data7_1,'002370.SZ')

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
        data7_4 = df.iloc[22:42]  # 前10个交易日
        # data7_4 = df.iloc[22:22+30+10]  # 前10个交易日
        data7_4 = df.iloc[22:22+30+22]  # 前10个交易日
        data7_4 = df.iloc[22:22+30+120]  # 前10个交易日
        len_1=len(data7_4)
        for i in range(0, len_1 - 30 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_NXingFanZhuan_model(data7_4[i:i + 30], stock_code)

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
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_NXingFanZhuan(localpath1)
    # test_isAn_NXingFanZhuan_laoshi()
    # test_Befor_data()
    # test_isAn_NXingFanZhuan_ziji()

    endtime = time()
    print "总共运行时长:"+str(round((endtime - starttime) / 60 ,2))+"分钟"