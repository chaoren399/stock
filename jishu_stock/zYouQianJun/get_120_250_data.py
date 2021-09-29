#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts
import sys

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1
from stock.settings import BASE_DIR
import pandas as pd
import time
reload(sys)

sys.setdefaultencoding('utf8')

''''
单独处理 120 250 的日线数据
'''
def get_120_250_StockData():
    starttime = datetime.datetime.now()
    today = starttime.strftime('%Y%m%d')
    start_date = '20150101'
    end_date = today
    info = " 下载 120 250 的日线数据数据开始运行 ----------start_date="+str(start_date)+'--end_date='+str(end_date)

    print info
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表


    path_150stock = BASE_DIR + '/jishu_stock/zYouQianJun/150stock.csv'  # 150个的数据


    data_150stock = pd.read_csv(path_150stock, dtype='object')

    for index,row in data_150stock.iterrows():
        stock_code_1= str(row[0])

        #1 得到股票的全称代码
        stock_code = getStockCode_to_SHSZ(stock_code_1)
        if(stock_code ==0):
            print '数据为空'+stock_code_1
        else:

            #2 开始下载数据
            #  2021年08月16日 增加 ma5 ma13 ma 34
            df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=end_date, ma=[120, 250])
            df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
            stockdata_path = BASE_DIR + '/jishu_stock/zYouQianJun/150data/'+stock_code+'_150'+".csv"
            # 3 保存数据

            df.to_csv(stockdata_path)
            # print df




'''
得到 150 只股票对应的同花顺代码
'''
def getStockCode_to_SHSZ(stockcode_1):
    path = BASE_DIR + '/jishu_stock/zYouQianJun/' + 'allstock_list' + ".csv"
    data = pd.read_csv(path, dtype={'code': str})
    for index1, row1 in data.iterrows():
        name = row1['name']
        stock_code = row1['ts_code']
        s1 = stock_code[0:6]


        if (s1 == stockcode_1):
            # print1(s1)
            # print1(stockcode_1)
            return stock_code
    return 0

def test_getStockCode_to_SHSZ():
    stock_code_1='688516'
    stock_code = getStockCode_to_SHSZ(stock_code_1)
    print1(stock_code)

if __name__ == '__main__':
    starttime = datetime.datetime.now()


    get_120_250_StockData()
    #
    # test_getStockCode_All()



    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds / 60