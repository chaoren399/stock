#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from pandas import DataFrame

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian
from stock.settings import BASE_DIR

liststocks = []

'''

月线失败
得到一只股票判断 是不是满足 7 星落长空的标准  

复习 2021年09月01日   一定是  下跌中, 最好是 下跌中横盘
'''




def getallstockdata_is7start_From_Month_K(localpath1):
    info1 = "月线 7 星落长空1  start "

    writeLog_to_txt_nocode(info1 )

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})

    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        # stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/stockdata/MONTH_DATA_K/' + stock_code + '_Month' + ".csv"

        df = pd.read_csv(stockdata_path, index_col=0)
        if (df.empty):
            continue
        # data7_1 = df.iloc[0:7]  # 前7行
        data7_1 = df.iloc[2:9]  # 前7行

        # 2 单独一个函数 判断是不是符合 7 星落长空模型
        isAn7start_model_pro_Month_K(data7_1, stock_code)

'''
#2 单独一个函数 判断是不是符合 7 星落长空模型 3-2-1-1
'''
def isAn7start_model_pro_Month_K(dataframe_df,stockcode):
    # print len(dataframe_df)
    if(len(dataframe_df) ==7):

        dataframe_df = dataframe_df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        dataframe_df = dataframe_df.reset_index(drop=True)  # 重新建立索引 ,
        # print dataframe_df
        riqi = dataframe_df.ix[0][1]
        # print open
        # print close
        key_is7start=0
        for index, row in dataframe_df.iterrows():

            if(index ==0 and isYangXian(row)==0):
                # print row
                key_is7start= key_is7start+1
            if(index==1 and isYangXian(row)==0):
                key_is7start = key_is7start + 1
            if(index==2 and isYangXian(row)==0):
                key_is7start = key_is7start + 1
            if(index==3 and isYangXian(row)==1):
                key_is7start = key_is7start + 1
            if(index==4 and isYangXian(row)==1):
                key_is7start = key_is7start + 1
            if(index==5 and isYangXian(row)==0):
                key_is7start = key_is7start + 1
            if(index==6 and isYangXian(row)==1):

                key_is7start = key_is7start + 1

        if(key_is7start==7):
                info=  stockcode+"--------月线符合 七星落长空 3-2-1-1----------"+str(riqi)
                # print info
                writeLog_to_txt(info,stockcode)
                return 1
        return 0
    return 3





def test_isAn7start_model_pro_Month_K():
    stockdata_path = BASE_DIR + localpath1 + '600919.SH' + ".csv"
    # stockdata_path = BASE_DIR + '/jishu_stock/stockdata/MONTH_DATA_K/' + stock_code + '_Month' + ".csv"

    # df =  pd.read_csv(stockdata_path, dtype={'code': str})

    df = pd.read_csv(stockdata_path, index_col=0)
    data7_1 = df.iloc[0:7]  # 前7行
    isAn7start_model_pro_Month_K(data7_1,'603583.SH')
    # print df

if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()
    localpath1 = '/jishu_stock/stockdata/data1/'

    # test_isAn7start_model_pro_Month_K()
    getallstockdata_is7start_From_Month_K(localpath1)

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds

