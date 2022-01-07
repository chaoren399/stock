#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian, is_big_to_small, \
    writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from stock.settings import BASE_DIR

import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
反客为主 强庄主力仅用一天的强势洗盘

https://www.yuque.com/chaoren399/eozlgk/ysft12/

首先已经是底底抬高、顶顶抬高的上涨结构，是个追涨模型，强庄主力仅用一天的强势洗盘。

在上涨结构中产生的中阴线或大阴线（有实体的，不是一字板），
第二天是高开高走的大阳线，其中高开高走指阳线开盘价高于阴线收盘价，阳线收盘价高于阴线开盘价， 
第三天开盘买入，以阴线或阳线的最低价为止损。

一般可这样区分：
 小阴线和小阳线的波动范围一般在0.6--1.5%；
 中阴线和中阳线的波动范围一般在1.6-3.5%；
 大阴线和大阳线的波动范围在3.6%以上。
 
 
涨 3 个月以内的最好
宁可错杀一千,不可选错一个

胜率 80%


'''

chengongs=[]
modelname='反客为主'

def get_all_FanKeWeiZhu(localpath1):
    info1=  '--反客为主 找 刚起来 不超过 3 个月的 强庄主力仅用一天的强势洗盘 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        data6_1 = df.iloc[0:2]  # 前6行
        # data6_1 = df.iloc[1:3]  # 前6行
        # data6_1 = df.iloc[3:5]  # 前6行
        isAn_FanKeWeiZhu_model(data6_1, stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_FanKeWeiZhu_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print1( data)


        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        # 设置两个 key
        key_1=0; # 先判断 阴阳
        key_2=0; # 是不是高开高走的大阳线
        key_3=0;  #判断是不是 中阴线 大阳线

        key_4=0; #  10 周,60 周均线是不是向上




        day1_open=0
        day1_close=0
        day2_open=0
        day2_close=0
        count1=0
        chazhi1=0
        chazhi2=0
        yangxian_pct_chg=0
        for index, row in data1.iterrows():
            if(index==0 and isYangXian(row) ==0):
                count1=count1+1
                day1_open=row['open']
                day1_close=row['close']
                chazhi1 = format(((row['close'] - row['open']) / row['open']) * 100 ,'.2f') # (开盘价-收盘价)÷开盘价＜0.5%

                zhisundian=row['low']
            if(index==1 and isYangXian(row)==1):
                count1 = count1 + 1
                day2_open = row['open']
                day2_close = row['close']
                chazhi2 = format(((row['close'] - row['open']) / row['open']) * 100,'.2f')  # (开盘价-收盘价)÷开盘价＜0.5%
                yangxian_pct_chg=row['pct_chg']
                mairuriqi=row['trade_date']
        # format(float(a) / float(b), '.2f'))
        if(count1==2):
            key_1=1
            # 阳线开盘价大于阴线收盘价  阳线收盘价高于阴线开盘价
            if(day2_open > day1_close and day2_close > day1_open):
                key_2=1


         #中阴线和中阳线的波动范围一般在1.6-3.5；
         #大阴线和大阳线的波动范围在3.6以上。

        count2=0
        # print1(chazhi1)
        # print1(chazhi2)
        if(abs(float(chazhi1))>1.6): # 中阴线的标准 大于 1.6 可以适当的放大 到 3.2
            count2=count2+1
        if(float(chazhi2) > 3.6):  #大阳线的标准可以放到 4.4 以上
            count2=count2+1



        if(count2==2):
            key_3=1


        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        if(key_1==1 and  key_2 ==1 and key_3==1):
            # 10 周均线是不是向上

            if(is10_60Week_XiangShang(stockcode, riqi) ==2):
               key_4=1

            # print1(key_4)

            if(key_4==1):
                Yang_Yin = (float(chazhi2) / abs(float(chazhi1)))
                # print1(Yang_Yin)
                if( Yang_Yin > 1 and Yang_Yin<2):  # 判断阳线和阴线实体的比例 选择大于 1 小于 2 的最好

                    info ='中阴线=' + str(chazhi1) +','+'大阳线='+str(chazhi2)+'-涨幅-'+str(yangxian_pct_chg)
                    info =info + "-----反客为主  刚起来 不超过 3 个月 强庄主力仅用一天的强势洗盘 ----" + str(riqi)
                    # print info
                    writeLog_to_txt(info, stockcode)

                    path = '反客为主.txt'
                    writeLog_to_txt_path_getcodename(info, path, stockcode)

                    chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
                    chengongs.append(chenggong_code)

#10 周均线是不是向上
def is10_60Week_XiangShang(stock_code, riqi):
    df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20180101', end_date=str(riqi))

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
    df_week = df_week[0:4]  # 一年有 48 周
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
测试老师的案例
'''
def test_isAn_FanKeWeiZhu_laoshi():
    # 案例 1
    df1 = ts.pro_bar(ts_code='000408.SZ',adj='qfq', start_date='20210206', end_date='20210518')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_model(data7_1,'000408.SZ')

    # 案例 2
    df1 = ts.pro_bar(ts_code='600735.SH',adj='qfq', start_date='20210206', end_date='20210510')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_model(data7_1,'600735.SH')

    # 案例 3

    df1 = ts.pro_bar(ts_code='600735.SH',adj='qfq', start_date='20210206', end_date='20210518')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_model(data7_1,'600735.SH')

    # 案例 4

    df1 = ts.pro_bar(ts_code='600338.SH', adj='qfq', start_date='20210206', end_date='20210512')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_model(data7_1, '600338.SH')

    # 案例 5
    df1 = ts.pro_bar(ts_code='300001.SZ', adj='qfq', start_date='20190206', end_date='20201223')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_model(data7_1, '300001.SZ')



'''
测试自己的案例
'''
def test_isAn_FanKeWeiZhu_ziji():
    # 案例 5
    df1 = ts.pro_bar(ts_code='300001.SZ', adj='qfq', start_date='20190206', end_date='20201030')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_FanKeWeiZhu_model(data7_1, '300001.SZ')




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
        data7_4 = df.iloc[22:22+2+22]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 2 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_FanKeWeiZhu_model(data7_4[i:i + 2], stock_code)

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

    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_FanKeWeiZhu(localpath1)
    # test_isAn_FanKeWeiZhu_laoshi()
    test_Befor_data()
    # test_isAn_FanKeWeiZhu_ziji()

    # jisuan_all_shouyilv(chengongs, modelname, 1.10)

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"