#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts

from jishu_stock.z_tool.PyDateTool import getDayNumberYMD
from stock.settings import BASE_DIR

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''


处理 每天 沪深两市 的交易额, 每天万亿以上的才是牛市.

'''

def get_HS_index_data():
    ts.set_token('0c9acbe761612301ff2baaa9b3e8ec4053150ad1c1fb0e7b6d53bd5d')



    # starttime = datetime.datetime.now()
    today = getDayNumberYMD()

    start_date = '20210101'

    # 上证指数 000001.SH
    df1 = ts.pro_bar(ts_code='000001.SH', adj='qfq', asset='I', start_date=start_date, end_date=today)
    df1 = df1[['trade_date', 'amount']]

    df1=df1.set_index('trade_date')

    # 深证成指 399001
    df2 = ts.pro_bar(ts_code='399001.SZ', adj='qfq', asset='I', start_date=start_date, end_date=today)
    df2 = df2[['trade_date', 'amount']]

    # print df2
    df2 = df2.set_index('trade_date')

    df3 =  df1 +df2
    df3 = df3.reset_index(drop=False)
    # df3 =
    hsstockpath = BASE_DIR + '/st_pool/get_index_data/index_old_data/'
    # df3.to_csv(hsstockpath + 'hs' + ".csv")

    return df3

    # print df1[['trade_date','amount']]


if __name__ == '__main__':
    print  get_HS_index_data()