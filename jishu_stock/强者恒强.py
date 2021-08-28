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

2021年08月11日 -2021年08月20日大盘走势是 下跌趋势.
我们找到 个股  在相同日期 中成上涨趋势的股票 ,这样就有了一个强于大盘的 股票池

20日 的收盘价 大于 11 日的收盘价 就可以
'''

def getallQiang_stock():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})


    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        start_date='20210811'
        end_date = '20210820'
        df = ts.pro_bar(ts_code=stock_code, start_date=start_date, end_date=end_date)
        # print df
        if(len(df) ==8 ):
            count= count+1
            time.sleep(0.1)

            print count
            close_20 = df.ix[0]['close']
            close_11 = df.ix[7]['close']

            if(close_20 > close_11):
                # line = {'ts_code': stock_code}
                path1 = BASE_DIR + '/jishu_stock/stockdata/qiangshi_stock.csv'
                writeLog_to_txt_path(stock_code,path1)
                print stock_code





if __name__ == '__main__':
    getallQiang_stock()