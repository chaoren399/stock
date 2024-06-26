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

XiaoV

1-一定是上涨趋势的突破 （近20天是1年来最高点）

2- 至少连续2天的下降， 第3天是一个阳线， 尾盘买入

3- 止损： 这3天的最低价 （收盘的时候止损）
'''
chengongs=[]
modelname='YinGaoYangDi'
#BASE_DIR + '/jishu_stock/z_stockdata/模型编码.csv'



def get_all_YinGaoYangDi(localpath1):
    info1=  '--小V  start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:130]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_YinGaoYangDi_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YinGaoYangDi_model(data, stockcode):
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
        # print data1
        data2= data[len_data-22:len_data-2]   # huoqu suo xuyao de shuju1
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        data3= data[len_data-3:len_data-2]   # huoqu suo xuyao de shuju1
        data3 = data3.reset_index(drop=True)  # 重新建立索引 ,
        # print data3

        key_1 = 0  # yin  yang
        key_2 = 0 # yingao  yangdi


        key_4=0 # dayinxian  gao  20days

        key_5=0 # da yinxian  qian yi tian , buneng shi zhangtingban

        count=0


        day1_low=0
        day1_open=0
        day2_high=0

        for index,row in data1.iterrows():

            if(index==0 and isYinXian(row)==1):
                count=count+1

                day1_low=row['low']
                day1_open=row['open']


            if(index==1 and isYangXian(row)==1):
                count=count+1
                day2_high= row['high']
        day20s_high = getMax_High_fromDataFrame(data2)

        for index, row in data3.iterrows():
            if (index == 0 and isZhangTingBan(row) !=1):
                key_5=1



        if (count==2):
            key_1=1
        if(day1_low > day2_high):
            key_2=1

        if(day1_open > day20s_high):
            key_4=1

        if(key_1==1 and key_2==1  and key_4==1 and key_5 ==1) :
            # print data1
            # print data3
            # print day1_open
            # print day0_high
        # if(key_1==1 ):
            info = ''

            info = info + "YinGaoYangDi--"  + str(riqi)
            # print len(data)
            # print info

            writeLog_to_txt(info, stockcode)

            path = modelname+'.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)







'''
测试老师的案例
'''
def test_isAn_YinGaoYangDi_model_laoshi():
    # 案例 1 gong da diansheng
    st_code='002655.SZ'
    df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20240611')

    data7_1 = df1.iloc[0:100]  # 前7行
    # print data7_1
    isAn_YinGaoYangDi_model(data7_1, st_code)


'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST_tmp.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        data7_4 = df.iloc[0:300]  # 前10个交易日
        # print data7_4
        # data7_4 = df.iloc[22:22+62+22]  # 前1个个月

        # data7_4 = df.iloc[22*3:22*3+62+22]  # 前2个月
        # data7_4 = df.iloc[22:22+62+120]  # 半年
        # data7_4 = df.iloc[22:22+62+250]  # 前1年
        len_1=len(data7_4)
        n=22 # jian ge tian shu
        for i in range(0, len_1-n-1 ):
            # print "i" + str(i )+ "j"+str(i+n)
            # print data7_4[i:i + 2]
            # isAn_YinGaoYangDi_model(data7_4[i:i + 62], stock_code)
            isAn_YinGaoYangDi_model(data7_4[i:i + n], stock_code)



if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/z_stockdata/data1/'



    # get_all_YinGaoYangDi(localpath1)
    # test_isAn_YinGaoYangDi_model_laoshi()
    test_Befor_data()



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"