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

''''
海底捞模型的条件

条件一： 高开放量的阴线， 振幅 5%以上
条件二： 放量阴线的开盘价是近期的新高，至少2个月。
条件三：  放量阴线 比昨天和明天的量都大。

2022年05月07日 编写


HaiDiLao
'''
chengongs=[]
modelname='海底捞'

def get_all_HaiDiLao(localpath1):
    info1=  '--海底捞 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        n = 2
        data6_1 = df.iloc[n + 0:n + 100]  # 回测

        # data6_1 = df.iloc[0:30]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        if(stock_code == '603390.SH'):
            print '603390.SH  come in '

            isAn_HaiDiLao_model(data6_1, stock_code)

            print data6_1



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_HaiDiLao_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-3:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[2]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        data2 = data[len_data - 30:len_data]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,


        # 设置两个 key
        key_1=0; # 阴线
        key_2=0; # 放量
        key_3=0; # 实体大小 大于 5
        key_4=1; # 开盘价是最近新高

        day1_vol =0
        day2_vol=0
        day3_vol=0

        day2_fuguiyin_shiti=0
        day2_fuguiyin_open = 0
        for index,row in data1.iterrows():
            if(index==0):
                day1_vol= row['vol']
            if(index==1):
                day2_fuguiyin_shiti = getShiTiDaXiao(row)
                day2_vol = row['vol']
                day2_fuguiyin_open= row ['open']
                if(isYinXian(row)==1):
                    key_1=1
            if(index==2):
                day3_vol = row['vol']

        if(day2_vol > day1_vol and day2_vol > day3_vol): #放量
            key_2=1


        # 开盘价是最近 60 天 新高
        for index, row in data2.iterrows():

            openprice = row['open']
            closeprice = row['close']
            if(openprice > day2_fuguiyin_open or closeprice > day2_fuguiyin_open):
                key_4=0

        if(day2_fuguiyin_shiti > 5): #实体大小 大于 5
            key_3=1
        print1(key_1)
        print1(key_2)
        print1(key_3)
        print1(key_4)
        # print1(day2_fuguiyin_shiti)

        if(key_1==1 and  key_2 ==1 and key_3 ==1 and key_4==1):
            info = ''

            info = info + "--海底捞  成功了--"  + str(riqi)
            info = info + "--实体="  + str(day2_fuguiyin_shiti)

            # 统一 info管理 一个函数,每次都要执行, 并且信息 返回后,要添加到 info中,
            # 方便后期修改,这样一改,所有的都可以执行了.
            from jishu_stock.z_tool.InfoTool import manage_info
            manage_info = manage_info(info, stockcode, riqi, '')
            info = info + manage_info

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
def test_isAn_HaiDiLao_laoshi():
    # 案例 1  大东方-2021-05-19 - 600327
    df1 = ts.pro_bar(ts_code='600327.SH',adj='qfq', start_date='20200206', end_date='20210518')
    data7_1 = df1.iloc[0:100]  # 前7行
    isAn_HaiDiLao_model(data7_1,'600327.SH')

    # 案例 2 2021-06-15 -先锋电子-002767

    df1 = ts.pro_bar(ts_code='002767.SZ',adj='qfq', start_date='20200206', end_date='20210611')
    data7_1 = df1.iloc[0:100]  # 前7行
    isAn_HaiDiLao_model(data7_1,'002767.SZ')

    # 案例 3 2021-06-29 -海源复材-002529

    df1 = ts.pro_bar(ts_code='002529.SZ',adj='qfq', start_date='20200206', end_date='20210625')
    data7_1 = df1.iloc[0:100]  # 前7行
    isAn_HaiDiLao_model(data7_1,'002529.SZ')

    # 案例4 海南瑞泽-002596

    df1 = ts.pro_bar(ts_code='002596.SZ',adj='qfq', start_date='20200206', end_date='20220325')
    data7_1 = df1.iloc[0:100]  # 前7行
    isAn_HaiDiLao_model(data7_1,'002596.SZ')

    #案例5  2022年05月05日 永安药业-002365

    df1 = ts.pro_bar(ts_code='002365.SZ',adj='qfq', start_date='20210206', end_date='20220418')
    data7_1 = df1.iloc[0:100]  # 前7行
    isAn_HaiDiLao_model(data7_1,'002365.SZ')


'''
测试自己的案例
'''
def test_isAn_HaiDiLao_ziji():
    #自己的 案例 ,汽车配件,通达电气**603390.SH
    df1 = ts.pro_bar(ts_code='603390.SH',adj='qfq', start_date='20210206', end_date='20220510')
    data7_1 = df1.iloc[0:100]  # 前7行
    isAn_HaiDiLao_model(data7_1,'603390.SH')

    #自己的 塞力医疗-603716
    df1 = ts.pro_bar(ts_code='603716.SH',adj='qfq', start_date='20210206', end_date='20220510')
    data7_1 = df1.iloc[0:100]  # 前7行
    isAn_HaiDiLao_model(data7_1,'603716.SH')


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

        n = 5  # 模型需要最低的数据
        # data7_4 = df.iloc[22:22 + n + 5]  # 前1个月个交易日
        data7_4 = df.iloc[22:22 + n + 22]  # 1 个月
        # data7_4 = df.iloc[22:22 + n + 120]  # 半年
        # data7_4 = df.iloc[22:22+n+250]  # 1年

        len_1 = len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_HaiDiLao_model(data7_4[i:i + n], stock_code)

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


    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_HaiDiLao(localpath1)
    # test_isAn_HaiDiLao_laoshi()
    test_isAn_HaiDiLao_ziji()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"