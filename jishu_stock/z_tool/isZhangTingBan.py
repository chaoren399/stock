#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR


'''
判断 row 是不是涨停板, 返回 1 是涨停板, 返回 0 不是涨停板

只做 00 60 开头的 股票
'''



def isAn_ZhangtingBan(row):
    '''
    60  00 开头的 10%

    30 68 开头的 20%

    '''

    zhangfuMax = 9.1 # 涨幅 是不是大于 这个
    pct_chg = row['pct_chg']
    if(pct_chg > zhangfuMax):  # 涨停板
        return 1;

    return 0;



if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    localpath1 = '/jishu_stock/stockdata/data1/'
