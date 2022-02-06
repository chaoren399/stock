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

from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

'''
神龙摆尾 4
https://www.yuque.com/chaoren399/eozlgk/fkbnbi

下跌横盘缓慢上涨
涨幅5%左右的放量中阳线 且成为近期高点
之后横盘或下跌调整10个交易日以内
之后再次放量阳线
创之前阳线的新高且成交量更大


思路:


思路 找到最近 60 天的数据, 然后 判断最新一天是不是阳线,而且是 最近 60 的最大值,  yangxian1 放量

如果是, 继续循环 找5% 放量阳线 yangxian2


'''

chengongs=[]
modelname='神4Pro'

def get_all_Shen4_Pro(localpath1):
    info1=  '--神4Pro start--   '
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
        isAn_Shen4_Pro_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_Shen4_Pro_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-60:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        len_data1 = len(data1)
        data2=  data1[len_data1-2:len_data1]  # 找到最近2 天的数据 找到最新一天的阳线1
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,
        len_data2=len(data2)
        print1(data2)
        # 设置两个 key
        key_1=0; #最新一天阳线
        key_2=0; #最新一天阳线  放量

        # 第一步 找到最新一天的阳线1
        yangxian1_day1_amount=0
        day1_amount=0
        day2_amount=0
        for index,row in data2.iterrows(): # 找到最新一天的阳线1
            if(index==0):
                day1_amount= row['amount']
            if(index==1):
                day2_amount= row['amount']
                yangxian1_day1_amount=day2_amount
                if(isYangXian(row)==1):
                    key_1=1
        if(day2_amount > day1_amount):
            key_2=1

        #第 2 步  找到 5% 的放量阳线2

        data3 = data1[len_data1 -4-6:len_data1-4]  # 找到除了最新一天后 的近 6 天的数据
        data3 = data3.reset_index(drop=True)  # 重新建立索引 ,
        # print data3
        for index, row in data3.iterrows():
            if(index>0):
                pct_chg = row['pct_chg']
                if (pct_chg >= 3.9 and pct_chg < 7.5):  # 5% 左右
                    a




        print1(key_1)
        print1(key_2)
        if(key_1==1 and  key_2 ==1):
            info = ''

            info = info + "--Shen4_Pro 成功了--"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = modelname + '.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            # print1(day2_shizixing_low)
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_ShenLongBaiWei2_laoshi():
    # 案例 1
    df4 = ts.pro_bar(ts_code='600085.SH', start_date='20210417', end_date='20210514')
    data7_4 = df4.iloc[0:60]  # 前10个交易日
    isAn_Shen4_Pro_model(data7_4, '600085.SH')

    # 案例 2

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_Shen4_Pro_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_Shen4_Pro_model(data7_1,'002507.SZ')

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

        n = 5  # 模型需要最低的数据
        # data7_4 = df.iloc[22:22 + n + 5]  # 前1个月个交易日
        data7_4 = df.iloc[22:22 + n + 22]  # 1 个月
        # data7_4 = df.iloc[22:22 + n + 120]  # 半年
        # data7_4 = df.iloc[22:22+n+250]  # 1年

        len_1 = len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_Shen4_Pro_model(data7_4[i:i + n], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    # jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)


if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_Shen4_Pro(localpath1)
    test_isAn_ShenLongBaiWei2_laoshi()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"