#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import pandas as pd
import tushare as ts
from jishu_stock.Tool_jishu_stock import isInQiangShi_gupiaochi, get_Stock_Name, \
    jiagezhongshu_writeLog_to_txt_path_getcodename, writeLog_to_txt_path_getcodename, print1, isYangXian, \
    is_small_to_big
from stock.settings import BASE_DIR

'''
https://www.yuque.com/chaoren399/eozlgk/byziie/

葛式八法 买 2 ,  老萧 2021年11月20 日直播提到的
创建日期: 2021年11月23日 

方法:  就是阳线有个下影线 穿越 60 周均线, 并且 60 周均线向上.

目的 找到每周增长 5% 的模型.
G8M2_XiaYingXian

阳线 下影线 下穿 60 周均线

'''

def get_all_G8M2_XiaYingXian_YangXian():
    print '-------G8M2 阳线影线下穿 60 周均线start 葛式八法---'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    if(len(data)>0):

        for index, row in data.iterrows():
            stock_code = row['ts_code']
            stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
            df=pd.DataFrame()
            try:
                df = pd.read_csv(stockdata_path, index_col=0)
            except IOError:
                print  stock_code+"Error: 没有找到文件或读取文件失败"
            # print df
            if (df.empty):
                continue
            df = df.reset_index(drop=False)  # 重新建立索引 ,

            df=df.iloc[0:15]  # 只找最近 1 个月的

            is_G8M2_XiaYingXian_YangXian_model(df, stock_code)


def is_G8M2_XiaYingXian_YangXian_model(data, stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if (len_data >= 2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1 = data[len_data - 2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        # print1(data1)
        riqi = data1.ix[1]['trade_date']  # 阳线的日期

        data2 = data[len_data - 10:len_data]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key

        key_1 = 0;  # 阳线的下影线 穿过 MA60
        key_2 = 0;  # MA60 向上

        key_3=1; # 所有数据,开盘价 收盘价都在 MA60 以上


        week2_open=0
        week2_low=0
        week2_ma60=0
        count=0
        for index,row in data1.iterrows():
            if(index==1and isYangXian(row)==1):
                count=count+1
                week2_open=row['open']
                week2_low=row['low']
                week2_ma60=row['WeekMa60']
        if(count==1):
            # 阳线的下影线 穿过 MA60
            if(week2_open > week2_ma60 and week2_low < week2_ma60):
                key_1=1
            # MA60 向上

            ma60s=[]
            for index,row  in data2.iterrows():
                ma60 = round(row['WeekMa60'],2)
                ma60s.append(ma60)
                week_close=row['close']
                week_open=row['open']
                if(week_close < ma60):
                    key_3=0
                if(week_open < ma60):
                    key_3=0



            if(is_small_to_big(ma60s)==1):
                key_2=1
            # print1(ma60s)



    # print1(key_1)
    # print1(key_2)
    # print1(week2_low)
    # print1(week2_open)
    # print1(week2_ma60)


    if (key_1 == 1 and key_2 ==1 and key_3==1  ):
        #     print1(shangyingxian_xiayingxian)
        info = ''


        info = info + "--G8M2下影线_阴线--" + str(riqi)
        # print info
        # writeLog_to_txt(info, stockcode)

        path = BASE_DIR + '/jishu_stock/sJieGuo/G8/' + 'G8M2下影线-阳线-' + datetime.datetime.now().strftime(
            '%Y-%m-%d') + '.txt'

        jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)

        path = 'G8M2下影线_阳线.txt'
        writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试自己的案例
'''
def test_isAn_G8M2_XiaYingXian_YangXian_ziji():
    #自己的 案例
    #价格中枢-实体一半=0.04---上影线是下的几倍=1.33---阳线实体=7.26---实体看涨做涨--2021-10-31--维力医疗**603309.SH

    # df = ts.pro_bar(ts_code='600653.SH', adj='qfq', freq='W', start_date='20170101', end_date='20211119',ma=[60])

    stock_code ='600653.SH'
    stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    df = df.reset_index(drop=False)  # 重新建立索引 ,
    data7_1 = df.iloc[1:100]  # 1 年有 50 周
    is_G8M2_XiaYingXian_YangXian_model(data7_1, '600653.SH')
#--G8M2下影线--20211112--华锦股份--强势股票**000059.SZ

    stock_code ='000059.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    df = df.reset_index(drop=False)  # 重新建立索引 ,
    data7_1 = df.iloc[0:5]  # 1 年有 50 周
    is_G8M2_XiaYingXian_YangXian_model(data7_1, stock_code)


if __name__ == '__main__':

    get_all_G8M2_XiaYingXian_YangXian()
    # test_isAn_G8M2_XiaYingXian_YangXian_ziji()


