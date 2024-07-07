#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''

涨停板-阴线

3-涨停板+大阴线-凯中精密

https://www.yuque.com/chaoren399/zxadsn/vdn7zgqgilq0roys


-涨停板+大阴线-凯中精密

'''
chengongs=[]
modelname='涨停后阴线'



def get_all_ZTB_Yin(localpath1):
    info1=  '--涨停板+大阴线-start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ZTB_Yin_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ZTB_Yin_model(data, stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        data2= data[len_data-2-1:len_data-2]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #1-昨天 是一个涨停板,

        key_2=0; # 2阴线 底开的打阴线


        count=0

        day1_close=0
        day2_open=0

        for index,row in data1.iterrows():
            if(index==0 and isZhangTingBan(row)==1):
                count=count+1
                day1_close=row['close']
                key_1=1


            if(index==1 and isYinXian(row)==1):
                count=count+1
                day2_open= row['open']

        if(count==2):
            if(day2_open < day1_close):
                key_2 = 1

        if(0):

           print "key_1=" + str(key_2)
           print "key_1=" + str(key_2)
        # print1(key_1)

        if(key_1==1 and key_2==1 ):
            info = ''
            info = info + "--涨停后低开阴线 成功了"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = modelname+'.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            # print1(day2_shizixing_low)
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_ZTB_Yin_laoshi():
    # 案例 1
    df1 = ts.pro_bar(ts_code='000408.SZ',adj='qfq', start_date='20210206', end_date='20210518')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_ZTB_Yin_model(data7_1, '002174.SZ')

    # 案例 2

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_ZTB_Yin_ziji():
    #自己的 案例 凯中精密
    ts_code='002823.SZ'
    df1 = ts.pro_bar(ts_code=ts_code,adj='qfq', start_date='20210206', end_date='20240628')
    # print df1
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_ZTB_Yin_model(data7_1,ts_code)

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        try:
            df = pd.read_csv(stockdata_path, index_col=0)
            n=14

            # data7_4 = df.iloc[22:22+n+22]  #1 个月
            # data7_4 = df.iloc[22:22+n+120]  # 半年
            # data7_4 = df.iloc[22:22+132+250]  # 1年
            data7_4 = df.iloc[n:n+3]  # 1年
            isAn_ZTB_Yin_model(data7_4, stock_code)

            len_1=len(data7_4)
            # for i in range(0, len_1 - n + 1):
            #     # print "i" + str(i )+ "j"+str(i+3)
            #     isAn_ZTB_Yin_model(data7_4[i:i + n], stock_code)
        except Exception as e:
            # `e` has the error info
            print `e`
            continue



if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_ZTB_ZTB_TiaoKong(localpath1)
    # test_isAn_ZTB_Yin_ziji()
    test_Befor_data()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"