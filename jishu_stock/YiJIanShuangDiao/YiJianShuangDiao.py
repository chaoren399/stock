#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1, \
    writeLog_to_txt_path_getcodename, isYinXian
from jishu_stock.z_tool.is5_13_34_ShangZhang import is5_13_34_XiangShang
from stock.settings import BASE_DIR

import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
''''
一箭双雕 主力中继洗盘模型  正课

https://www.yuque.com/chaoren399/eozlgk/xwhd4i



上涨结构初期或中期
第1天中阳线或大阳线后
第2、3天连续两个小实体阴线
阴线不能跌破阳线实体
第4天收阳线阳线收盘价高过前3天的所有实体上沿
以全部4天的最低价做止损
两个小阴线最好高开

思路 1

1. 先判断4 天数据是不是阳 阴 阴 阳 

2. 判断 第 4 天收盘价是不是高过前 3 天

3 . 2 个阴线不能跌破第一天的阳线实体.

4 . 两个小阴线最好高开


 复盘 8 月份 94% 的成功率
 
 2021年10月21日 更新 
 小阴线实体最好小于 1.6 , 成功概率会大, 联创电子 实体1.92 失败 
 
 
 
'''

def get_all_YiJianShuangDiao(localpath1):

    info1=  '--一箭双雕 主力中继洗盘模型 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:4]  # 前6行
        data6_1 = df.iloc[0:14]  # 前6行
        # data6_1 = df.iloc[3:17]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_YiJianShuangDiao_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YiJianShuangDiao_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    # print1(len_data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >=14):
        data1= data[4:len_data]
        data=data[0:4]
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,


        # print data
        riqi = data.ix[0]['trade_date']  # 阳线的日期

        # 设置两个 key
        key_1=0; #先判断4 天数据是不是阳 阴 阴 阳
        key_2=0;#判断 第 4 天收盘价是不是高过前 3 天
        key_3=0; #2 个阴线不能跌破第一天的阳线实体.
        key_4=0; # 两个小阴线最好高开  这种情况很少见

        key_5=0; # 大阴线和大阳线的波动范围在3.6以上。
        key_6=1; #  第一天阳线的收盘价 要高过之前 10 天的 数据, 这样是上涨行情
        key_7=0; # 判断是不是小阴线  小阴线和小阳线的波动范围一般在0.6--1.5

        key_8=0; # 5-13-34 需要上升趋势



        count =0
        day1_close=0
        day1_open=0

        day2_open=0
        day2_close=0
        day3_open = 0
        day3_close=0
        day4_close=0
        yangxian_shiti=0
        yinxian_shiti1=0
        yinxian_shiti2=0
        for index,row in data.iterrows():
            # print1(count)
            if(index==0 and isYangXian(row)==1): # 中阳线
                count=count+1

                day1_open=row['open']
                day1_close=row['close']
                yangxian_shiti = format(((row['close'] - row['open']) / row['open']) * 100, '.2f')  # (开盘价-收盘价)÷开盘价＜0.5%

            if(index==1 and isYinXian(row)==1): #小阴线
                count=count+1
                day2_open=row['open']
                day2_close=row['close']

                yinxian_shiti1 = format(((row['close'] - row['open']) / row['open']) * 100, '.2f')  # (开盘价-收盘价)÷开盘价＜0.5%

            if(index==2 and isYinXian(row)==1): #小阴线
                count=count+1
                day3_open = row['open']
                day3_close=row['close']
                yinxian_shiti2 = format(((row['close'] - row['open']) / row['open']) * 100, '.2f')  # (开盘价-收盘价)÷开盘价＜0.5%

            if(index==3 and isYangXian(row)==1):
                count=count+1
                day4_close = row['close']
        if(count==4):
            key_1=1
        if(key_1==1):

            #判断 第 4 天收盘价是不是高过前 3 天
            if(day4_close > day3_open and day4_close> day2_open and day4_close > day1_close):
                key_2=1

            # 3, 2 个阴线不能跌破第一天的阳线实体.

            if(day3_close > day1_open  and day2_close > day1_open):
                # print1(day3_close)
                key_3=1

            if(float(yangxian_shiti)> 1.6 ):

                key_5=1
            # 判断是不是小阴线  小阴线和小阳线的波动范围一般在0.6--1.5
            # print1(yinxian_shiti1)
            # print1(yinxian_shiti2)

            xiaoshiti_yinxian=1.6 # 小实体阴线 值为 2 老师的案例都成功
            # xiaoshiti_yinxian=2 # 小实体阴线 值为 2 老师的案例都成功
            if(abs(float(yinxian_shiti1)) <xiaoshiti_yinxian  and abs(float(yinxian_shiti2))<xiaoshiti_yinxian):
                if( abs(float(yinxian_shiti1)) > 0.1 and abs(float(yinxian_shiti2)) > 0.1):
                    key_7=1
                    # print1(key_7)


             # key_6 = 0;  第一天阳线的收盘价 要高过之前 10 天的 数据, 这样是上涨行情
            # print data1

            for index,row in data1.iterrows():
                if(day4_close < row['close'] or day4_close < row['open']):
                    key_6=0


        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_5)
        # print1(key_6)
        # print1(key_7)


        if(key_1==1 and  key_2 ==1  and key_3==1 and key_5==1 and key_6==1 and key_7==1 ):
            info=''

            #key_8=0; # 5-13-34 需要上升趋势

            if(is5_13_34_XiangShang(data,0)>2):
                info =info+ '5-13-34都上升-'
            else:
                info =info+ '5-13-34不满足-'

            # 两个小阴线最好高开  这种情况很少见
            if( day2_open > day1_close  ):
                key_4=key_4+1
            if(day3_open > day2_close):
                key_4 = key_4 + 1

            if(key_4==1):
                info=info+'1个阴线高开'
            elif(key_4==2):
                info =info+ '2个阴线高开(极少见)'
            else:
                info =info+'没有阴线高开-----'
            if (key_4==2 and is5_13_34_XiangShang(data,0)>2):

                info = info+'-中阳线=' + str(yangxian_shiti) + ',' +'小阴线1=' + str(yinxian_shiti1) + ',' + '小阴线2=' + str(yinxian_shiti2)

                info = info+"-----一箭双雕 主力中继洗盘模型 ---- "  + str(riqi)
                # print info
                writeLog_to_txt(info, stockcode)

                path = '一箭双雕.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例
'''
def test_isAn_YiJianShuangDiao_laoshi():


    # 案例 0-2
    df1 = ts.pro_bar(ts_code='000059.SZ',adj='qfq', start_date='20210206', end_date='20210907',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:14]  # 前4行
    # print data7_1
    isAn_YiJianShuangDiao_model(data7_1,'000059.SZ')
    # 案例 0-3  这两个是后来讲的案例, 比较符合模型的.

    df1 = ts.pro_bar(ts_code='300233.SZ', adj='qfq', start_date='20210206', end_date='20210628',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:14]  # 前4行
    # print data7_1
    isAn_YiJianShuangDiao_model(data7_1, '300233.SZ')


    # 案例 2  此案例 小阴线实体 大于 1.6 .
    #5-13-34都上升-2个阴线高开(极少见)-中阳线=12.50,小阴线1=-0.22,小阴线2=-1.76-
    # ----一箭双雕 主力中继洗盘模型  成功了 ----000928.SZ ----20210426--中钢国际--强势股票
    df1 = ts.pro_bar(ts_code='000928.SZ',adj='qfq', start_date='20210206', end_date='20210429',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:14]  # 前4行
    # print data7_1
    isAn_YiJianShuangDiao_model(data7_1,'000928.SZ')

    # 案例 3
    df1 = ts.pro_bar(ts_code='002466.SZ',adj='qfq', start_date='20200206', end_date='20210107',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:14]  # 前4行
    # print data7_1
    isAn_YiJianShuangDiao_model(data7_1,'002466.SZ')

    # 案例 4
    df1 = ts.pro_bar(ts_code='002229.SZ',adj='qfq', start_date='20200206', end_date='20210416',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:14]  # 前4行
    # print data7_1
    isAn_YiJianShuangDiao_model(data7_1,'002229.SZ')


'''
测试老师举例讲解学生 失败案例
'''
def test_isAn_YiJianShuangDiao_laoshi_shibai_anli():
    # 案例 1

    df1 = ts.pro_bar(ts_code='600900.SH',adj='qfq', start_date='20210206', end_date='20210927',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:14]  # 前4行
    # print data7_1
    isAn_YiJianShuangDiao_model(data7_1,'600900.SH')

def linshi():

    df1 = ts.pro_bar(ts_code='000061.SZ',adj='qfq', start_date='20210206', end_date='20211014',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:14]  # 前4行
    print data7_1
    isAn_YiJianShuangDiao_model(data7_1,'000061.SZ')
'''
测试我自己的
'''
def test_isAn_YiJianShuangDiao_ziji():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例 1-----一箭双雕 主力中继洗盘模型  成功了 ----000423.SZ ----20210930--东阿阿胶

    # df1 = ts.pro_bar(ts_code='000423.SZ',adj='qfq', start_date='20210206', end_date='20210930')
    #-----一箭双雕 主力中继洗盘模型  成功了 ----000159.SZ ----20210810--国际实业
    # df1 = ts.pro_bar(ts_code='000159.SZ',adj='qfq', start_date='20210206', end_date='20210814')
    #-----一箭双雕 主力中继洗盘模型  成功了 ----000989.SZ ----20210816--九芝堂
    # df1 = ts.pro_bar(ts_code='000989.SZ',adj='qfq', start_date='20210206', end_date='20210819')

    #-----一箭双雕 主力中继洗盘模型  成功了 ----603416.SH ----20210810--信捷电气
    # df1 = ts.pro_bar(ts_code='603416.SH',adj='qfq', start_date='20210206', end_date='20210813')
    df1 = ts.pro_bar(ts_code='000061.SH',adj='qfq', start_date='20210206', end_date='20210813',ma=[5, 13, 34])


    data7_1 = df1.iloc[0:14]  # 前4行
    print data7_1
    isAn_YiJianShuangDiao_model(data7_1,'603416.SH')

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


        data7_4 = df.iloc[22:52]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 14 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_YiJianShuangDiao_model(data7_4[i:i + 14], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_YiJianShuangDiao(localpath1)
    # test_isAn_YiJianShuangDiao_laoshi()#测试老师举例 5个成功案例 其中一个 阴线实体为0,一个阴线实体大于 1.6  总共 3 个成功
    # test_isAn_YiJianShuangDiao_laoshi_shibai_anli()#测试老师举例讲解学生 失败案例

    # test_isAn_YiJianShuangDiao_ziji()
    test_Befor_data() #测试 8 月份所有数据
    # linshi()
