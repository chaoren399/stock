#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd

from jishu_stock.JiaGeZhongShu.jiagezhognshu_Get_Week_K_data import getAll_jiagezhongshu_WeekKdata
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    jiagezhongshu_writeLog_to_txt_path_getcodename, writeLog_to_txt_path_getcodename, isShiZiXing
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
创建日期: 2024年6月13日
更新日期:
价格中枢-看涨做涨 -ShiZiXing
ShiZiXing


上涨初期或中期
实体较大有上下影线的阳线
实体的1/2恰好是中枢价
收盘价在中枢价之上
上下影线都不长且等长
第2周高开高走低开不能做
后期发力上攻
大阳线最低价止损

JGZS_KanZhangShiZiXing
'''

chengongs=[]
modelname='价格中枢-看涨ShiZiXing'

def get_all_JGZS_KanZhang_ShiZiXing(localpath1):
    info1=  '--上涨初期 价格中枢-看涨做涨 start-- '
    webhook.sendData( info1)
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
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
            isAn_JGZS_KanZhangShiZiXing_model(data6_1, stock_code)
        except:
            print  'stock_code is null = ' + str(stock_code)


'''
#2 单独一个函数 判断 2 个数据是不是符合模型
'''
def isAn_JGZS_KanZhangShiZiXing_model(data, stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

        data2= data[len_data-2-4:len_data-2]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # print1(data1)
        # print1(data2)
        riqi = data1.ix[0]['trade_date']  # 阳线的日期


        # 设置两个 key

        key_1=0;  #1实体的1/2恰好是中枢价
        key_2=0;  #
        key_3=0 # gao kai
        key_4=1 # hengpan

        week1_close=0
        week1_open=0
        week1_high=0
        week1_low=0
        week2_open =0
        week2_close =0

        # print '1111'

        for index, row in data1.iterrows():

            if(index==0 and isYangXian(row)==1):

                key_1=1
                week1_close=row['close']
                week1_open=row['open']
                week1_low=row['low']
                week1_high=row['high']

            if(index==1 and isShiZiXing(row) ):
                key_2=1
                week2_close=row['close']
                week2_open=row['open']

        for index, row in data2.iterrows():

            if(row['open'] > week1_high or row['close'] > week1_high) :
                key_4 = 0
            if(row['open'] > week1_low or row['close'] > week1_low) :
                key_4 = 0





        if(week1_close < week2_close and  week1_close < week2_open ) :
            key_3=1



        if(key_1==1 and key_2==1 and key_3==1 and key_4==1):

        #     print1(shangyingxian_xiayingxian)
            info = ''
            info = info + "--价格中枢看涨ShiZiXing--" + str(riqi)
            # info=info+'价格中枢-实体一半=' +str(week1_zhongshu_shitiyiban)
            # info=info+'--上影线是下的几倍=' +str(shangyingxian_xiayingxian)
            # info=info+'--阳线实体=' +str(week1_shiti)
            # info=info+'--实体是影线的几倍=' +str(shiti_yingxian_jibei)




            path = BASE_DIR + '/jishu_stock/zJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                '%Y-%m-%d') + '.txt'

            jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)

            path = '价格中枢看涨ShiZiXing.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例
'''
def test_isAn_JGZS_KanZhangShiZiXing_laoshi():


    # 案例  hengyuan mei dian
    ts_code = '600971.SH'
    # ts_code = '300215.SZ'
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', freq='W', start_date='20170101', end_date='20231117')
    data7_1 = df.iloc[0:10]  # 1 年有 50 周
    isAn_JGZS_KanZhangShiZiXing_model(data7_1, ts_code)
    # print data7_1



'''
测试自己的案例
'''
def test_isAn_JGZS_KanZhangShiZiXing_ziji():
    #自己的 案例
    #价格中枢-实体一半=0.04---上影线是下的几倍=1.33---阳线实体=7.26---实体看涨做涨--2021-10-31--维力医疗**603309.SH
    # df1 = ts.pro_bar(ts_code='603309.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    stock_code = '000812.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    df = df.reset_index(drop=False)  # 重新建立索引 ,
    data7_1 = df.iloc[0:8]  # 前7行
    isAn_JGZS_KanZhangShiZiXing_model(data7_1, '000812.SZ')




'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST_tmp1.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        # stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        try :
            df = pd.read_csv(stockdata_path, index_col=0)
                # print df
            if (df.empty):
                continue

            df = df.reset_index(drop=False)  # 重新建立索引 ,
            data7_4 = df.iloc[0:50]  # 1 年有 52 周
            # data7_4 = df.iloc[8:10]  # 1 年有 52 周
            # data7_4 = df.iloc[8:8+2+4]  # 上个与的

            len_1=len(data7_4)
            n = 6  # jian ge tian shu
            for i in range(0, len_1 - n + 1):
                # print "i" + str(i )+ "j"+str(i+3)
                isAn_JGZS_KanZhangShiZiXing_model(data7_4[i:i + n], stock_code)
        except:
            print  'stock_code is null = ' + str(stock_code)


if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_JGZS_KanZhang_ShiZiXing(localpath1)

    # test_isAn_JGZS_KanZhangShiZiXing_ziji()
    # test_isAn_JGZS_KanZhangShiZiXing_laoshi() #测试老师的案例
    test_Befor_data()



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"