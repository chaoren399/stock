#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from pandas import DataFrame

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, getRiQi_Befor_Ater_Days
from stock.settings import BASE_DIR


'''
第一步  遍历所有的七星 1 七星 2 

第二步 , 根据 日期获取第二天的交易数据 ,从第 3 天开始 找最高价,只要大于 3% 的 就可以是成功, 
'''

def getall7start_data():
    path = BASE_DIR + '/jishu_stock/bQiXingLuoChangKong/7startdata.csv'

    # print "ssss"
    print path
    count = 0
    price_10_count=0;  # 价格高于 10 的
    data = pd.read_csv(path)
    len_data = len(data)

    for index, row in data.iterrows():
        stock_code = row['ts_code']
        start_date=str(row['trade_date'])
        start_date= getRiQi_Befor_Ater_Days(start_date,1)
        # print start_date
        df = ts.pro_bar(ts_code=stock_code, start_date=start_date, end_date='20210824')
        df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序
        df = df.reset_index(drop=True)  # 重新建立索引 ,
        high_price = df.ix[0]['open'] * 1.1
        # if (df.ix[0]['open'] > 10 and df.ix[0]['open'] < 30):
        if (df.ix[0]['open'] > 15):
        # if (1):
            price_10_count = price_10_count + 1
        # print stock_code+ "买入"+str(df.ix[0]['open']) + "最高价"+str(high_price)
            flag1 = 1;
            high_price_riqi  = df.ix[0]['trade_date']
            for index1, row1 in df.iterrows():
                if(row1['high'] > high_price):
                    high_price_riqi = row1['trade_date']
                    print stock_code+ "----成功---"+start_date+'结束日期'+str(high_price_riqi) +"---"+str(df.ix[0]['open'])
                    count=count+1
                    flag1=0
                    break
            if(flag1 == 1):

                print stock_code + "----失败---" + start_date+"---"+str(df.ix[0]['open'])



        # print df

    print count
    print price_10_count
    print "成功率=" + str( float(count) / float(price_10_count))


if __name__ == '__main__':
    getall7start_data()