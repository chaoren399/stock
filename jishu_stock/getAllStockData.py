#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts
import sys

from jishu_stock.Tool_jishu_stock import writeLog_to_txt
from stock.settings import BASE_DIR
import pandas as pd
import time
reload(sys)

sys.setdefaultencoding('utf8')

def getAllStockData(start_date , end_date, localpath):
    info = str(end_date)+ "开始运行 --------------"
    writeLog_to_txt(info)

    print "下载 更新数据  start"
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # print "ssss"
    print path
    data = pd.read_csv(path, dtype={'code': str})

    start_date = start_date
    end_date = end_date
    count = 0
    for index, row in data.iterrows():
        count = count + 1
        # print row['ts_code']
        name = row['name']
        stock_code = row['ts_code']
        if ('ST' not in name):
            # 下载股票信息 近一个月的
            time.sleep(0.05)  # //睡觉

            # df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
            # df = pro.daily(ts_code=stock_code, start_date='20210701', end_date='20210802')
            #  2021年08月16日 增加 ma5 ma13 ma 34
            df = ts.pro_bar(ts_code=stock_code, start_date=start_date, end_date=end_date, ma=[5, 13, 34])
            stockdata_path = BASE_DIR + localpath
            df.to_csv(stockdata_path + stock_code + ".csv")
            print count




if __name__ == '__main__':
    starttime = datetime.datetime.now()


    localpath= '/jishu_stock/stockdata/data1/'
    today = starttime.strftime('%Y%m%d')
    getAllStockData(start_date = '20200801',end_date = today,localpath=localpath)

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds / 60