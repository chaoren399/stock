#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''

神龙摆尾

1# 找到 涨停板
605277      新亚电子      这是个成功的神1  为什么程序没跑出来, 所以我要改进我的 程序

Shen1
思路: 循环40 天的数组, 找到涨停板, 然后 从涨停板 截取后边的数据,  必须大于 7 天, 然后最后一天必须是放量突破,
在找到最后 6 天的数据, 判断是还不是在箱体内运行.
'''
chengongs=[]
modelname='神1'
def get_all_Shen1(localpath1):
    info1=  '--神 1  start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:62]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_Shen1_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_Shen1_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 62):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。
        # print data
        data1= data[len_data-40:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        lendata1=len(data1)
        riqi = data1.ix[lendata1-1]['trade_date']  # 阳线的日期
        zhangtingban_riqi=0
        mairuriqi=0
        zhisundian=0
        # print1(data1)

        data3 = data[len_data - 40 - 22 :len_data - 40 ]
        data3 = data3.reset_index(drop=True)  # 重新建立索引 ,

        #思路: 循环40 天的数组, 找到涨停板, 然后 从涨停板 截取后边的数据,  必须大于 7 天, 然后最后一天必须是放量突破,
        #在找到最后 6 天的数据, 判断是还不是在箱体内运行.

        # 设置两个 key
        key_1=0; #1, 最新一天 阳线
        key_2=0; #1, 最新一天放量突破
        key_3=1;#2, 6 天的数据在箱体内运行.
        key_4=1;#3, 所有数据 收盘价和开盘价 不能低于 涨停板的 开盘价

        key_6 = 1;  # 前 20 个交易日 不能有涨停板

        #1 找到涨停板 以后的数据

        count=0
        zhangtingban_open_price=0
        zhangtingban_close_price=0
        zhangtingban_riqi=0
        for index,row in data1.iterrows():
            count=count+1
            if(isZhangTingBan(row)==1): # 涨停板
                zhangtingban_open_price=row['open']
                zhangtingban_close_price=row['close']
                zhangtingban_riqi=row['trade_date']
                zhisundian=zhangtingban_open_price
                break


        lendata1=len(data1)
        # print1(lendata1)
        data2=data1[count:lendata1]  # 涨停板后的数据
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,
        # print1(data2)



        lendata2 = len(data2)  # lendata2 必须大于 5 天的数据

        if(lendata2 > 5):

            #2 遍历 涨停板之后的数据 , 分为 2 部分数据,
            # (1)最后一个阳线放量,
            # (2)倒数第2到 到 6 天的数据
            # (3)倒数第6到 涨停板的数据, 不能跌破涨停板开盘价

            data2_1=data2[lendata2-2:lendata2] # 倒数 2 个数据(1)最后一个阳线放量,
            data2_1 = data2_1.reset_index(drop=True)  # 重新建立索引 ,
            # print1(data2_1)

            # 2022年03月12日  皖通科技**002331.SZ 更改为  6 变为 4 ,后期可以考虑更改
            data2_2=data2[lendata2-4:lendata2-1] #  (2)倒数第2到 到 6 天的数据
            data2_2 = data2_2.reset_index(drop=False)  # 重新建立索引 ,
            # print data2_2
            data2_3=data2[0:lendata2-4] #(3)倒数第6到 涨停板的数据, 不能跌破涨停板开盘价
            data2_3 = data2_3.reset_index(drop=False)  # 重新建立索引 ,

            # 1, 最新一天放量突破

            day1_amount_data2_1=0
            day2_amount_data2_1=0
            for index ,row in data2_1.iterrows():
                if(index==0):
                    day1_amount_data2_1=row['amount']
                if(index==1):
                    mairuriqi=row['trade_date']
                    day2_amount_data2_1=row['amount']
                    if(isYangXian(row)==1 and row['close'] > zhangtingban_close_price):
                        key_1=1

            if(day2_amount_data2_1 > day1_amount_data2_1):
                key_2=1

            #2, 6 天的数据在箱体内运行.
            for index, row in data2_2.iterrows():
                open=row['open']
                close=row['close']
                if(open > zhangtingban_close_price  or close > zhangtingban_close_price or open <zhangtingban_open_price or close <zhangtingban_open_price):
                    key_3=0

            # 3, 所有数据 收盘价和开盘价 不能低于 涨停板的 开盘价
            for index, row in data2_3.iterrows():
                open = row['open']
                close = row['close']
                if(open < zhangtingban_open_price or close < zhangtingban_open_price):
                    key_4=0
        #key_6=0; # 前 20 个交易日 不能有涨停板
        for index,row in data3.iterrows():
            if(isZhangTingBan(row)==1):
                key_6=0


        if(0):
            print1(key_1)
            print1(key_2)
            print1(key_3)
            print1(key_4)
            print1(zhangtingban_close_price)
            print1(zhangtingban_open_price)
            print1(zhangtingban_riqi)
            # print data2_3
        if(key_1==1 and  key_2 ==1 and key_3==1and key_4==1 and key_6==1):
        # if(key_1==1 and  key_2 ==1 and key_3==1and key_4==1):
        # if(key_1==1  and key_3==1and key_4==1):
            info = ''

            info = info + "神 1--"  +"涨停板日期:"+str(zhangtingban_riqi)+'--'+str(riqi)
            # print info
            # 统一 info管理 一个函数,每次都要执行, 并且信息 返回后,要添加到 info中,
            # 方便后期修改,这样一改,所有的都可以执行了.

            from jishu_stock.z_tool.InfoTool import manage_info
            manage_info = manage_info(info, stockcode, riqi, '')
            info = info + manage_info

            writeLog_to_txt(info, stockcode)
            path = '神1.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
            chengongs.append(chenggong_code)


'''
测试老师的案例 5个 
https://xueqiu.com/3476656801/206376922

'''
def test_isAn_Shen1_laoshi():
    # 测试案例 1 渤海租赁   一周的 K 线没有在箱体内运行
    df1 = ts.pro_bar(ts_code='000415.SZ', adj='qfq',start_date='20190403', end_date='20210723')
    data7_1 = df1.iloc[0:62]  # 前4行
    isAn_Shen1_model(data7_1, '000415.SZ')
    # 测试案例 2 大立科技
    df2 = ts.pro_bar(ts_code='002214.SZ', start_date='20190403', end_date='20210723')
    data7_2 = df2.iloc[0:62]  # 前4行
    isAn_Shen1_model(data7_2, '002214.SZ')
    # 测试案例 3 飞亚达
    df3 = ts.pro_bar(ts_code='000026.SZ', start_date='20190403', end_date='20200616')
    data7_3 = df3.iloc[0:62]  # 前4行
    isAn_Shen1_model(data7_3, '000026.SZ')
    # 复杂盘面  1 000038深大通
    df5 = ts.pro_bar(ts_code='000038.SZ', start_date='20190403', end_date='20200403')
    data7_5 = df5.iloc[0:62]  # 前4行
    isAn_Shen1_model(data7_5, '000038.SZ')
    # 复杂盘面  2  000400 许继电气, 20191118 以后买入 但是 有一个破了箱体 所以程序跑不出来,
    # 然后但是 如果我每天测试一次, 就可以 在 2019 1113 可以检测出来,所以程序非常好
    df6 = ts.pro_bar(ts_code='000400.SZ', start_date='20190403', end_date='20191113')
    data7_6 = df6.iloc[0:62]  # 前4行
    isAn_Shen1_model(data7_6, '000400.SZ')

def testlinshi():
    df1 = ts.pro_bar(ts_code='000415.SZ', adj='qfq',start_date='20190403', end_date='20210723')
    data7_1 = df1.iloc[0:62]  # 前4行
    isAn_Shen1_model(data7_1, '000415.SZ')

       # -中间值=8.23--大于7个--换手率=80.3--流通市值=32.0亿--皖通科技**002331.SZ  神1 5 天改为 4天
    df1 = ts.pro_bar(ts_code='002331.SZ', adj='qfq',start_date='20190403', end_date='20220312')
    data7_1 = df1.iloc[0:62]  # 前4行
    isAn_Shen1_model(data7_1, '002331.SZ')
'''
测试学员朋友找到的案例
'''
def test_xueyuan():
    #605277      新亚电子    成功
    # 这是个成功的神1  为什么程序没跑出来, 所以我要改进我的 程序
    #神1	600337	美克家居	2021年12月23日

    df4 = ts.pro_bar(ts_code='600337.SH', start_date='20190403', end_date='20211221')
    data7_4 = df4.iloc[0:62]  # 前4行
    isAn_Shen1_model(data7_4, '600337.SH')

'''
测试自己的案例
'''
def test_isAn_DaYou_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:62]  # 前7行
    isAn_Shen1_model(data7_1,'002507.SZ')



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
        data7_4 = df.iloc[22:22+62+22]  # 前1个个月

        data7_4 = df.iloc[22*3:22*3+62+22]  # 前2个月
        # data7_4 = df.iloc[22:22+62+120]  # 半年
        # data7_4 = df.iloc[22:22+62+250]  # 前1年
        len_1=len(data7_4)
        for i in range(0, len_1 - 62 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_Shen1_model(data7_4[i:i + 62], stock_code)

    # jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.10)
    # jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    jisuan_all_shouyilv(chengongs, modelname, 1.30)

if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_Shen1(localpath1)
    # test_isAn_Shen1_laoshi()
    # test_Befor_data()
    # testlinshi()
    # test_xueyuan()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"