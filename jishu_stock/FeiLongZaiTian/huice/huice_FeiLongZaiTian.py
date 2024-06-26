#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
from jishu_stock.z_tool.ShiTiDaXiao import  getShiTiDaXiao
''''
飞龙在天, 超短线
https://www.yuque.com/chaoren399/eozlgk/gyht6e


1. 涨停板
2. 次日 小 K 线, 跳空高开缺口
3. 小 K 线成交量放大
4.之后阳线 收盘价高过小 K 线实体

思路, 找到  3 个数据,  先判断是不是涨停板, 然后再判断是不是 小 K , 

再判断是不是跳空 ,  
再判断 小 K 线成交量放大

再判断 阳线 收盘价高过小 K 线实体

'''
chengongs=[]
modelname='飞龙在天'
def get_all_FeiLongZaiTian(localpath1):
    info1=  '--飞龙在天, 超短线 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行
        len1 = len(data6_1)
        isAn_FeiLongZaiTian_model(data6_1, stock_code)

'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_FeiLongZaiTian_model(data,stockcode):
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
        mairuriqi=0
        zhisundian=0

        # 设置两个 key
        key_1=0; # 先判断是不是涨停板,
        key_2=0# 然后再判断是不是 小 K ,
        key_3=0; #再判断是不是跳空 ,
        key_4=0 #小 K 线成交量放大
        key_5=0;#再判断 阳线 收盘价高过小 K 线实体

        key_6=0;#连续涨停 或者 1 字板不做

        day2_open=0
        day2_close=0
        day3_close=0
        day1_high=0
        day2_low=0
        xiao_K_shiti=0
        count=0
        for index, row in data1.iterrows():
            if(isZhangTingBan(row)==1):
                count=count+1 # 排除 3 个连续涨停板
            if(index==0 and isZhangTingBan(row)==1): #先判断是不是涨停板
                key_1=1
                day1_high=row['high']
                day1_amount=row['vol']
                zhisundian=row['close']
                riqi=row['trade_date']

            if(key_1==1):  #
                if(index==1): #判断是不是 小 K
                    xiao_K_shiti = getShiTiDaXiao(row)
                    if(xiao_K_shiti < 1): # 0.9 是所有案例都满足的, 我可以放到 1. 5
                        key_2=1
                    day2_open=row['open']
                    day2_close=row['close']
                    day2_low=row['low']
                    if(day2_low > day1_high):#再判断是不是跳空 ,
                        key_3=1
                    day2_amount=row['vol']
                    if(day2_amount > day1_amount): #小 K 线成交量放大
                        key_4=1

                    if (isZhangTingBan(row)==1):
                        key_6=key_6+1

                if(index==2  and isYangXian_FeiLongZaiTian(row)==1) : # 阳线 收盘价高过小 K 线实体
                    day3_close=row['close']
                    mairuriqi=row['trade_date']

                    if (isZhangTingBan(row) == 1):
                        key_6 = key_6 + 1
                if(day3_close > day2_open and day3_close > day2_close):
                    key_5=1
                        # print1(day3_close)
                        # print1(day2_close)
                        # print1(day2_open)

                #      key_6=0;#连续涨停 或者 1 字板不做 key_6!=2

        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(xiao_K_shiti)


        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1 and key_6!=2 ):
        # if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1  ):
            info = ''
            info=info+'xiao_K_shiti='+str(xiao_K_shiti)

            info = info + "-----飞龙在天, 超短线  ----" + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '飞龙在天.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            chengongs.append(chenggong_code)



'''
飞龙在天专用,  一字板 开盘价 == 收盘价的也算是阳线
判断一行是不是 阳线, 返回 1 是阳线, 返回0 是阴线
'''
def isYangXian_FeiLongZaiTian(row):
    # print row['open']
    # print row['close']
    # print len(row)
    if(len(row) > 0):
        # print'-----'
        if(row['open'] < row['close'] or row['open'] ==row['close']):
            # print row['open']
            return 1
        # if(row['open'] == row['close']):
        #     return 2 # 不阴不阳
    return 0

'''
测试老师的案例
'''
def test_isAn_FeiLongZaiTian_laoshi():

    # 案例 1 000883.SZ ----20210324--湖北能源
    df1 = ts.pro_bar(ts_code='000883.SZ',adj='qfq', start_date='20210206', end_date='20210326')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_FeiLongZaiTian_model(data7_1,'000883.SZ')

    # 案例 2 600744.SH ----20210312--华银电力 #连续的涨停板或者一字板不要做.
    df1 = ts.pro_bar(ts_code='600744.SH',adj='qfq', start_date='20210206', end_date='20210316')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_FeiLongZaiTian_model(data7_1,'600744.SH')

    # 案例 3  600569.SH ----20210407--安阳钢铁#连续的涨停板或者一字板不要做.
    df1 = ts.pro_bar(ts_code='600569.SH',adj='qfq', start_date='20210206', end_date='20210409')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_FeiLongZaiTian_model(data7_1,'600569.SH')


    # 案例 4 飞龙在天, 超短线  ----603080.SH ----20210326--新疆火炬- #连续的涨停板或者一字板不要做.
    df1 = ts.pro_bar(ts_code='603080.SH',adj='qfq', start_date='20210206', end_date='20210330')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_FeiLongZaiTian_model(data7_1,'603080.SH')

'''
测试自己的案例
'''
def test_isAn_FeiLongZaiTian_ziji():
    #xiao_K_shiti=1.92-----飞龙在天, 超短线  ----002468.SZ ----20211019--申通快递--强势股票


    #自己的 案例
    df1 = ts.pro_bar(ts_code='002354.SZ',adj='qfq', start_date='20210206', end_date='20211110')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_FeiLongZaiTian_model(data7_1,'002354.SZ')

def test_xueyuan_anli():

    #案例 xiao_K_shiti=1.44-----飞龙在天, 超短线  ----002234.SZ ----20211019--民和股份
    df1 = ts.pro_bar(ts_code='002270.SZ', adj='qfq', start_date='20210206', end_date='20211121')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_FeiLongZaiTian_model(data7_1, '002270.SZ')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        data7_4 = df.iloc[22:42]  # 前10个交易日
        data7_4 = df.iloc[0:22]  # 前10个交易日
        data7_4 = df.iloc[22:22+3+10]  # 1 个月
        # data7_4 = df.iloc[22:22+3+22]  # 1 个月
        len_1=len(data7_4)
        for i in range(0, len_1 - 3 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_FeiLongZaiTian_model(data7_4[i:i + 3], stock_code)

    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    # jisuan_all_shouyilv(chengongs, modelname, 1.30)

if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # test_isAn_FeiLongZaiTian_laoshi()
    # get_all_FeiLongZaiTian(localpath1)
    test_Befor_data()
    # test_isAn_FeiLongZaiTian_ziji()
    # test_xueyuan_anli()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"