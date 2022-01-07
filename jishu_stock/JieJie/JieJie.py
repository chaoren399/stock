#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
结界
https://www.yuque.com/chaoren399/eozlgk/kyqslp

结界均成
价格在[75日均线]之. 上运行
且均线方向向上
K线下跌到均线附近
形成 [壁]
JieJie
'''
chengongs=[]
modelname='结界'
def get_all_JieJie(localpath1):
    info1=  '--结界 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:5]  # 前6行
        data6_1 = df.iloc[1:6]  #  找前一天那出现 结界的, 今天出现阳线的明天可以买入
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_JieJie_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JieJie_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 5):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=False)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-1:len_data]
        data1 = data1.reset_index(drop=False)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)
        mairuriqi = 0
        zhisundian = 0

        data2 = data[len_data-1-4:len_data-1]
        data2 = data2.reset_index(drop=False)  # 重新建立索引 ,
        # print1(data2)

        # 设置两个 key
        key_1=0; # 1下影线 穿过 75 日均线
        key_2=1;#2 其他的 开盘价 和收盘价 都在 75 日以上
        key_3=0; #3 75 日均线必须向上

        day1_yingxian_shang=0
        day1_yingxian_xia=0
        day1_75=0

        for index,row in data1.iterrows():
            if(index==0):
                day1_yingxian_xia= row['low']
                day1_75=row['ma75']
                mairuriqi=row['trade_date']
                zhisundian=row['low']
                #r如果是阳线
                if(isYangXian(row)==1):
                    day1_yingxian_shang = row['open']
                #如果是阴线
                if(isYinXian(row)==1):
                    day1_yingxian_shang=row['close']
        # 1下影线 穿过 75 日均线

        if(day1_yingxian_shang >day1_75 and day1_yingxian_xia < day1_75 ):
            key_1=1

        if(key_1==1):
            #2 其他的 开盘价 和收盘价 都在 75 日以上

            ma75s=[]
            for index, row in data2.iterrows():
                ma75=row['ma75']
                ma75s.append(ma75)
                open_price= row['open']
                close_price= row['close']
                low_price=row['low']
                # if(open_price < ma75 or close_price < ma75):
                #     key_2=0
                if(low_price  < ma75):
                    key_2=0

            # 3 75 日均线必须向上
            if(is_small_to_big(ma75s)==1):
                key_3=1
            # print1(ma75s)


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(day1_yingxian_shang)
        # print1(day1_yingxian_xia)


        if(key_1==1 and  key_2 ==1 and key_3==1):
            info = ''

            info = info + "---结界--"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '结界.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_JieJie_laoshi():
    # 案例 1 捷成股份 300182
    df1 = ts.pro_bar(ts_code='300182.SZ',adj='qfq', start_date='20200206', end_date='20210517', ma=[75])
    data7_1 = df1.iloc[0:5]  # 前7行
    isAn_JieJie_model(data7_1,'300182.SZ')

    # 案例 2 不满足
    df1 = ts.pro_bar(ts_code='600252.SH',adj='qfq', start_date='20200206', end_date='20210615', ma=[75])
    data7_1 = df1.iloc[0:5]  # 前7行
    isAn_JieJie_model(data7_1,'600252.SH')

    # 案例 3羚锐制药**600285.SH
    df1 = ts.pro_bar(ts_code='600285.SH',adj='qfq', start_date='20200206', end_date='20210427', ma=[75])
    data7_1 = df1.iloc[0:5]  # 前7行
    isAn_JieJie_model(data7_1,'600285.SH')
    #案例 4 东方盛虹--强势股票**000301.SZ
    df1 = ts.pro_bar(ts_code='000301.SZ',adj='qfq', start_date='20200206', end_date='20210621', ma=[75])
    data7_1 = df1.iloc[0:5]  # 前7行
    isAn_JieJie_model(data7_1,'000301.SZ')


'''
测试自己的案例
'''
def test_isAn_JieJie_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_JieJie_model(data7_1,'002507.SZ')

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
        data7_4 = df.iloc[22:29]  # 前10个交易日
        data7_4 = df.iloc[22:22+5+22]  # 前1 个月的
        len_1=len(data7_4)
        for i in range(0, len_1 - 5 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JieJie_model(data7_4[i:i + 5], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    jisuan_all_shouyilv(chengongs, modelname, 1.30)

if __name__ == '__main__':

    from  time import  *
    starttime = time()
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_JieJie(localpath1)

    test_Befor_data()
    # test_isAn_JieJie_laoshi()

    jisuan_all_shouyilv(chengongs, modelname, 1.10)


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"