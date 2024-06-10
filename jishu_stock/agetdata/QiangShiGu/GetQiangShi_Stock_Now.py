#!/usr/bin/python
# -*- coding: utf8 -*-
import time

import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt_path
from stock.settings import BASE_DIR
import tushare as ts
import sys

reload(sys)
sys.setdefaultencoding('utf8')



'''


强者恒强, 思路:

20210121 - 20210128 大盘下跌,  28日收盘价 大于 21 日收盘价

2021年12月13日 -2021年12月20日大盘走势是 下跌趋势.
我们找到 个股  在相同日期 中成上涨趋势的股票 ,这样就有了一个强于大盘的 股票池

20日 的收盘价 大于 13 日的收盘价 就可以

'''

def getallQiang_stock_12():
    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST-1.csv'
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})


    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        start_date='20220121'
        end_date = '20220128'
        df = ts.pro_bar(ts_code=stock_code, start_date=start_date, end_date=end_date)

        df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        df = df.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。



        # print df
        len_df =len(df)
        if(len(df) >0 ):

            time.sleep(0.1)

            # print count
            close_start = df.ix[0]['close']
            close_end = df.ix[len_df-1]['close']


            if(close_end > close_start):
                count = count + 1
                # line = {'ts_code': stock_code}
                # path1 = BASE_DIR + '/jishu_stock/z_stockdata/qiangshi_stock.csv'
                # print df
                path1 = 'qiangshi_stock.csv'
                writeLog_to_txt_path(stock_code,path1)
                print stock_code
    print count





if __name__ == '__main__':
    # getallQiang_stock()
    getallQiang_stock_12()