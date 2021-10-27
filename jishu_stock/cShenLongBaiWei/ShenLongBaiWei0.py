#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from stock.settings import BASE_DIR
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
神龙摆尾 0
https://www.yuque.com/chaoren399/eozlgk/ez5zh7

急速下跌熊市末期
(连续3根或以上阴线伴随着低开和大阴线)
小十字星
第2日阴线创新低
第3夭阳线收盘价高过第2日阴线收盘价
以亢龙有悔的方法结算和止损

思路 ,
找到 4 个数据, 满足 第一个是阴线, 第 2 个是十字星, 第 3 个是 阴线,并且是最低点, 第 4 个是 收高的阳线.

然后肉眼判断趋势.

   #  小十字星 判断条件改为收盘价 是不是等于开盘价, 如果是,那么才可以, 这样条件就比较严谨了.


'''

def get_all_isShenLongBaiWei0(localpath1):
    info1=  '-神龙摆尾 0 start  https://xueqiu.com/3476656801/201062781   ----  '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:136]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ShenLongBaiWei0_model(data6_1, stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ShenLongBaiWei0_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-3:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        data2=data[0:len_data-3]

        # 设置两个 key
        key_1=0; #  小十字星
        key_2=0; #第2日阴线
        key_3=0; # 第3夭阳线收盘价高过第2日阴线收盘价

        key_4=1 ; # 第2日阴线  创新低 单独判断

        day2_close=0
        day3_close=0
        day2_low=0
        shizixing_daxiao=0
        for index,row in data1.iterrows():

            if(index==0):
                shizixing_daxiao = getShiTiDaXiao(row)
                # if( shizixing_daxiao < 0.51):
                if( shizixing_daxiao < 0.1):
                    key_1=1


            if(index==1 and isYinXian(row)==1):
                key_2=1
                day2_close=row['close']
                day2_low=row['low']
            if(index==2 and isYangXian(row)==1):

                day3_close=row['close']
                if(day3_close > day2_close):
                    key_3 = 1

      # 第2日阴线  创新低 单独判断
        if(key_1==1):
            for index, row in data2.iterrows():
                if(row['low'] < day2_low):
                    key_4=0


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(shizixing_daxiao)
        # print1(riqi)
        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1):
            info = ''
            info=info+'shizixing_daxiao='+str(shizixing_daxiao)
            info = info + "-----神0 ----"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '神0.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例

小十字星  小于 0.9 的 老师案例都满足.

'''
def test_isAn_ShenLongBaiWei2_laoshi():
    # 下边的 3 个是小十字星
    # 案例 3 东旭光电

    df1 = ts.pro_bar(ts_code='000413.SZ', adj='qfq', start_date='20200101', end_date='20210209')  # 十字星
    data7_1 = df1.iloc[0:136]  # 前7行
    isAn_ShenLongBaiWei0_model(data7_1, '000413.SZ')

    # 案例 4太龙药业

    df1 = ts.pro_bar(ts_code='600222.SH', adj='qfq', start_date='20200101', end_date='20210114')  # 十字星
    data7_1 = df1.iloc[0:136]  # 前7行
    isAn_ShenLongBaiWei0_model(data7_1, '600222.SH')

    # 案例 5香江控股

    df1 = ts.pro_bar(ts_code='600162.SH', adj='qfq', start_date='20200101', end_date='20210205')  # 十字星
    data7_1 = df1.iloc[0:136]  # 前7行
    isAn_ShenLongBaiWei0_model(data7_1, '600162.SH')

     # 下边 2 个 十字星实体有点大
    # 案例 1
    df1 = ts.pro_bar(ts_code='000066.SZ', adj='qfq', start_date='20200101', end_date='20210510')
    df1 = ts.pro_bar(ts_code='000066.SZ',  start_date='20200101', end_date='20210510')
    data7_1 = df1.iloc[0:136]  # 前7行
    # print data7_1
    isAn_ShenLongBaiWei0_model(data7_1,'000066.SZ')

    # 案例 2
    df1 = ts.pro_bar(ts_code='000031.SZ', adj='qfq', start_date='20210101', end_date='20210205')
    data7_1 = df1.iloc[0:136]  # 前7行
    isAn_ShenLongBaiWei0_model(data7_1,'000031.SZ')





'''
测试自己的案例
'''
def test_isAn_ShenLongBaiWei0_ziji():

    #自己的 案例
    df1 = ts.pro_bar(ts_code='600466.SH', adj='qfq', start_date='20200101', end_date='20211018')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_ShenLongBaiWei0_model(data7_1,'600466.SH')

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

        for i in range(0, len_1 - 3 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ShenLongBaiWei0_model(data7_4[i:i + 3], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # test_isAn_ShenLongBaiWei2_laoshi()
    # test_isAn_ShenLongBaiWei0_ziji()

    get_all_isShenLongBaiWei0(localpath1)