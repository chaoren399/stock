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
from jishu_stock.z_tool.isXiongShiMoQi import hasXiongShiMoQi

from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan, isYiZiBan
import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
4个小阳线+ 1 个涨停板

思路: 自己看李栋案例, 感觉出来的, 自己分析主力的辅助 . 这种主力慢慢进场的.

4Yang1ZTB

4阳1涨停板
'''
chengongs = []
modelname = '4阳1涨停板'


def get_all_4Yang1ZTB(localpath1):
    info1 = '--4阳1涨停板 start--   '
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
        isAn_4Yang1ZTB_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''


def isAn_4Yang1ZTB_model(data, stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if (len_data >= 10):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1 = data[len_data - 5:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期

        mairuriqi = 0
        zhisundian = 0

        # print1(data1)




        # 设置两个 key
        key_1 = 0;  #最近 5 天的数据, 前 4天是小阳线, 第 5 天是涨停板



        count=0
        for index, row in data1.iterrows():
            if(index==0 and isZhangTingBan(row)==0 and isYangXian(row)==1):
                count=count+1
            if(index==1 and isZhangTingBan(row)==0 and isYangXian(row)==1):
                count=count+1
            if(index==2 and isZhangTingBan(row)==0 and isYangXian(row)==1):
                count=count+1
            if(index==3 and isZhangTingBan(row)==0 and isYangXian(row)==1):
                count=count+1
            if(index==4 and isZhangTingBan(row)==1 and isYangXian(row)==1):
                count=count+1
        if(count==5):
            key_1=1



        # print1(key_1)
        # print1(key_2)
        if (key_1 == 1 ):
            info = ''

            info = info + "--4阳1涨停板成功了--" + '--日期:' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = modelname + '.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
            # print1(day2_shizixing_low)
            chengongs.append(chenggong_code)




'''
测试老师的案例 案例: 
'''


def test_isAn_4Yang1ZTB_laoshi():
    # 案例 1 000088
    df1 = ts.pro_bar(ts_code='000088.SZ', adj='qfq', start_date='20190206', end_date='20200706')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_4Yang1ZTB_model(data7_1, '000088.SZ')





'''
测试自己的案例
'''


def test_isAn_XiaoYangJianCang_ziji():
    # 自己的 案例
    df1 = ts.pro_bar(ts_code='002838.SZ', adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_4Yang1ZTB_model(data7_1, '002507.SZ')


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
        n = 30
        data7_4 = df.iloc[22:22 + n + 5]  # 前1个月个交易日
        data7_4 = df.iloc[22:22 + n + 22]  # 1 个月
        data7_4 = df.iloc[22:22 + n + 120]  # 半年
        data7_4 = df.iloc[0:0 + n + 22]  # 半年
        # data7_4 = df.iloc[22:22+132+250]  # 1年

        len_1 = len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_4Yang1ZTB_model(data7_4[i:i + n], stock_code)

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
    from time import *

    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_4Yang1ZTB(localpath1)
    # test_isAn_4Yang1ZTB_laoshi()
    # test_Befor_data()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"