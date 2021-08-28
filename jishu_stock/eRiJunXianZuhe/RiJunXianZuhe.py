#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt
from stock.settings import BASE_DIR

'''
https://tushare.pro/document/2?doc_id=109

日均线组合5-13-34
方法 2 

如果我判断 近 10 天, ma5 ma13 相减 差值  由 正 到负  , 然后又由负到正,   这个应该不难

然后根据 日期 得到 之前的 60 天的数据, 只要当天是最大值说明是上涨趋势. 可以排除很多了 

'''
def get_5_13_34_RiJunXian(localpath1):
    print  '--日均线组合5-13-34  start--'
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    pro = ts.pro_api()
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        df = df[['ts_code', 'trade_date', 'low', 'ma5', 'ma13', 'ma34']]
        df['ma5_13_cha'] = df['ma5'] - df['ma13']

        data7_1 = df.iloc[0:10]  # 前7行
        # print data7_1

        isyes = isRiJunxianZuHe_mode(data7_1, stock_code)
        time.sleep(0.01)  # //睡觉



def isRiJunxianZuHe_mode(dataframe_df, stock_code):
    len1 = len(dataframe_df)
    # print len1
    count =0;
    for i in range(0, len1 - 2 + 1):
        x= isRiJunXianZuHe_2Days_data(dataframe_df[i:i + 2], stock_code)
        count = count + x

    # 找 最近 10 天的最小值
    min_10_tian = 0
    riqi= dataframe_df.ix[0]['trade_date']
    for index ,row in dataframe_df.iterrows():
        if(index == 1):
           min_10_tian = row['low']
        if( min_10_tian > row['low']):  # 近 10 天的最小值
            min_10_tian = row['low']
        if(row['ma34'] > row['ma5'] or row['ma34'] > row['ma13'] ): #  5日 和 13 日 必须大于 34 日慢线
            break;


    isYes = isLow_in_60days(stock_code,riqi,min_10_tian)
    if( count==2 and isYes == 1):
        info ="-----日均线组合5-13-34 成功了" +' ----'+ stock_code +' ----'+ str(riqi)
        # print info
        writeLog_to_txt(info,stock_code)

'''
得到 之前的 60 天的数据, 只要当天是最大值, 说明是上涨趋势. 可以排除很多了 

'''
def isLow_in_60days(stock_code,date,min_10_tian):
    import datetime
    day1riqi = str(date)
    # day1riqi = '20210813'
    # print date
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    result_date = cur_day + datetime.timedelta(days=-60)
    try:
        result_date = result_date.strftime('%Y%m%d')
    except Exception as e:
        print e

    pro = ts.pro_api()
    df = pro.daily(ts_code=stock_code, start_date=result_date, end_date=date)
    # print df
    # 计算最小值
    min = 0;
    date1 = date
    for index, row in df.iterrows():
        # 获取 每天的最低值
        if (index == 0):
            min = row['low']
            # print '------sss'+ str(row['low'])
        amin = row['low']
        if (amin < min):
            min = amin
            date1 = row['trade_date']
    if( min <= min_10_tian):
        return 1;
    return 0

'''
判断 2 个数据 是不是 一个正值,一个负值
'''
def isRiJunXianZuHe_2Days_data(data,stock_code):
    data = data.reset_index(drop=True)  # 重新建立索引 ,
    # print data
    if(len(data) ==2):
        a1=data.ix[0]['ma5_13_cha']
        a2=data.ix[01]['ma5_13_cha']
        if( a1 > 0 and a2 <0):
            # print a1
            # print a2
            return 1
        if(a1 <0 and a2 >0):
            # print a1
            # print a2
            return 1;

        return 0;



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_5_13_34_RiJunXian(localpath1=localpath1)
