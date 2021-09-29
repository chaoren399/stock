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

def  getDuoZhi_Gupiao():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    pro = ts.pro_api()
    # 多个股票
    df = pro.daily(ts_code='000001.SZ,600000.SH', start_date='20180701', end_date='20180718',ma=[5, 13, 34])
    print df

def testLiRunbiao():

    pro = ts.pro_api()

    df = pro.query('fina_indicator', ts_code='600000.SH', start_date='20190101', end_date='20200101')
    df.to_csv('1.csv')
    df_sum = df.sum()
    print df_sum['roe']
    print df_sum['roe_waa']
    print df_sum['roe_dt']
    print df_sum['roe_yearly']
    # print df
'''
财务指标数据
https://waditu.com/document/2?doc_id=79
'''
def testfina_indicator():
    pro = ts.pro_api()
    df = pro.query('fina_indicator', ts_code='600000.SH', start_date='20171231', end_date='20171231')
    day3=df.ix[0]['roe']
    print day3
    # print df

    df = pro.query('fina_indicator', ts_code='600000.SH', start_date='20181231', end_date='20181231')
    day3=df.ix[0]['roe']
    print day3

    df = pro.query('fina_indicator', ts_code='600000.SH', start_date='20191231', end_date='20191231')
    day3=df.ix[0]['roe']
    print day3

    df = pro.query('fina_indicator', ts_code='600000.SH', start_date='20201231', end_date='20201231')
    day3=df.ix[0]['roe']
    day3_npta=df.ix[0]['npta']
    print day3
    print day3_npta

if __name__ == '__main__':
    # getETFdata()
    # getDuoZhi_Gupiao()
    # testLiRunbiao()
    testfina_indicator()