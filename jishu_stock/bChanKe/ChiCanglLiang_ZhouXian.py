#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.agetdata.liutongshizhi.LiuTongShiZhi import LTSZ_IS_Small_100YI
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import hasXiongShiMoQi

from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
持仓量的多少看周线,  寻找已经建仓完毕,突破要拉升的股票. 过滤所有股票池的 


当汽车 出现违规的时候交警才 注意他. 

思路: 周线获取 10 个数据 ,x1,x2,x3....,  然后 找到 这 10 个数据的最大值与最小值 max0, min0 .

从最小值开始遍历到 最大值 步进为 0.01 ,   
例如,a1 ,  在 x1, 内, count= count +1
a1 在 x2 内, count= count +1  ...  如果 count >=7 ,满足条件 退出 . 否则继续循环. 
预计 空间为: 10 元里边有, 10*100 =1000 词循环.  OK


https://www.yuque.com/chaoren399/eozlgk/vg3ik9 案例:


ChiCangLiang_ZhouXian
'''
chengongs = []
modelname = '持仓量_周线'


def get_all_ChiCangLiang_ZhouXian(localpath1):
    info1 = '--持仓量_周线 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + '/jishu_stock/stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        # stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        # df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:40]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ChiCangLiang_ZhouXian_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''


def isAn_ChiCangLiang_ZhouXian_model(data, stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if (len_data >= 11):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1 = data[len_data -1- 10:len_data-1]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        riqi1 = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        data2 = data[len_data - 1:len_data]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1 = 0;  # 当天 收阳线  涨幅 6% 以上 的个股
        key_2 = 0; # 本周必须是阳线
        key_3 = 0; # 为了打印日志 区别 大于 7 的 哪些票子.
        key_4 =1 ; #  第一周的收盘价 要 高于其他 10 周的收盘价


        '''
        思路: 周线获取 10 个数据 ,x1,x2,x3....,  然后 找到 这 10 个数据的最大值与最小值 max0, min0 .

从最小值开始遍历到 最大值 步进为 0.01 ,   
例如,a1 ,  在 x1, 内, count= count +1
a1 在 x2 内, count= count +1  ...  如果 count >=7 ,满足条件 退出 . 否则继续循环. 
预计 空间为: 10 元里边有, 10*100 =1000 词循环.  OK
        '''

        #key_2=0; # 本周必须是阳线
        week0_close= 0
        for index, row in data2.iterrows():
            if(index==0):
                week0_close=row['close']
                if(isYangXian(row)==1):
                    key_2=1
        if(key_2==1):
            # key_4 = 0;  # 第一周的收盘价 要 高于其他 10 周的收盘价
            for index, row in data1.iterrows():
                close= row['close']
                if(close > week0_close):
                    key_4=0
                    break  # 如果 收盘价有大于 本周的,那么就要终止

        if(key_2==1 and key_4==1): #减少遍历的时间

            #1-找到 10 个数据的最大值 max0 最小值 min0
            max0=0
            min0=0
            for index, row in data1.iterrows():
                high = row['high']
                low = row['low']
                if(index==0):
                    max0= high
                    min0= low
                    riqi=row['trade_date']
                if(high > max0):
                    max0=high
                if(low < min0):
                    min0=low

                if(index==9):
                    riqi1 = row['trade_date']
            #遍历 max0 min0
            import numpy as np
            list = np.arange(min0, max0, 0.01)

            zhongjianzhi=0
            for item in list:
                zhongjianzhi = round(item,2)
                count = 0  # 计数 满足 大于 7 的个数
                # 遍历 10 个数据
                for index, row in data1.iterrows():
                    high = row['high']
                    low = row['low']
                    if(zhongjianzhi >=low  and zhongjianzhi <= high):
                        count=count+1
                    if(count>=6): #6个满足 神1 中路股份**600818.SH
                        key_1=1
                        # print zhongjianzhi
                        # print '---22--'+'count ='+str(count)
                    if(count >=7): # 为了打印日志 区别 大于 7 的 哪些票子.
                        key_3=1
                        break;
                # print '---count='+str(count)
                if(count>=7):  # 终止 外层的循环, 不然 中间值会继续 赋值 之前是 6,改成大于 7 比较合适, 否则 有些值到了 6 打印的会不显示
                    break

        # print1(key_1)
        # print1(key_2)
        if (key_1 == 1 and key_2==1 ):

            if (1):
                info = ''

                info = info + "--持仓量_周线 看周线 然后看日线--" +'开始=' +str(riqi) +'-结束='+str(riqi1)
                info = info + '--中间值='+str(zhongjianzhi)
                if(key_3==1):
                    info = info + '--大于7个--'
                    # print info
                writeLog_to_txt(info, stockcode)
                path = modelname + '.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)

                chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
                # print1(day2_shizixing_low)
                chengongs.append(chenggong_code)


'''
测试老师的案例
'''


def test_isAn_ChiCangLiang_ZhouXian_laoshi():
    # 案例 1  福建金森 002679  老师的案例
    df = ts.pro_bar(ts_code='002679.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20181026')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_ChiCangLiang_ZhouXian_model(data7_1, '002679.SZ')

    # 案例 2 自己找  悦心健康 002162
    df = ts.pro_bar(ts_code='002162.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20220218')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_ChiCangLiang_ZhouXian_model(data7_1, '002162.SZ')

    # 案例 3 自己找  中坚科技 002779 20220128
    df = ts.pro_bar(ts_code='002779.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20220211')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_ChiCangLiang_ZhouXian_model(data7_1, '002779.SZ')

    # 案例 4 自己找  宁波联合 600051  20220225
    df = ts.pro_bar(ts_code='600051.SH', adj='qfq', freq='W', start_date='20170101', end_date='20220304')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_ChiCangLiang_ZhouXian_model(data7_1, '600051.SH')

    # 案例 5 自己找  中路股份 600818  20220114  神1 成功案例
    df = ts.pro_bar(ts_code='600818.SH', adj='qfq', freq='W', start_date='20170101', end_date='20220114')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_ChiCangLiang_ZhouXian_model(data7_1, '600818.SH')

    # 神 3

'''
测试自己的案例
'''


def test_isAn_ChiCangLiang_ZhouXian_ziji():
    # 案例 4 自己找  中路股份 600818  20220114  神1 成功案例 01-11 筹码突破
    df = ts.pro_bar(ts_code='600818.SH', adj='qfq', freq='W', start_date='20170101', end_date='20220114')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_ChiCangLiang_ZhouXian_model(data7_1, '600818.SH')




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
            isAn_ChiCangLiang_ZhouXian_model(data7_4[i:i + n], stock_code)

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

    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_ChiCangLiang_ZhouXian(localpath1)
    # test_isAn_ChiCangLiang_ZhouXian_laoshi()
    # test_isAn_ChiCangLiang_ZhouXian_ziji()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"