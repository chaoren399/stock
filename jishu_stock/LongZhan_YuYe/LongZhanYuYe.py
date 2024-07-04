#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
龙战于野
https://www.yuque.com/chaoren399/eozlgk/hafzse

第一步先判断 模型
 获取近 3 天的数据, 

第一天 涨停
第二天 大阴线
第三天, 阳线收盘价 高过阴线开盘价  

第二步 再判断是不是下跌趋势
获取 近 7 天的最低值, 并判断 是近 30 天的最低值, 思路 当前日期的近 7 天的最低点,  判断 半年的 最低点是不是 小于那个值
然后

案例 : 常山北明 000158  20210420

从之前的 10 个里边 成功可以做到 0.9

'''
chengongs=[]
modelname='龙战于野'
def get_all_LongZhanYuYe(localpath1):
    info1=  '--龙战于野 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:3]  # 前6行
        data6_1 = df.iloc[0:10]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_LongZhanYuYe_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
数据长度 6: 
'''
def isAn_LongZhanYuYe_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 25):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-3:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi=0
        # print1(data1)
        data2 = data[len_data - 3-22:len_data-3]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #是不是涨停板
        key_2=0; #次日大阴线
        key_3=0; #阳线收盘价 高过阴线开盘价

        key_4=1; #前 22 天不能出现涨停

        day2_open=0
        day3_close=0
        day2_shiti=0
        for index,row in data1.iterrows():
            if(index==0 and isZhangTingBan(row)==1):
                key_1=1
                zhisundian=row['open']
            if(key_1==1):
                if(index==1 and isYinXian(row)==1): #次日大阴线
                    day2_open = row['open']
                    day2_shiti=getShiTiDaXiao(row)
                    # print1(day2_shiti)
                    if(day2_shiti >2.9):
                        key_2=1
                if(index==2 and isYangXian(row)==1):
                    day3_close=row['close']
                    mairuriqi=row['trade_date']
                    if(day3_close > day2_open):
                        key_3=1
        # key_4 = 0;  # 前 22 天不能出现涨停
        for index,row in data2.iterrows():
            if(isZhangTingBan(row)==1):
                key_4=0
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(day2_shiti)
        # if(key_1==1 and  key_2 ==1and key_3==1 and key_4==1):
        if(key_1==1 and  key_2 ==1and key_3==1):
            info = ''
            info1= info+ '阴线实体大于3.6最好:'+str(day2_shiti)
            if(key_4==0):
                info1= info+ '--前边有涨停板--'

            info = info + "龙战于野--"  + str(riqi)
            # print info

            # 统一 info管理 一个函数,每次都要执行, 并且信息 返回后,要添加到 info中,
            # 方便后期修改,这样一改,所有的都可以执行了.
            from jishu_stock.z_tool.InfoTool import manage_info
            manage_info = manage_info(info, stockcode, riqi, '')
            info = info + manage_info


            writeLog_to_txt(info, stockcode)
            path = '龙战于野.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            chengongs.append(chenggong_code)



'''
测试老师的案例
'''
def test_isAn_LongZhanYuYe_laoshi():

    # 案例 1云鼎科技
    df1 = ts.pro_bar(ts_code='000409.SZ',adj='qfq', start_date='20210206', end_date='20210607')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_LongZhanYuYe_model(data7_1,'000409.SZ')

    # 案例 2 本钢板材
    df1 = ts.pro_bar(ts_code='000761.SZ',adj='qfq', start_date='20210206', end_date='20210412')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_LongZhanYuYe_model(data7_1,'000761.SZ')

    # 案例 3常山北明

    df1 = ts.pro_bar(ts_code='000158.SZ',adj='qfq', start_date='20210206', end_date='20210422')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_LongZhanYuYe_model(data7_1,'000158.SZ')

    # 案例 4 广晟有色

    df1 = ts.pro_bar(ts_code='600259.SH',adj='qfq', start_date='20200206', end_date='20210120')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_LongZhanYuYe_model(data7_1,'600259.SH')

'''
测试自己的案例
'''
def test_isAn_LongZhanYuYe_ziji():

    #自己的 案例
    df1 = ts.pro_bar(ts_code='603335.SH',adj='qfq', start_date='20210206', end_date='20211108')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_LongZhanYuYe_model(data7_1,'603335.Sh')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        # data7_4 = df.iloc[22:42]  # 前10个交易日
        data7_4 = df.iloc[1:72]  # 前10个交易日
        # data7_4 = df.iloc[1:22+250]  # 1年的数据
        len_1=len(data7_4)
        n=0
        isAn_LongZhanYuYe_model(data7_4[n:n+ 30], stock_code)
        #
        # for i in range(0, len_1 - 6 + 1):
        #     # print "i" + str(i )+ "j"+str(i+3)
        #     isAn_LongZhanYuYe_model(data7_4[i:i + 26], stock_code)


if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_LongZhanYuYe(localpath1)
    # test_Befor_data()
    # test_isAn_LongZhanYuYe_laoshi()
    # test_isAn_LongZhanYuYe_ziji()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"