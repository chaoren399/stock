#!/usr/bin/python
# -*- coding: utf8 -*-
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, is_big_to_small, print1
from stock.settings import BASE_DIR

'''
葛式八法 买 1

2021年09月22日  :  
https://www.yuque.com/chaoren399/eozlgk/ett8fr

思路 : MA10-MA60  的值 只要 
分为 2 个数组, ma10-ma60 的值由大到小 而且是正的, 另一个 是由大到小
取4 个值 ,分为 数组a, 数组 b ,   数组 a 有一个值,最前边的一个 , 数组b 是后两个值, 

第一步 : 用  Get_Week_K_data.py 来 得到 周K 线
第二步:   计算 10 周K 线 和 60 周K 线, 葛式八法 需要的
 


trade_date,open,close,high,low,WeekMa10,WeekMa60,Week60-10
2021-03-28,20.55,21.14,21.65,20.4,22.452999999999992,16.50683333333334,-5.946166666666652



'''
def getallstockdata_is_GeShi_8fa():
    info1= '------start 葛式八法---'
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST-1.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    if(len(data)>0):

        # print len(data)
        # print '1111111'
        for index, row in data.iterrows():
            stock_code = row['ts_code']
            stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
            df = pd.read_csv(stockdata_path, index_col=0)
            df = df.reset_index(drop=False)  # 重新建立索引 ,
            # print df
            if (df.empty):
                continue

            df1=df.iloc[0:4]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据
            df2=df.iloc[0:8]  #  主要测试 60 周均线
            # df=df.iloc[4:8]  # 测试  上个月的数据 7 月份
            # df=df.iloc[12:18]  # 测试  上个月的数据  月份

            # 再找到 慢速 60 周均线明显 上涨的,
            isAn_GEShi8_model(df1,df2, stock_code)
            count = count + 1
            # print count


def isAn_GEShi8_model(data,data1,stock_code):
    # print data1

    if (data is None or data.empty):
        print '--df.empty--' + str(stock_code)
        return 0
    len_data = len(data)

    if(len_data>3):

        key_1=0; # 第一个数组A 大于 0
        key_2=0; # 第 2 个数组 小于 0
        key_3=0; # 10周线是向上的
        key_4=0; # 60周线是向上的

        count=0
        # riqi=data.ix[0]['trade_date']
        # riqi='111'
        riqi=data.ix[0]['trade_date']
        Week10_60 =[]

        data_a= data[0:1]
        data_b= data[len_data-2:len_data]


        if(data_a.ix[0]['Week10-60'] > 0):
            key_1=1

        data_b_Week10_60=[]
        for index,row in data_b.iterrows():
            Week10_60 =row['Week10-60']
            data_b_Week10_60.append(Week10_60)
            if(Week10_60 <0):
                count=count+1
        if(count==2 and is_big_to_small(data_b_Week10_60)==1):
            key_2=1
        # print1(data_b_Week10_60)


        week10=[]
        week60=[]
        for index,row in data.iterrows():
            week10.append(row['WeekMa10'])

        for index,row in data1.iterrows():

            week60.append(row['WeekMa60'])
        # print1(week60)

        if(is_big_to_small(week10)==1):
            key_3=1
        if(is_big_to_small(week60)==1):
            key_4=1


        if(key_1==1 and key_2==1 and key_3==1and key_4==1):

                # path = BASE_DIR + '/jishu_stock/zJieGuo/G8/9/' +'G8M1-'+ datetime.now().strftime('%Y-%m-%d') +'.txt'

                info = "-----葛式八法---"  + stock_code + ' ----' + str(riqi)
                # print info
                writeLog_to_txt(info, stock_code)

def test_one_stock_is_GeShi_8fa():

    # -----葛式八法---000839.SZ ----3.02--强势股票----中信国安
    # -----葛式八法---000685.SZ ----9.45--强势股票----中山公用
    stock_code='000001.SZ'
    stock_code='000685.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    df = df.reset_index(drop=False)  # 重新建立索引 ,
    # print df

    df1 = df.iloc[0:4]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据
    df2 = df.iloc[0:8]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据
    print1(df1)
    # df.set_index('trade_date', inplace=True)

    isAn_GEShi8_model(df1,df2, stock_code)

if __name__ == '__main__':

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # getAllWeekKdata(localpath1)  #更新数据的时候可以打开 可以每周更新一次

    getallstockdata_is_GeShi_8fa()
    # test_one_stock_is_GeShi_8fa()
