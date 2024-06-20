#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import *
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
创建日期:2021年11月03日
更新日期:
价格中枢-看涨阴线1
https://www.yuque.com/chaoren399/eozlgk/zyxa53

价格中枢看涨阴线1:
实体较大阴线上下影线等长价格中枢在中间
上涨途中的回调(前期有过一波上涨)
第2周比第1周的中枢价低开高收
后期发力50%+

思路: 先找到 符合条件的阴线 
#经过观察, 10 周或者 60 周均线,必须有一个是上涨的. 

JGZS_KanZhangYinXian1

'''

def get_all_JGZS_KanZhangYinXian1(localpath1):
    info1=  '--价格中枢-看涨阴线1 start--   '
    writeLog_to_txt_nocode(info1)
    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST_xmind.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        # stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        try:
            df = pd.read_csv(stockdata_path, index_col=0)
            df = df.reset_index(drop=False)

            data6_1 = df.iloc[0:6]  # 前6行
            # data6_1 = df.iloc[2:8]  # 前6行
            # data6_1 = df.iloc[20:32]  # 前6行
            len1 = len(data6_1)
            isAn_JGZS_KanZhangYinXian1_model(data6_1, stock_code)
        except:
            print  'stock_code is null = ' + str(stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JGZS_KanZhangYinXian1_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 5):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        # print1 (data)

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        data2= data[len_data-2-2:len_data-2]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,
        # print1(data2)
        # 设置两个 key

        key_1=0; #上下影线等长
        key_2 = 0;  # 实体较大阴线
        key_3=0; # 第 2 周 阳线, 低开高收
        key_4=1; # 阶段性回调 思路, 阴线收盘价 是最低的

        key_5=0; #第一周价格中枢在中间



        count=0
        shangyingxian_daxiao=0
        xiayingxian_daxiao=0
        yinxian_jiagezhongshu=0  #价格中枢

        week2_open=0
        week2_close=0
        week1_shiti_daxiao=0
        week2_shiti_daxiao=0
        week1_open_close=0
        week1_close=0
        shangyingxian_xiayingxian=0
        shangyingxian_xiayingxian_beishu=0 # 上影线是下影线 的几倍
        for index,row in data1.iterrows():
            if(index==0 and isYinXian(row)==1):
                count=count+1
                shangyingxian_daxiao=row['high']-row['open']
                xiayingxian_daxiao=row['close']-row['low']
                yinxian_jiagezhongshu = round((row['high']+row['low']) /2 ,2)#价格中枢


                week1_shiti_daxiao= getShiTiDaXiao(row) # 阴线实体的大小
                week1_open_close=row['open']-row['close']
                week1_close=row['close']
            if(index==1 and isYangXian(row)==1):
                count=count+1
                week2_open=row['open']
                week2_close=row['close']
                week2_shiti_daxiao=getShiTiDaXiao(row)

        if(count==2): #一个阴线 一个阳线
            # 1上下影线等长
            xiayingxian_daxiao=xiayingxian_daxiao+0.00001 #防止 除数为 0
            shangyingxian_xiayingxian_beishu= round(shangyingxian_daxiao /xiayingxian_daxiao ,2)
            if(shangyingxian_xiayingxian_beishu <1.5 and shangyingxian_xiayingxian_beishu>0.5): #上下影线等长
                key_1=1

            # 2实体较大阴线
            shangyingxian_daxiao=shangyingxian_daxiao+0.00001
            shiti_yingxian_beishu= round(week1_open_close / shangyingxian_daxiao ,1)
            if( shiti_yingxian_beishu > 2):
                key_2=1

            #3 第 2 周 阳线, 低开高收
            if(week2_open < yinxian_jiagezhongshu and week2_close > yinxian_jiagezhongshu):

                key_3=1

        # 阶段性回调 思路, 阴线收盘价 是最低的
        if (key_1 == 1 and key_2 == 1 and key_3 == 1):

           for index,row in data2.iterrows():
               # print1(row['close'])
               if(row['close'] <  week1_close):
                   key_4=0


        if(0):
            print1(key_1)
            print1(key_2)
            print1(key_3)
            print1(key_4)
            print1(week1_close)
            # print1(shangyingxian_xiayingxian_beishu)

            # print1(yinxian_jiagezhongshu)
            # print1(shangyingxian_daxiao)
            # print1(week1_shiti_daxiao)
            # print1(week1_open_close)
            # print1(shiti_yingxian_beishu)

        if(stockcode=='000983.SZ'):
            print1(yinxian_jiagezhongshu)



        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 ):
            info = ''
            info = info + "--价格中枢看涨阴线1--" + str(riqi)

            info=info+'--实体是影线的'+str(shiti_yingxian_beishu)+'倍--'
            info=info+'--上下影线'+str(shangyingxian_xiayingxian_beishu)+'倍--'
            info=info+'--阴线实体大小'+str(week1_shiti_daxiao)
            info=info+'--阳线实体大小'+str(week2_shiti_daxiao)


            # print info
            # writeLog_to_txt(info, stockcode)

            path = BASE_DIR + '/jishu_stock/zJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                '%Y-%m-%d') + '.txt'

            jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)

            path = '价格中枢看涨阴线1.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试老师的案例
'''
def test_isAn_JGZS_KanZhangYinXian1_laoshi():
    # 案例 1 TCL科技**000100.SZ
    df = ts.pro_bar(ts_code='000100.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20200430')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    isAn_JGZS_KanZhangYinXian1_model(data7_1, '000100.SZ')

    # 案例 2 冀东水泥--强势股票**000401.SZ
    df = ts.pro_bar(ts_code='000401.SZ', adj='qfq', freq='W', start_date='20180101', end_date='20190111')
    # df = ts.pro_bar(ts_code='000401.SZ', freq='W', start_date='20180101', end_date='20190111')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    isAn_JGZS_KanZhangYinXian1_model(data7_1, '000401.SZ')





def test_bendi_shuju():
    stock_code = '000100.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    data7_1=df.loc['2020-05-03':'2020-04-12' ]
    print data7_1
    isAn_JGZS_KanZhangYinXian1_model(data7_1, '000100.SZ')
'''
测试自己的案例
'''
def test_isAn_JGZS_KanZhangYinXian1_ziji():
    #自己的 案例  ---价格中枢看涨阴线1--2021-10-17--雪峰科技--强势股票**603227.SH

    #不是回调状态----实体是影线的2.1--2021-10-17--东尼电子**603595.SH
    #----山西焦煤**000983.SZ

    df = ts.pro_bar(ts_code='603595.SH', adj='qfq', freq='W', start_date='20170101', end_date='20211022')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    # isAn_JGZS_KanZhangYinXian1_model(data7_1, '603595.SH')

    #水星家纺**603365.SH
    ts_code = '603365.SH'
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', freq='W', start_date='20170101', end_date='20240329')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    # isAn_JGZS_KanZhangYinXian1_model(data7_1, ts_code)

    ts_code = '600843.SH' #工申贝**600843.SH
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', freq='W', start_date='20170101', end_date='20240614')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    # isAn_JGZS_KanZhangYinXian1_model(data7_1, ts_code)

    ts_code = '601500.SH' #通用股份
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', freq='W', start_date='20170101', end_date='20240329')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    # isAn_JGZS_KanZhangYinXian1_model(data7_1, ts_code)

    ts_code = '000400.SZ' #通用股份
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', freq='W', start_date='20170101', end_date='20240208')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    # isAn_JGZS_KanZhangYinXian1_model(data7_1, ts_code)

    ts_code = '000791.SZ' #通用股份
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', freq='W', start_date='20170101', end_date='20240617')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    # isAn_JGZS_KanZhangYinXian1_model(data7_1, ts_code)

    ts_code = '002099.SZ' #海翔药业
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', freq='W', start_date='20170101', end_date='20240617')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    isAn_JGZS_KanZhangYinXian1_model(data7_1, ts_code)

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']

        # stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        try:
            df = pd.read_csv(stockdata_path, index_col=0)
            df = df.reset_index(drop=False)  # 重新建立索引 ,

            data7_4 = df.iloc[5:15]  # 前10个交易日
            len_1=len(data7_4)
            for i in range(0, len_1 - 5 + 1):
                # print "i" + str(i )+ "j"+str(i+3)
                isAn_JGZS_KanZhangYinXian1_model(data7_4[i:i + 5], stock_code)
        except:
            print  'stock_code is null = ' + str(stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_JGZS_KanZhangYinXian1(localpath1)
    # test_isAn_JGZS_KanZhangYinXian1_laoshi()  #
    # test_ziaxian_zhuan_Week()
    test_isAn_JGZS_KanZhangYinXian1_ziji()
    # test_Befor_data()