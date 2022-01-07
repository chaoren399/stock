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
价格中枢-看涨阴线2
https://www.yuque.com/chaoren399/eozlgk/zxf3g5


收盘价为最低价(或附近很近)的大阴线
开盘价在价格中枢上方.上影线不长
第2周收盘价在第1周中枢价之.上
前期有过一波涨幅
后期看涨50%+


注意 必须有上影线且不是很长，
下影线最好没有，不过没有的情况很少， 可以给个浮动值。

JGZS_KanZhangYinXian2

'''

def get_all_JGZS_KanZhangYinXian2(localpath1):
    info1=  '--价格中枢-看涨阴线2 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        # stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"

        df = pd.read_csv(stockdata_path, index_col=0)
        df = df.reset_index(drop=False)

        data6_1 = df.iloc[0:6]  # 前6行
        # data6_1 = df.iloc[2:8]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_JGZS_KanZhangYinXian2_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JGZS_KanZhangYinXian2_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >=2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        # print1 (data)

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        # 设置两个 key

        key_1=0; #收盘价为最低价, 或者相差不大
        key_2=0;  # 实体较大阴线
        key_3=0; #  开盘价在价格中枢上方
        key_4=0; # 上影线不长
        key_5=0; # 第 2 周收盘价在第一周价格中枢 之上.

        count=0
        week1_close=0
        week1_low=0
        week1_shiti=0
        week1_jiagezhongshu=0
        week1_open=0
        week1_high=0
        week1_shangyingxian=0
        week2_close=0
        for index,row in data1.iterrows():
            if(index==0 and isYinXian(row)==1):
                count=count+1
                week1_close=row['close']
                week1_low=row['low']
                week1_shiti=getShiTiDaXiao(row)
                week1_jiagezhongshu=round((row['high']+row['low'])/2,2)
                week1_open=row['open']
                week1_high=row['high']

            if(index==1 and isYangXian(row)==1):
                count=count+1
                week2_close=row['close']

        if(count==2): #满足一阳一阴 才继续

            #1 收盘价为最低价, 或者相差不大 下影线不能太长
            week1_xiayingxian= round(((week1_close-week1_low)/week1_close)*100,2)
            # print1(week1_xiayingxian)
            if(week1_xiayingxian <0.1):  #两个案例 0.07, 0,
            # if(week1_xiayingxian <0.2):  #两个案例 0.07, 0,
                key_1=1
            # 2  实体较大阴线
            if(week1_shiti>1.6):
                key_2=1
            #3 开盘价在价格中枢上方
            if(week1_open > week1_jiagezhongshu):
                key_3=1

            #4 上影线不长
            week1_shangyingxian = round(((week1_high-week1_open) / week1_open )*100,4)

            if(week1_shangyingxian < 1 and week1_shangyingxian>0 ): #
                key_4=1

            #5  第 2 周收盘价在第一周价格中枢 之上.

            if(week2_close > week1_jiagezhongshu):
                key_5=1






        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(week1_xiayingxian)
        # print1(week1_shangyingxian)



        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1and key_5==1 ):
            info = ''

            info=info+'上影线='+str(week1_shangyingxian)
            info=info+'--下影线最好为0='+str(week1_xiayingxian)
            info=info+'--实体大小='+str(week1_shiti)

            info = info + "--价格中枢看涨阴线2--"  + str(riqi)

            path = BASE_DIR + '/jishu_stock/sJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                '%Y-%m-%d') + '.txt'

            jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)

            path = '价格中枢看涨阴线2.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试老师的案例
'''
def test_isAn_JGZS_KanZhangYinXian2_laoshi():
    # 案例 1 先进数通 ， 300541
    df = ts.pro_bar(ts_code='300541.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20210210')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    isAn_JGZS_KanZhangYinXian2_model(data7_1, '300541.SZ')

    # 案例 2 ： 南玻A ,000012，20200430

    df = ts.pro_bar(ts_code='000012.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20200430')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    isAn_JGZS_KanZhangYinXian2_model(data7_1, '000012.SZ')






def test_bendi_shuju():
    stock_code = '000100.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    data7_1=df.loc['2020-05-03':'2020-04-12' ]
    print data7_1
    isAn_JGZS_KanZhangYinXian2_model(data7_1, '000100.SZ')
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
    isAn_JGZS_KanZhangYinXian1_model(data7_1, '603595.SH')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']

        # stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
            # print df
        if (df.empty):
            continue

        df = df.reset_index(drop=False)  # 重新建立索引 ,
        data7_4 = df.iloc[0:6]  # 1 年有 52 周
        data7_4 = df.iloc[8:12]  # 1 年有 52 周

        len_1=len(data7_4)
        for i in range(0, len_1 - 2 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JGZS_KanZhangYinXian2_model(data7_4[i:i + 2], stock_code)





if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_JGZS_KanZhangYinXian2(localpath1)
    # test_isAn_JGZS_KanZhangYinXian2_laoshi()  #
    # test_ziaxian_zhuan_Week()
    # test_isAn_JGZS_KanZhangYinXian2_ziji()
    test_Befor_data()