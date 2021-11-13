#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian, is_big_to_small, \
    writeLog_to_txt_path_getcodename, isYinXian
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from stock.settings import BASE_DIR

import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
反客为主Plus  强庄主力仅用一天的强势洗盘

https://www.yuque.com/chaoren399/eozlgk/ysft12/

首先已经是底底抬高、顶顶抬高的上涨结构，是个追涨模型，强庄主力仅用一天的强势洗盘。

反客为主Plus
上涨结构突然出现中/大阴线
跌幅4%以.上或振幅5%以上
次日高开高收大阳线/涨停板
涨幅5%以.上
以模型最低价作为止损价

反客为主前必定是阳线, 因为是突然出现



一般可这样区分：
 小阴线和小阳线的波动范围一般在0.6--1.5%；
 中阴线和中阳线的波动范围一般在1.6-3.5%；
 大阴线和大阳线的波动范围在3.6%以上。
 
 
涨 3 个月以内的最好
宁可错杀一千,不可选错一个

胜率 80%


'''

def get_all_FanKeWeiZhu_Plus(localpath1):
    info1=  '--反客为主Plus找刚起来不超过3个月的 强庄主力仅用一天的强势洗盘 --   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        data6_1 = df.iloc[0:3]  # 前6行
        # data6_1 = df.iloc[1:3]  # 前6行
        # data6_1 = df.iloc[3:5]  # 前6行
        isAn_FanKeWeiZhu_Plus_model(data6_1, stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_FanKeWeiZhu_Plus_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,



        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        data0= data[len_data-3:len_data-2]
        data0 = data0.reset_index(drop=True)  # 重新建立索引 ,
        # print1(data0)

        # 设置两个 key
        key_1=0; # 先判断 阴阳
        key_2=0; # 是不是高开高走的大阳线
        key_3=0;  #阴线 跌幅 4% 以上或者 振幅 5%以上
        key_4=0; # 阳线涨幅 5% 以上

        key_5=0; #  10 周,60 周均线是不是向上
        key_6=0; # 反客为主前必定是阳线, 因为是突然出现





        day0_close=0
        day1_open=0
        day1_close=0
        day1_high=0
        day1_low=0
        day2_open=0
        day2_close=0
        count1=0

        yinxian_pct_chg=0
        yangxian_pct_chg=0
        yangxian_daxiao=0
        for index, row in data1.iterrows():
            if(index==0 and isYinXian(row) ==1):
                count1=count1+1
                day1_open=row['open']
                day1_close=row['close']
                # chazhi1 = format(((row['close'] - row['open']) / row['open']) * 100 ,'.2f') # (开盘价-收盘价)÷开盘价＜0.5%
                # day1_yinxian_zhangfu=row[]
                yinxian_pct_chg= round(row['pct_chg'],2)
                day1_high=row['high']
                day1_low=row['low']
            if(index==1 and isYangXian(row)==1):
                count1 = count1 + 1
                day2_open = row['open']
                day2_close = row['close']

                yangxian_pct_chg=row['pct_chg']
                yangxian_daxiao=getShiTiDaXiao(row)
        # format(float(a) / float(b), '.2f'))
        if(count1==2):
            key_1=1
            # 阳线开盘价大于阴线收盘价  阳线收盘价高于阴线开盘价
            if(day2_open > day1_close and day2_close > day1_open):
                key_2=1
            # 阴线 跌幅 4% 以上或者振幅5%以上
            # zhenfu = ((day2_high - day2_low) / day1_close) * 100

            for index,row in data0.iterrows():
                if(index==0):
                    day0_close=row['close']
                    if( isYangXian(row)==1):
                        key_6=1
            yinxian_zhenfu =  round (((day1_high - day1_low) / day0_close) * 100,2)
            if(yinxian_pct_chg < -4 or yinxian_zhenfu > 5): #阴线 跌幅 4% 以上或者振幅5%以上
            # if(yinxian_pct_chg < -4 and  yinxian_zhenfu > 5): #阴线 跌幅 4% 以上或者振幅5%以上
                key_3=1



             # 阳线涨幅 5% 以上
            if(yangxian_pct_chg >5) :
                key_4=1


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_6)
        # print1(yangxian_pct_chg)
        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_6==1):
            # 10 周均线是不是向上

            if(is10_60Week_XiangShang(stockcode, riqi) ==2):
               key_5=1


            if(key_5==1):
            # if(1):
                    info =''
                    info=info+'--阴线涨幅='+str(yinxian_pct_chg)
                    info=info+'--阴线振幅='+str(yinxian_zhenfu)
                    info=info+'--阳线涨幅='+str(yangxian_pct_chg)
                    info=info+'--阳线大小='+str(yangxian_daxiao)
                    if(key_5==1):
                        info=info+"10-60周向上"
                    else:
                        info = info + "1060周不满足"

                    info =info + "-----反客为主Plus 强庄主力仅用一天的强势洗盘 ----" + str(riqi)
                    # print info
                    writeLog_to_txt(info, stockcode)

                    path = '反客为主Plus.txt'
                    # writeLog_to_txt_path_getcodename(info, path, stockcode)

#10 周均线是不是向上
def is10_60Week_XiangShang(stock_code, riqi):
    df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20190101', end_date=str(riqi))

    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    # print df
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行

    # print df
    df_week = df

    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    df_week['Week10-60'] = df_week['WeekMa10'] - df_week['WeekMa60']  # G8 买 2 用到

    df_week = df_week.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print  df_week[0:10]
    df_week = df_week[0:2]  # 一年有 48 周 ,2 周是向上的就可以
    # df_week = df_week[0:24]  # 一年有 48 周
    WeekMa10 = []
    WeekMa60 = []
    for index, row in df_week.iterrows():
        WeekMa10.append(row['WeekMa10'])
        WeekMa60.append(row['WeekMa60'])
    # print1(WeekMa10)
    # print1(WeekMa60)
    count=0
    if (is_big_to_small(WeekMa10) == 1):
        count=count+1

    if (is_big_to_small(WeekMa60) == 1):
        count = count + 1


    return count



'''
测试老师的案例 10月份的案例
'''
def test_isAn_FanKeWeiZhu_Plus_laoshi_10yue():

    # 案例 1 道森股份**603800.SH
    df1 = ts.pro_bar(ts_code='603800.SH',adj='qfq', start_date='20210206', end_date='20210729')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1,'603800.SH')

    # 案例 2 中国巨石 600176

    df1 = ts.pro_bar(ts_code='600176.SH',adj='qfq', start_date='20210206', end_date='20210901')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1,'600176.SH')

    #案例 3  300061  创业板的 涨幅 振幅要乘 2 的 所以测试无效
    df1 = ts.pro_bar(ts_code='300061.SZ',adj='qfq', start_date='20210206', end_date='20210429')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1,'300061.SZ')
    #------
    # 案例 1 藏格控股--强势股票**000408.SZ
    df1 = ts.pro_bar(ts_code='000408.SZ',adj='qfq', start_date='20210206', end_date='20210518')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1,'000408.SZ')

'''
测试老师的案例 6月份的案例
'''
def test_isAn_FanKeWeiZhu_Plus_laoshi_6yue():
    # 案例 1 藏格控股--强势股票**000408.SZ
    df1 = ts.pro_bar(ts_code='000408.SZ',adj='qfq', start_date='20210206', end_date='20210518')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1,'000408.SZ')

    # 案例 2  新华锦**600735.SH
    df1 = ts.pro_bar(ts_code='600735.SH',adj='qfq', start_date='20210206', end_date='20210510')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1,'600735.SH')

    # 案例 3
    df1 = ts.pro_bar(ts_code='600735.SH',adj='qfq', start_date='20210206', end_date='20210510')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1,'600735.SH')

    # 案例 4 西藏珠峰--强势股票**600338.SH

    df1 = ts.pro_bar(ts_code='600338.SH', adj='qfq', start_date='20210206', end_date='20210512')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1, '600338.SH')

    # 案例 5
    df1 = ts.pro_bar(ts_code='300001.SZ', adj='qfq', start_date='20190206', end_date='20201223')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1, '300001.SZ')



'''
测试自己的案例
'''
def test_isAn_FanKeWeiZhu_Plus_ziji():
    # 案例 5

    df1 = ts.pro_bar(ts_code='600784.SH',adj='qfq', start_date='20210206', end_date='20211029')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_Plus_model(data7_1,'600784.SH')




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


        data7_4 = df.iloc[22:27]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 3 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_FanKeWeiZhu_Plus_model(data7_4[i:i + 3], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_FanKeWeiZhu_Plus(localpath1)
    # test_isAn_FanKeWeiZhu_Plus_laoshi_10yue()
    # test_isAn_FanKeWeiZhu_Plus_laoshi_6yue()
    # test_Befor_data()
    # test_isAn_FanKeWeiZhu_Plus_ziji()