#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts

'''
https://waditu.com/document/2?doc_id=19
'''
def getETFdata():
    '''沪港深ETF500","517060",'''


    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    pro = ts.pro_api()

    df = pro.daily(ts_code='512850.SH', start_date='20180701', end_date='20180718')
    print df
    # df = pro.fund_basic(market='E')
    print df


if __name__ == '__main__':
    getETFdata()