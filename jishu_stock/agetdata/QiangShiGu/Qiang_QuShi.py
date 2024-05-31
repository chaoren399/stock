#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.StockCode_Tool import getSockCode_from_SZSH601899
from jishu_stock.z_tool.email import webhook
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
看到东方电子突破后回调 ，然后看到威程操作的麻雀战法，吃一口就跑的策略
自己深度思考，这么大的市场，就没有我自己的模式吗？

所以我要自己搞一个模式

1 一定是有人气的票， 什么票有人气？  就是突破的票，吸引了人。
2 一定是在人们胆怯的时候进去。。

Qiang_QuShi

1-一定是上涨趋势的突破 （近20天是1年来最高点）

2- 至少连续2天的下降， 第3天是一个阳线， 尾盘买入

3- 止损： 这3天的最低价 （收盘的时候止损）
'''
chengongs=[]
modelname='Qiang_QuShi'
#BASE_DIR + '/jishu_stock/stockdata/模型编码.csv'


def test():

    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/qiang_qushi_stocks.csv'

    data = pd.read_csv(path, dtype={'code': str})
    all_count=0
    for index, row in data.iterrows():
        code = row['代码']
        # stock_code = row['ts_code']
        # print row
        code = getSockCode_from_SZSH601899(code)
        if(code):
            print code
def get_all_Qiang_QuShi(localpath1):
    info1=  '--Qiang_QuShi  start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    all_count=0
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:130]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        x = isAn_Qiang_QuShi_model(data6_1, stock_code)

        if (x == 1):
            all_count = all_count + 1

    print modelname+"总数量=" + str(all_count)
'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_Qiang_QuShi_model(data, stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-2:len_data]   # huoqu suo xuyao de shuju1
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0  # 第一天买入， 第2天卖出
        zhisundian = 0
        # print1(data1)

        data2= data[len_data-20:len_data]  #
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,


        data3= data[len_data-20 - 230 :len_data-20]  #
        data3 = data3.reset_index(drop=True)  # 重新建立索引 ,


        # 设置两个 key
        key_1=0; # 3tian  yin -yin -yang

        key_2=0; # 近30天 最高点是近1年的最高点 --突破
        key_3=1 ; #3前边没有涨停板




        count=0
        day1_open=0
        day1_close=0
        day2_open=0
        day2_close=0
        day1_amount=0
        day2_amount=0

        for index,row in data1.iterrows():


            if(index==0 and isYinXian(row)==1):
                count=count+1

                day1_open=row['open']
                day1_close=row['close']
                day1_amount=row['amount']

            if(index==1 and isYinXian(row)==1):
                count=count+1
                day2_open= row['open']
                day2_close= row['close']

                day2_amount=row['amount']
                zhisundian = row['low']
                mairuriqi = row['trade_date']



        if (count==2):
            key_1=1
        data2Max=getMax_High_fromDataFrame(data2)
        data3Max=getMax_High_fromDataFrame(data3)
        # print data3

        if(data2Max > data3Max):
            key_2=1


        # if(key_1==1 & key_2==1):
        if(key_2==1):
        # if(key_1==1 ):
            info = ''

            info = info + "Qiang_QuShi--"  + str(mairuriqi)
            # print len(data)
            # print info

            writeLog_to_txt(info, stockcode)

            path = modelname+'.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            # print1(day2_shizixing_low)
            chengongs.append(chenggong_code)
            return 1
    return 0





'''
测试老师的案例
'''
def test_isAn_Qiang_QuShi_model_laoshi():
    # 案例 1 dongfangdianzi
    st_code='000017.SZ'
    df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20240513')

    data7_1 = df1.iloc[0:100]  # 前7行
    # print data7_1
    isAn_Qiang_QuShi_model(data7_1, st_code)

    # 案例 2 zhongguoxidian
    st_code='601179.SH'
    df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20240506')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    # isAn_XiaoV_model(data7_1,st_code)

    # 案例 3


if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/stockdata/data1/'

    # test_isAn_XiaoV_model_laoshi()

    get_all_Qiang_QuShi(localpath1)
    # test()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"