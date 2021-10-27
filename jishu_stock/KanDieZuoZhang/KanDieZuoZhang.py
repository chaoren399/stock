#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.PyDateTool import get_date1_date2_days
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from stock.settings import BASE_DIR
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
看跌做涨 上涨结构 抄底 尾盘买入
https://www.yuque.com/chaoren399/eozlgk/gnge86

急速下跌缓慢上涨
1根缩量大阴线吃掉近期N多小阳线
尾盘直接买入
大阴线不能近期创新低
以近期最低点做止损
思路 :

找近期 2 个数据, 看看有没有缩量的大阴线


创建时间 : 2021年10月19日
更新时间: 2021年10月20日

发现每天出现看跌做涨的有很多, 怎么用程序找出比较符合模型的呢? 
首先,
老师 3 个案例中 从大阴线 到最低点 没有超过 3 个月的 , 66 
1 . 拿到半年的数据, 判断最低点, 然后看看中间相差的天数, 不能超过 66 天, 

2 . 找到最低点 与 大阴线之间 计算 实体大小, 与大阴线比较



'''

def get_all_KanDieZuoZhang (localpath1):
    info1=  '--看跌做涨  start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:132]  # 半年数据
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_KanDieZuoZhang_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_KanDieZuoZhang_model(data,stockcode):
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

        data2=data[0: len_data-2]
        # print1(data2)

        # 设置两个 key
        key_1=0; #找近期 2 个数据, 看看有没有缩量的大阴线
        key_2=0; #大阴线

        key_3=0; #拿到半年的数据, 判断最低点, 然后看看中间相差的天数, 不能超过 66 天,
        key_4=1; #找到最低点 与 大阴线之间 计算 实体大小, 与大阴线比较

        key_5=0; #阴线前一天必须是阳线

        day1_amount=0
        day2_amount=0
        day2_shiti=0
        for index, row in data1.iterrows():
            if(index==0):
                day1_amount=row['amount']
                if(isYangXian(row)==1):
                    key_5=1
            if(index==1 and isYinXian(row)==1):
                day2_amount=row['amount']
                day2_shiti=getShiTiDaXiao(row)
                # if (day2_shiti > 3.6):
                if (day2_shiti > 3):
                    key_2 = 1

        if(day2_amount < day1_amount):
            key_1=1


        #拿到半年的数据, 判断最低点, 然后看看中间相差的天数, 不能超过 66 天,

        if (key_1 == 1 and key_2 == 1):
            day_low= data2.ix[0]['low']  # 阳线的日期
            day_low_riqi=data2.ix[0]['trade_date']

            for index, row in data2.iterrows():
                low= row['low']
                # print1(low)
                if(day_low >  low):
                    day_low=low
                    day_low_riqi=row['trade_date']
            # print1(day_low_riqi)
            # print1(riqi)
            # print1(day_low)

            xiangcha_tianshu= get_date1_date2_days(str(day_low_riqi),str(riqi))
            # print1(xiangcha_tianshu)
            if(xiangcha_tianshu < 90):
                key_3=1

          # 找到最低点 与 大阴线之间 计算 实体大小, 与大阴线比较

        # 因为上边是比较的日期 相差的天数, 但是实际上以交易日为主
        #所以先找到 最低点与 大阴线相差几个交易日,再获取数据.
        if (key_1 == 1 and key_2 == 1 and key_3==1):
            enddate= data2.ix[len(data2)-1]['trade_date']  #  大阴线之前2 天的日期
            data3 = ts.pro_bar(ts_code=stockcode, adj='qfq', start_date=str(day_low_riqi), end_date=str(enddate))

            yinxian_shiti=0
            for index, row in data3.iterrows():
                if(isYinXian(row)==1):
                    yinxian_shiti= getShiTiDaXiao(row)
                    if(yinxian_shiti > day2_shiti):
                        key_4=0
                        # print '-----------------'
                    # print1(yinxian_shiti)


            # print1(data3)

        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(day2_shiti)
        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1):
            info = ''
            info = info+ '-阴线实体='+str(day2_shiti)
            info = info + "-----看跌做涨 缩量大阴线  ----" + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '看跌做涨.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例
'''
def test_isAn_KanDieZuoZhang_laoshi():

    # 案例 1 吉林化纤
    df1 = ts.pro_bar(ts_code='000420.SZ',adj='qfq', start_date='20200206', end_date='20210302')
    data7_1 = df1.iloc[0:132]  # 前7行
    # print data7_1
    isAn_KanDieZuoZhang_model(data7_1,'000420.SZ')

    # 案例 2

    df1 = ts.pro_bar(ts_code='000040.SZ',adj='qfq', start_date='20200206', end_date='20210310')
    data7_1 = df1.iloc[0:132]  # 前7行
    # print data7_1
    isAn_KanDieZuoZhang_model(data7_1,'000040.SZ')
    # 案例 3

    df1 = ts.pro_bar(ts_code='600123.SH',adj='qfq', start_date='20200206', end_date='20210413')
    data7_1 = df1.iloc[0:132]  # 前7行
    # print data7_1
    isAn_KanDieZuoZhang_model(data7_1,'600123.SH')

def linshi():
    df1 = ts.pro_bar(ts_code='600123.SH', adj='qfq', start_date='20200206', end_date='20210413')
    data7_1 = df1.iloc[0:132]  # 前7行
    # print data7_1
    isAn_KanDieZuoZhang_model(data7_1, '600123.SH')


'''
测试自己的案例
'''
def test_isAn_KanDieZuoZhang_ziji():

    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:132]  # 前7行
    isAn_KanDieZuoZhang_model(data7_1,'002507.SZ')

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


        data7_4 = df.iloc[22:164]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 132 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_KanDieZuoZhang_model(data7_4[i:i + 132], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_KanDieZuoZhang(localpath1)
    # test_isAn_KanDieZuoZhang_laoshi()

    # linshi()
    # test_Befor_data()