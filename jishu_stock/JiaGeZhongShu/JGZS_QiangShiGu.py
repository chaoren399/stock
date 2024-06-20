#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd

from jishu_stock.JiaGeZhongShu.jiagezhognshu_Get_Week_K_data import getAll_jiagezhongshu_WeekKdata
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    jiagezhongshu_writeLog_to_txt_path_getcodename, writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.email import webhook
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
创建日期: 2024-05-29
更新日期:

每次的都要在强势股中找买点（可以是当天的热点题材）

底部横盘4周， 第5周开始突破 第6周找买点（比如小v） 

1- 首先找5周数据
2- 第5个必须是阳线且要收盘价要高过 前4个

3- 前4个的实体大小不能超过 第5个

JGZS_QiangShiGu
'''

chengongs=[]
modelname='价格中枢-QiangShiGu'


def get_all_JGZS_QiangShiGu(localpath1):
    info1=  '--上涨初期 价格中枢-QiangShiGu start-- '
    webhook.sendData( info1)
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST_xmind.csv'
    data = pd.read_csv(path, dtype={'code': str})
    all_count=0
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        # stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        try:
            df = pd.read_csv(stockdata_path, index_col=0)
            if (df.empty):
                continue
            df = df.reset_index(drop=False)  # 重新建立索引 ,
            data6_1 = df.iloc[0:8]  # 前6行
            # data6_1 = df.iloc[20:32]  # 前6行
            len1 = len(data6_1)
            # print len1
            x=isAn_JGZS_QiangShiGu_model(data6_1, stock_code)
            if(x==1):
                all_count = all_count+1

        except:
            print  'stock_code is null = ' + str(stock_code)

    print modelname+"总数量=" + str(all_count)

'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JGZS_QiangShiGu_model(data, stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 5):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-5:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        mairuriqi = 0
        zhisundian = 0

        riqi = data1.ix[4]['trade_date']  # 第5个周线，大阳线的日期
        # print riqi


        # 设置两个 key

        key_1=0;  #1第5个必须是阳线
        key_2=0; # 2 第5个收盘价高过前4个的收盘价
        key_3=0; # 2 第5个收盘价高过前4个的开盘价
        key_4=0; # 3 前4个的实体大小不能超过 第5个
        key_5=0; # 前4个的最大值要小于第5个收盘价



        week4_close=0
        week3_close=0
        week2_close=0
        week1_close=0
        week0_close=0

        week3_open=0
        week2_open=0
        week1_open=0
        week0_open=0

        week4_shiti=0
        week3_shiti=0
        week2_shiti=0
        week1_shiti=0
        week0_shiti=0

        week3_max=0
        week2_max=0
        week1_max=0
        week0_max=0


        for index, row in data1.iterrows():

            if(index==4 and isYangXian(row)==1):
                key_1 = 1
                week4_close = row['close']
                week4_shiti=getShiTiDaXiao(row)
            if (index ==3 ):
                week3_close = row['close']
                week3_open = row['open']
                week3_shiti = getShiTiDaXiao(row)
                week3_max = row['high']
            if (index ==2 ):
                week2_close = row['close']
                week2_open = row['open']
                week2_shiti = getShiTiDaXiao(row)
                week2_max = row['high']
            if (index ==1 ):
                week1_close = row['close']
                week1_open = row['open']
                week1_shiti = getShiTiDaXiao(row)
                week1_max = row['high']
            if (index == 0):
                week0_close = row['close']
                week0_open = row['open']
                week0_shiti = getShiTiDaXiao(row)
                week0_max = row['high']

        if(week4_close > week3_close and week4_close > week2_close and week4_close > week1_close and week4_close > week0_close ) :
            key_2 =1
        if(week4_close > week3_open and  week4_close > week2_open and week4_close > week1_open and week4_close > week0_open  ):
            key_3 =1
        if(week4_shiti > week3_shiti and  week4_shiti > week2_shiti and week4_shiti > week1_shiti and week4_shiti > week0_shiti  ):
            key_4=1

        if(week4_close > week3_max and  week4_close > week2_max and week4_close > week1_max  and week4_close > week0_max ):
            key_5 =1

        if(0):
        # if(1):
            print1(data1)
            print1(key_1)
            print1(key_2)
            print1(key_3)
            print1(key_4)
            print1(key_5)



        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1):


        #     print1(shangyingxian_xiayingxian)
            info = ''
            info = info + "--价格中枢QiangShiGu--" + str(riqi)




            path = BASE_DIR + '/jishu_stock/zJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                '%Y-%m-%d') + '.txt'

            jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)

            path = '价格中枢QiangShiGu.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
            chengongs.append(chenggong_code)
            return 1
    return 0

'''
测试老师的案例
'''
def test_isAn_JGZS_QiangShiGu_laoshi():
    # 案例 1
    df = ts.pro_bar(ts_code='300157.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20200807')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_JGZS_QiangShiGu_model(data7_1, '300157.SZ')

    # 案例 2  得到的数据不对
    df = ts.pro_bar(ts_code='600089.SH', adj='qfq', freq='W', start_date='20170101', end_date='20201225')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_JGZS_QiangShiGu_model(data7_1, '600089.SH')

    # 案例 3 000155
    df = ts.pro_bar(ts_code='000155.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20201225')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_JGZS_QiangShiGu_model(data7_1, '000155.SZ')

    # 案例 4
    df = ts.pro_bar(ts_code='000409.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20210226')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_JGZS_QiangShiGu_model(data7_1, '000409.SZ')



'''
测试自己的案例
'''
def test_isAn_JGZS_KanZhangZuoZhang_ziji():
    #自己的 案例
    #价格中枢-实体一半=0.04---上影线是下的几倍=1.33---阳线实体=7.26---实体看涨做涨--2021-10-31--维力医疗**603309.SH
    # df1 = ts.pro_bar(ts_code='603309.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    stock_code = '000812.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    df = df.reset_index(drop=False)  # 重新建立索引 ,
    data7_1 = df.iloc[0:8]  # 前7行
    # isAn_JGZS_QiangShiGu_model(data7_1,'000812.SZ')

    # 案例 4
    stock_code = '600163.SH'
    df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20170101', end_date='20240510')
    data7_1 = df.iloc[0:10]  # 1 年有 50 周
    isAn_JGZS_QiangShiGu_model(data7_1, stock_code)



'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        # stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
            # print df
        if (df.empty):
            continue

        df = df.reset_index(drop=False)  # 重新建立索引 ,
        data7_4 = df.iloc[8:10]  # 1 年有 52 周
        data7_4 = df.iloc[8:8+2+4]  # 上个与的

        len_1=len(data7_4)
        for i in range(0, len_1 - 2 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JGZS_QiangShiGu_model(data7_4[i:i + 2], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)

if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_JGZS_QiangShiGu(localpath1)
    # test_isAn_JGZS_KanZhangZuoZhang_laoshi() #测试老师的案例
    # test_isAn_JGZS_KanZhangZuoZhang_ziji()
    # test_Befor_data()
    # jisuan_all_shouyilv(chengongs, modelname, 1.03)


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"