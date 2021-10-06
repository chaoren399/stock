#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1, is_big_to_small
from stock.settings import BASE_DIR

''''
九死一生 1 底部强势反转
https://www.yuque.com/chaoren399/eozlgk/lp8wzh/
熊市未期急速下跌
连续阴线的最后一根阴线是中阴线/大阴线
(最好最后一根阴线实体最大)
中阳线/大阳线高开高收

思路:  选出最近 的 4 个数据,  前 3 个是 阴线, 最后一个是 中阳线/大阳线高开高收


'''

def get_all_JiuSiYiSheng_1(localpath1):
    info1=  '--九死一生 1 底部强势反转 (最好最后一根阴线实体最大) 熊市未期急速下跌 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:4]  # 前4行
        # data6_1 = df.iloc[1:5]  # 前4行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_JiuSiYiSheng_1_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JiuSiYiSheng_1_model(data,stockcode):
    # print len(data)
    if(len(data)==0):
        print str(stockcode)+'--data --is null'
    if(len(data) == 4):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data
        riqi = data.ix[3]['trade_date'] # 阳线的日期

        # 设置两个 key
        key_1=0; #连续 3 天的阴线
        key_2=0; #是否收阳线 中阳线/大阳线高开高收
        key_3=0; # 大阴线 是不是 day3_yin_pct_chg 大于 5% ,打开开关后, 概率很低
        key_4=0; # 3个阴线是 跳空的

        key_5=0; # 必须符合 祖传模型

        # print data
        day1_yin_open = 0
        day1_yin_close=0
        day1_yin_pct_chg = 0

        day2_yin_open = 0
        day2_yin_close=0
        day2_yin_pct_chg = 0

        day3_yin_open=0
        day3_yin_close=0
        day3_yin_pct_chg=0

        day4_yang_open=0
        day4_yang_close=0




        for index, row in data.iterrows():
            if(index==0 and isYangXian(row) ==0):
                key_1 = key_1+1
                day1_yin_close=row['close']
                day1_yin_open=row['open']
                day1_yin_pct_chg=abs(row['pct_chg'])
            if(index==1 and isYangXian(row) ==0):
                key_1 = key_1 + 1
                day2_yin_close = row['close']
                day2_yin_open = row['open']
                day2_yin_pct_chg = abs(row['pct_chg'])
            if(index==2 and isYangXian(row) ==0):
                key_1 = key_1 + 1
                day3_yin_open=row['open']
                day3_yin_close=row['close']
                day3_yin_pct_chg=abs(row['pct_chg'])

            if(index==3 and isYangXian(row) ==1):
                key_1 = key_1 + 1
                day4_yang_open=row['open']
                day4_yang_close=row['close']

        #高开高收
        if(day4_yang_open > day3_yin_close and day4_yang_close > day3_yin_open ):
            key_2=1
        if(day3_yin_pct_chg>=4):
            key_3=1
        #3个阴线是 跳空的
        if(day2_yin_open<= day1_yin_close  and day3_yin_open <= day2_yin_close):
            key_4=1

        ## 必须符合 祖传模型
        if(day1_yin_pct_chg<day2_yin_pct_chg and day2_yin_pct_chg< day3_yin_pct_chg):
            key_5=1

        # print1(key_1)
        # print1(key_2)
        # print1(key_5)

        if(key_1 ==4 and key_2==1  and  key_5==1):
            info=''

            # if (is_60WEEK_ShangZhang(stockcode, riqi) == 1):
            if (1):
                # info = info + "--60周上涨--"


                info = info+"---九死一生1 底部强势反转" + ' --' + stockcode + ' --' + str(riqi)

                writeLog_to_txt(info, stockcode)
                return 1

    return 0

'''
60周均线是不是一直上涨的
'''
def is_60WEEK_ShangZhang(stock_code,riqi):
    # print1(riqi)
    df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20180101', end_date=str(riqi))

    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    # print df
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行

    # print df
    df_week = df

    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    df_week['Week10-60'] = df_week['WeekMa10'] - df_week['WeekMa60']  # G8 买 2 用到

    df_week = df_week.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print  df_week[0:10]
    df_week = df_week[0:24] #一年有 48 周
    WeekMa60=[]
    for index, row in df_week.iterrows():
        WeekMa60.append(row['WeekMa60'])

    if(is_big_to_small(WeekMa60)==1):
        return 1
    return 0



def test_600173():
    # ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    #
    # # 查询当前所有正常上市交易的股票列表
    # pro = ts.pro_api()
    # 打印最新的数据
    stock_code='600173.SH'

    df1 = ts.pro_bar(ts_code='600173.SH', adj='qfq',start_date='20210204', end_date='20210219')
    # df1 = ts.pro_bar(ts_code='600173.SH', start_date='20210428', end_date='20210506')
    # df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011')
    data7_1 = df1
    print data7_1

    len_1 = len(data7_1)

    for i in range(0, len_1 - 4 + 1):
        # print "i" + str(i )+ "j"+str(i+3)
        ss= isAn_JiuSiYiSheng_1_model(data7_1[i:i + 4], stock_code)
        if(ss==1):
            continue

def test_isAn_JiuSiYiSheng_1_model():

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # 打印最新的数据

    df1 = ts.pro_bar(ts_code='002026.SZ', start_date='20210726', end_date='20210729')
    # df1 = ts.pro_bar(ts_code='300114.SZ', start_date='20210519', end_date='20210524')
    # df1 = ts.pro_bar(ts_code='600160.SH', start_date='20210630', end_date='20210705')


    data7_1 = df1.iloc[0:4]  # 前4行
    # print data7_1
    isAn_JiuSiYiSheng_1_model(data7_1,'002026.SZ')
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

        # data6_1 = df.iloc[0:4]  # 前4行
        data6_1 = df.iloc[26:30]  # 前4行
        data6_1 = df.iloc[26:58]  # 前4行
        data6_1 = df.iloc[48:80]  # 前4行
        len_1=len(data6_1)

        for i in range(0, len_1 - 4 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JiuSiYiSheng_1_model(data6_1[i:i + 4], stock_code)




if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_JiuSiYiSheng_1(localpath1)
    # test_isAn_JiuSiYiSheng_1_model()
    # test_Befor_data()
    # test_600173()