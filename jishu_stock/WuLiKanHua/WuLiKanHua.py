#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian, is_small_to_big, \
    writeLog_to_txt_path_getcodename, isYinXian
from jishu_stock.z_tool.PyDateTool import get_date1_date2_days
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from jishu_stock.z_tool.getMin_Max import getMin_fromDataFrame
from stock.settings import BASE_DIR
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
雾里看花
https://www.yuque.com/chaoren399/eozlgk/rhqy9u/

1. 较小的十字星 ,判断标准  实体小于 0.5 
2.次日阳线
3.阳线最高价 高于十字星最高价 ,收盘价高于十字星收盘价,阳线最低价 大于 十字星最低价


5日均线 明显上升 ,获取 5 天的数据

'''

def get_all_WuLiKanHua(localpath1):
    info1=  '--雾里看花, 特殊的十字星 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:132]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_WuLiKanHua_model(data6_1, stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_WuLiKanHua_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        data2 = data[0: len_data]
        data3=data[len_data-5:len_data]
        data3 = data3.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #较小的十字星 ,判断标准  实体小于 0.5 ,
        key_2=0;#次日阳线
        key_3=0;#阳线最高价 高于十字星最高价 ,收盘价高于十字星收盘价,阳线最低价 大于 十字星最低价

        key_4=0 ; # 与最低点的距离不能太大,可以小于 22 个交易日

        key_5=0; #5日均线 明显上升 ,获取 5 天的数据

        key_6=0; #6上下影线 相差不大

        day1_open =0
        day1_close =0
        day1_high = 0
        day1_low = 0
        day2_open =0
        day2_close =0
        day2_high = 0
        day2_low = 0

        yangxian_shiti=0
        day1_shangyingxian=0
        day1_xiayingxian=0
        shang_xia_yingxian=0
        for index,row in data1.iterrows():
            if(index==0 and getShiTiDaXiao(row) <0.5 ):
                key_1=1
                day1_open=row['open']
                day1_close=row['close']
                day1_high=row['high']
                day1_low=row['low']
                if(isYinXian(row)==1):#如果是十字星阳线
                    day1_shangyingxian=day1_high -day1_open
                    day1_xiayingxian= day1_close-day1_low
                else:
                    day1_shangyingxian=day1_high -day1_close
                    day1_xiayingxian= day1_open-day1_low


            if(key_1==1 and index==1 and isYangXian(row)==1):
                key_2=1
                day2_open=row['open']
                day2_close=row['close']
                day2_high=row['high']
                day2_low=row['low']
                yangxian_shiti=getShiTiDaXiao(row)

        count=0
        if(key_1==1 and key_2==1):
            #阳线最高价 高于十字星最高价 ,收盘价高于十字星收盘价,阳线最低价 大于 十字星最低价
            if( day2_high > day1_high):
                count=count+1
            if(day2_close > day1_close):
                count=count+1
            if(day2_low > day1_low):
                count=count+1
            if(count==3):
                key_3=1


            #与最低点的距离不能太大,可以小于 22 个交易日
            min_row = getMin_fromDataFrame(data2)
            if (min_row is None):
                print 'min_row  is None'

            min_row_riqi = min_row['trade_date']

            # print1(min_row_riqi)
            # print1(riqi)
            days_chazhi = get_date1_date2_days(min_row_riqi, riqi)  # 出水芙蓉与最低值相差几天
            # print days_chazhi
            if (int(days_chazhi) < 32 and int(days_chazhi) > 7):
                key_4 = 1

             # 5日均线 明显上升 ,获取 5 天的数据

            ma5s=[]
            for index, row in data3.iterrows():
                ma5=row['ma5']
                ma5s.append(ma5)

            if(is_small_to_big(ma5s)==1):
                key_5=1
            # 6上下影线 相差不大
            day1_xiayingxian=day1_xiayingxian+0.00001
            shang_xia_yingxian= round(day1_shangyingxian /day1_xiayingxian,2)
            # print1(day1_shangyingxian)
            # print1(day1_xiayingxian)


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(days_chahzi)
        # print1(shang_xia_yingxian)
        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1and key_5==1):

            info=''
            info = info+'阳线=' + str(yangxian_shiti)
            info = info+'--上下影线相差不大=' + str(shang_xia_yingxian)

            info =info + "-----雾里看花 ----"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '雾里看花.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例
'''
def test_isAn_WuLiKanHua_laoshi():

    # 案例 1
    df1 = ts.pro_bar(ts_code='600097.SH',adj='qfq', start_date='20210206', end_date='20210827',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:132]  # 前7行
    # print data7_1
    isAn_WuLiKanHua_model(data7_1,'600097.SH')

    # 案例 2
    df1 = ts.pro_bar(ts_code='300053.SZ',adj='qfq', start_date='20210206', end_date='20210527',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:132]  # 前7行
    # print data7_1
    isAn_WuLiKanHua_model(data7_1,'300053.SZ')

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_WuLiKanHua_ziji():

    #自己的 案例-阳线=3.36-----雾里看花 ----20211025--沪电股份**002463.SZ
    df1 = ts.pro_bar(ts_code='002463.SZ',adj='qfq', start_date='20210206', end_date='20211026')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_WuLiKanHua_model(data7_1,'002463.SZ')

def test_xueyuan_anli():
    df1 = ts.pro_bar(ts_code='603383.SH', adj='qfq', start_date='20210206', end_date='20211021',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:7]  # 前7行
    isAn_WuLiKanHua_model(data7_1, '603383.SH')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        data7_4 = df.iloc[22:42]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 2 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_WuLiKanHua_model(data7_4[i:i + 2], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_WuLiKanHua(localpath1)
    # test_isAn_WuLiKanHua_laoshi()
    # test_xueyuan_anli()
    # test_isAn_WuLiKanHua_ziji()