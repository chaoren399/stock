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
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
鱼跃龙门1

找到 , 第一个月是阳线, 第 2 个月跳空 阳线的
YuYueLongMen1
'''
chengongs=[]
modelname='鱼跃龙门1'

def get_all_YuYueLongMen1(localpath1):
    info1=  '--鱼跃龙门1 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'

    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    if (len(data) > 0):

        for index, row in data.iterrows():
            stock_code = row['ts_code']
            stockdata_path = BASE_DIR + '/jishu_stock/stockdata/MONTH_DATA_K/' + stock_code + '_Month' + ".csv"
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                continue
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df

            df = df.iloc[0:20]  # 前10个交易日
            isAn_YuYueLongMen1_model(df, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YuYueLongMen1_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        # riqi = data1.ix[0]['trade_date']  # 阳线的日期
        riqi = 0
        # print1(data1)

        # 设置两个 key
        key_1=0; # 跳空

        count=0
        month1_close=0
        month2_open=0
        for index,row in data1.iterrows():
            if(index==0  and isYangXian(row)==1):
                count=count+1
                month1_close=row['close']
                month1_high=row['high']

            if(index==1 and isYangXian(row)==1):
                count = count + 1
                month2_open = row['open']
                month2_low = row['low']

        if(count==2):
            if(month2_open > month1_close):
            # if(month2_low > month1_high):
                key_1=1


        # print1(key_1)
        if(key_1==1 ):
            info = ''+stockcode

            info = info + "-----鱼跃龙门1 成功了"  + str(riqi)

            path = BASE_DIR + '/jishu_stock/zJieGuo/YuYueLongM/' + 'Yu' + datetime.datetime.now().strftime(
                '%Y-%m-%d') + '.txt'
            if (isInQiangShi_gupiaochi(stockcode)):
                info = info + '--强势股票--'
            info = info + '--' + get_Stock_Name(stockcode)
            print info
            with open(path, "a") as f:
                f.write(info + '' + "\n")

            path = '鱼跃龙门.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试老师的案例
'''
def test_isAn_YuYueLongMen1_laoshi():
    # 案例 1
    df1 = ts.pro_bar(ts_code='000408.SZ',adj='qfq', start_date='20210206', end_date='20210518')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_YuYueLongMen1_model(data7_1,'002174.SZ')

    # 案例 2

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_YuYueLongMen1_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_YuYueLongMen1_model(data7_1,'002507.SZ')

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
        data7_4 = df.iloc[22:42]  # 前10个交易日
        len_1=len(data7_4)
        for i in range(0, len_1 - 3 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_YuYueLongMen1_model(data7_4[i:i + 3], stock_code)



if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_YuYueLongMen1(localpath1)


    endtime = time()
    print "总共运行时长:"+str(round((endtime - starttime) / 60 ,2))+"分钟"