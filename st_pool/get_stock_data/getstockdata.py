#!/usr/bin/python
# -*- coding: utf8 -*-

import tushare as ts
import pandas as pd
import numpy as np
import sys
import os
from datetime import *

def getdata(stock_pool_path):
#1. 处理 我的估值表格
    df_1 = pd.read_csv(stock_pool_path,dtype=object)

    df_1.columns = ['code', 'name','lowprice','upprice','order','tar_value','now_price','jiazhilv','date']

    for index ,row in df_1.iterrows():

        code = row['code'].zfill(6)

        df_1.iloc[index, 0] = code # 把 776转成 000776
        print code
        stockdata = ts.get_realtime_quotes(row['code']) #df[['code','name','price','bid','ask','volume','amount','time']]
        # data3.trade - data3.lowprice
        df_1.iloc[index, 7] = float(stockdata['price'][0])-  float(row['lowprice']) # 生成价值率 jiazhilv
        df_1.iloc[index, 6] = stockdata['price'][0]


        # df_1.iloc[index, 7] = df_1['']
        df_1.iloc[index, 8] = stockdata['date'][0]




        # print stockdata['date'][0]

    print df_1
    return df_1



if __name__ == '__main__':
#1
    path1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path2 = path1 + '/get_stock_data/get_today_all.csv'
    # download_data(path2) #下载之后关闭

#2

    path3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stock_pool_path = path3 + '/get_stock_data/股票池.csv'
    getdata(stock_pool_path)





