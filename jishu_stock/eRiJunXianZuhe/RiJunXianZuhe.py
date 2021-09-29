#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1
from stock.settings import BASE_DIR
from jishu_stock.Tool_jishu_stock import is_big_to_small,is_small_to_big

'''
2021年09月13日 
https://www.yuque.com/chaoren399/eozlgk/mg1zu3

找一个比较精确的方法.来测出来,我们找的是 N 字形 , 

找金叉 ,  就是 ma5 - ma13  的值 由大到小, 然后 又 由小到大  


https://tushare.pro/document/2?doc_id=109

日均线组合5-13-34

一定找 上涨中的 N 字型

2021年09月08日 

多头排列, 

方法 3 
先找 最近 7 天, 3 条均线 都是向上的 
然后再 找 近 7 天死叉 金叉的. 看看数量有多少

'''
def get_5_13_34_RiJunXian(localpath1):
    info1=  '--日均线组合5-13-34  start--固定 4 个值 来判断金叉 data7_1 = df.iloc[0:4]  '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        df = df[['ts_code', 'trade_date', 'low', 'ma5', 'ma13', 'ma34']]
        df['ma5_13_cha'] = df['ma5'] - df['ma13']
        data7_1 = df.iloc[0:4]  # 前7行
        # data7_1 = df.iloc[1:8]  # 前7行
        # data7_1 = df.iloc[15:22]  # 前7行
        # print data7_1
        isyes = isRiJunxianZuHe_mode_pro4(data7_1, stock_code)

'''
这个方法是判断 已经出现金叉 
找金叉 ,  就是 ma5 - ma13  的值 由大到小, 然后 又 由小到大  

'''
def isRiJunxianZuHe_mode_pro4(data, stock_code):
    data_len=len(data)
    if(data_len==4):
        #倒序排列
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index()  # 重新建立索引 , 保留日期
        # 1 分 2 个数组, 第一个金叉向上的两个 ,数组的最后 2 个值 , 金叉 左侧的值 由 2 个值 右侧 有 1 个值

        data_befor=data[0:2]
        data_last=data[data_len-1:data_len]

        data4= data[data_len-2:data_len] #ma5 ma13 ma34  3 个线 都要 向起头并进 ,

        riqi= data.ix[3]['trade_date']

        data_befor=data_befor.reset_index()
        data_last=data_last.reset_index()
        data4=data4.reset_index()

        key_1 = 0;  # 金叉右侧 的差值是必须大于 0
        key_2=0; # 金叉 左侧的 差值是不是 由大到小 必须小于 0

        key_3=0; # ma34 必须是 向上的走势
        key_4=0 # ma5 ma13 ma34  3 个线 都要 向起头并进 ,
        key_5=0 # 最近 一个月 WeekMa60 向上

        if(data_last.ix[0]['ma5_13_cha'] >0):
            key_1=1

        data_befor_ma5_ma13=[]
        for index, row in data_befor.iterrows():
            if(row['ma5_13_cha']>  0):
                return
            data_befor_ma5_ma13.append(row['ma5_13_cha'])

        if( is_small_to_big(data_befor_ma5_ma13)==1):
            key_2=1

        ma34_data = []
        for index, row in data.iterrows():
            ma34_data.append(row['ma34'])

        if (is_small_to_big(ma34_data) == 1 and len(ma34_data) > 0):
            key_3 = 1

        # ma5 ma13 ma34  3 个线 都要 向起头并进 ,


        data4_ma5=[]
        data4_ma13=[]

        for index, row in data4.iterrows():
            data4_ma5.append(row['ma5'])
            data4_ma13.append(row['ma13'])

        # print data4_ma5
        # print data4_ma13



        if(is_small_to_big(data4_ma5)==1 and is_small_to_big(data4_ma13)==1):
            key_4=1

        if(ma60_Week_is_XiangShang(stock_code)==1):
            key_5=1

        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)

        if ( key_1==1 and key_2==1 and key_3==1 and key_4==1 and key_5==1):
        # if ( key_1==1 and key_2==1 and key_3==1 and key_4==1 ):
                info = "-----日均线组合5-13-34 成功了" + ' ----' + stock_code + ' ----' + str(riqi)
                # print info
                writeLog_to_txt(info, stock_code)

def ma60_Week_is_XiangShang(stock_code):
    stock_code = stock_code
    stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    df = df.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print df
    if (df.empty):
        print '--WEEK_DATA_K--df.empty--'+str(stock_code)
        return 0

    df = df.iloc[0:4]  # 只找最近 1 个月的

    df = df.reset_index()
    # print df
    df_WeekMa60=[]
    for index, row in df.iterrows():
        df_WeekMa60.append(row['WeekMa60'])

    if(is_big_to_small(df_WeekMa60)==1):
        return 1

    return 0


'''
数组 是由小到大排列  返回 1  ,否则 0 
'''
def is_small_to_big(data):
    len_data = len(data)
    if(len_data > 0):
        is_small_to_big_flag=1
        for i in range(0, len_data - 1):
            # week10_60s[i:i+1]
            if (data[i] > data[i + 1]):
                is_small_to_big_flag = 0

        if(is_small_to_big_flag == 1):
            return 1
    return 0



def test_ma60_Week_is_XiangShang():
    # stock_code='002319.SZ'
    stock_code='002297.SZ'
    print ma60_Week_is_XiangShang(stock_code)



def test_get_5_13_34_RiJunXian_Pro3_1():

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    pro = ts.pro_api()
    df = ts.pro_bar(ts_code='600238.SH', start_date='20200417', end_date='20210528',ma=[5, 13, 34]) # 老师案例
    # df = ts.pro_bar(ts_code='002922.SZ', start_date='20210417', end_date='20210920',ma=[5, 13, 34])

    df = df[['ts_code', 'trade_date', 'low', 'ma5', 'ma13', 'ma34']]
    df['ma5_13_cha'] = df['ma5'] - df['ma13']

    data7_1 = df.iloc[0:4]  # 前7行
    # print data7_1

    isyes = isRiJunxianZuHe_mode_pro4(data7_1, '600238.SH')

'''
找 ma5-ma13 为0 并且 阳线的那种
'''
def ma5_ma13_is0():

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        df = df[['ts_code', 'trade_date', 'low', 'ma5', 'ma13', 'ma34']]
        df['ma5_13_cha'] = df['ma5'] - df['ma13']
        data7_1 = df.iloc[0:4]  # 前7行

        # print1(df.ix[0]['ma5_13_cha'])

        if( df.ix[0]['ma5_13_cha']==0):
            print1(stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_5_13_34_RiJunXian_Pro3(localpath1=localpath1)
    test_get_5_13_34_RiJunXian_Pro3_1()
    # ma5_ma13_is0()
    # test_ma60_Week_is_XiangShang()



