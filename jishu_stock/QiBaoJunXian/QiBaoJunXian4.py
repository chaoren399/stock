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
起爆均线4（自研）胜率 80%以上

判断   https://xueqiu.com/3476656801/204163278
思路:   

发现 很多案例都是  第一天的阳线 穿越 144 169 , 然后第 2 天 跳空高开 

https://xueqiu.com/3476656801/205942059

首先 找1个大阳线 穿越 起爆均线144,169的， 

然后144,169 都是向上的，

之前的最小值都是低于144,169的





QiBaoJunXian4

创建日期:2021年12月14日
更新日期: 
'''

chengongs=[]
modelname='起爆均线4'
def get_all_QiBaoJunXian4(localpath1):
    info1=  '--起爆均线4 start--   '
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
        isAn_QiBaoJunXian4_model(data6_1, stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_QiBaoJunXian4_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        data2= data[len_data-2-5:len_data-2]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,




        # 设置两个 key
        key_1=0; #1.  第一天的阳线 穿越 144 169 ,
        key_2=0; #2  然后第 2 天 跳空高开

        key_3=1; # 3 前 5 天的 最低值都要小于 169 144


        day1_close=0
        day1_144=0
        day1_169=0
        day1_low=0

        day2_open=0
        for index , row in data1.iterrows():
            if(index==0 and  isYangXian(row)==1):
                day1_open=row['open']
                day1_close=row['close']
                day1_144=row['ma144']
                day1_169=row['ma169']
                day1_low=row['low']
                # print day1_low
                day1_high=row['high']
                zhisundian=day1_low
            if(index==1 and isYangXian(row)==1):
                day2_open=row['open']
                mairuriqi=row['trade_date']

        # 1.  第一天的阳线的 最低价 与 第 2 天的开盘价   穿越 144 169 ,
        if(day1_144 > day1_low  and day1_169 > day1_low
                and  day1_144 < day2_open and day1_169 < day2_open):
            key_1=1

        # 2  然后第 2 天 跳空高开

        if(day2_open >= day1_close):
            key_2=1


        #key_3=0; # 3 前 5 天的 最低值都要小于 169 144

        for index ,row in data2.iterrows():
            ma144=row['ma144']
            ma169=row['ma169']
            day_low=row['low']
            if(day_low >= ma144 or day_low >= ma169):
                key_3=0



        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(day1_low)

        key_4=0

        if(key_1==1 and  key_2 ==1 and key_3==1 ):
            info = ''
            if (is144_169_shangzhang(data2) == 2):
                info = info + '144-169满足上涨'
                key_4=1
            else:
                info = info + '144-169不满足上涨'

            if(key_4==1):

                info = info + "-----起爆均线4----"  + str(riqi)
                # print info
                writeLog_to_txt(info, stockcode)
                path = '起爆均线4.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)

                chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
                chengongs.append(chenggong_code)


''''
判断 144.169 是不是上涨趋势, 发现 144 会变化, 但是 169 稳定上涨. 取 10 天的数据就可以
'''
def is144_169_shangzhang(data):
    ma144s=[]
    ma169s=[]
    count=0
    for index, row in data.iterrows():
        ma144s.append(round(row['ma144'],2))
        ma169s.append(round(row['ma169'],2))

    if(is_small_to_big(ma144s)==1 ):
        count=count+1
    if(is_small_to_big(ma169s)==1 ):
        count=count+1
    # print1(ma144s)
    # print1(ma169s)
    return count


'''
测试老师的案例
'''
def test_isAn_QiBaoJunXian4_laoshi():

    #案例 1 金发拉比**002762.SZ  第 2 天开盘价 等于第一天
    df1 = ts.pro_bar(ts_code='002762.SZ', adj='qfq', start_date='20200206', end_date='20210331',
                     ma=[5, 13, 34, 144, 169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian4_model(data7_1, '002762.SZ')

    # 案例 2 九安医疗**002432.SZ
    df1 = ts.pro_bar(ts_code='002432.SZ', adj='qfq', start_date='20200206', end_date='20211116',
                     ma=[5, 13, 34, 144, 169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian4_model(data7_1, '002432.SZ')

    # 案例 3 天下秀--强势股票**600556.SH
    df1 = ts.pro_bar(ts_code='600556.SH', adj='qfq', start_date='20200206', end_date='20211101',
                     ma=[5, 13, 34, 144, 169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian4_model(data7_1, '600556.SH')

    # 案例 4  605116.SH
    df1 = ts.pro_bar(ts_code='605116.SH', adj='qfq', start_date='20200206', end_date='20211125',
                     ma=[5, 13, 34, 144, 169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian4_model(data7_1, '605116.SH')

    # 案例 5  跃岭股份**002725.SZ
    df1 = ts.pro_bar(ts_code='002725.SZ', adj='qfq', start_date='20200206', end_date='20211206',
                     ma=[5, 13, 34, 144, 169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian4_model(data7_1, '002725.SZ')

    # 案例 6 萃华珠宝--强势股票**002731.SZ
    df1 = ts.pro_bar(ts_code='002731.SZ', adj='qfq', start_date='20200206', end_date='20210908',
                     ma=[5, 13, 34, 144, 169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian4_model(data7_1, '002731.SZ')







'''
测试自己的案例
'''
def test_isAn_QiBaoJunXian4_ziji():
    #自己的 案例
    # 案例 金山股份
    df1 = ts.pro_bar(ts_code='600396.SH', adj='qfq', start_date='20200206', end_date='20211208',
                     ma=[5, 13, 34, 144, 169])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_QiBaoJunXian4_model(data7_1, '600396.SH')

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
        # data7_4 = df.iloc[22:22+10+5]  #前1个月个交易日
        data7_4 = df.iloc[22:22+10+22]  #1 个月
        # data7_4 = df.iloc[22:22+10+120]  # 半年
        # data7_4 = df.iloc[22:22+10+250]  # 1年
        len_1=len(data7_4)
        for i in range(0, len_1 - 10 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_QiBaoJunXian4_model(data7_4[i:i + 10], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    # jisuan_all_shouyilv(chengongs, modelname, 1.15)

    # jisuan_all_shouyilv_10_5(chengongs, modelname, 1.10, 0.95)
    # jisuan_all_shouyilv_10_5(chengongs, modelname, 1.05, 0.95)


if __name__ == '__main__':

    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_QiBaoJunXian4(localpath1)
    # test_isAn_QiBaoJunXian4_laoshi()


    test_Befor_data()
    # test_isAn_QiBaoJunXian4_ziji()
    # jisuan_all_shouyilv(chengongs, modelname, 1.03)


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"