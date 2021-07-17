#encoding=utf-8
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR
import json

'''
测试  
2021年07月16日  tushare 改版,导致 添加的股票有获取历史数据, 
所以增加了这个方法 . 后期数据尽量不变.
'''
def test_new_getstockdatafrom_ts_5years(stock_code):
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    stock_code_SZ=stock_code
    stock_code = stock_code_SZ.split('.')[0]

    pro = ts.pro_api()
    df = pro.daily(ts_code=stock_code_SZ, start_date='20140101', end_date='20190101')
    # df = pro.daily(ts_code='000001.SZ', start_date='20140101', end_date='20190101')
    df = ts.get_hist_data(stock_code)
    # print df
    print stock_code
    f = open(BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data_2014_2019/' + stock_code + '.csv', 'w')
    for index, row in df.iterrows():
        date1 = row['trade_date']
        date2 = date1[0:4] + '-' + date1[4:6] + '-' + date1[6:8]
        # print date2
        f.write(date2 + ',' + str(row['close']) + '\n')
    f.close()


'''
旧接口
'''

def test_old_getstockdatafrom_ts_5years(stock_code):
    df = ts.get_hist_data(stock_code)
    f = open(BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data_2014_2019/' + stock_code + '.csv', 'w')
    print df
    for index, row in df.iterrows():
        f.write(index + ',' + str(row['close']) + '\n')
    f.close()


def test_olde_getdatafrom_ts_1years(stock_code):

    enddate = str(datetime.date.today()) #获取股票池的最近 1 年的 数据
    df =  ts.get_hist_data(stock_code,start='2021-01-01',end=enddate)
    print df
    # df =  ts.get_hist_data(stock_code)

    f = open(BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data/' + stock_code + '.csv', 'w')
    for index, row in df.iterrows():
        f.write(index + ',' + str(row['close']) + '\n')
    f.close()


if __name__ == '__main__':
    # test_getstockdatafrom_ts_5years('300014.SZ')
    test_old_getstockdatafrom_ts_5years('601012')
    test_olde_getdatafrom_ts_1years('601012')