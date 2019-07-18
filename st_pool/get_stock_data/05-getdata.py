#!/usr/bin/python
# -*- coding: utf8 -*-

import tushare as ts
import pandas as pd
import numpy as np
import sys
import os
from datetime import *

def get_today_all(path,range_path):
#1. 处理 我的估值表格
    df_1 = pd.read_csv(range_path)
    # print 'df_1'
    df_1.columns = ['code', 'name','lowprice','upprice','order']


    array = np.array(df_1['code'])  #取出 code列 为后期判断是否包含这个股票做准备



#2.处理下载的文件

    data2 = pd.read_csv(path)

    data2 = data2[data2['code'].isin(array)]


    # print 'data2sdddd'
    # print data2;

    # 处理价值率 , 最近价格减去 最低估值
    data3 = pd.merge(df_1,data2,left_on='code',right_on='code')
    data3['rate'] = data3.trade - data3.lowprice
    # data3 = data3.sort_values(by='rate')
    data3 = data3.sort_values(by='order') #如果其他排序没有设置默认是按照原始顺序




    path1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path2 = path1 + '/get_stock_data/alldata.csv'
    # path = '/Users/zzy/PycharmProjects/python-workspace/stock/st_pool/getdata/alldata.csv'
    data3.to_csv(path2,encoding='utf-8');

    # print 'sssss'
    for i, row in data2.iterrows():
        if row[2] == "南京银行":
            print row[2]
        # print row[2]
def download_data(path1):
    data1 = ts.get_today_all()
    # data1['date'] = sys.time

    dt = datetime.now()

   # 添加日期列
    data1['date'] =  dt.strftime('%Y-%m-%d %H:%M:%S')


    data1.to_csv(path1, encoding='utf-8')

if __name__ == '__main__':
#1
    path1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path2 = path1 + '/get_stock_data/get_today_all.csv'
    download_data(path2) #下载之后关闭

#2

    path3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path4 = path3 + '/get_stock_data/股票池.csv'
    get_today_all(path2,path4)





