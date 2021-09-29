#!/usr/bin/python
# -*- coding: utf8 -*-
import tushare as ts
import sys
import pandas as pd

from jishu_stock.Tool_jishu_stock import print1
from stock.settings import BASE_DIR

reload(sys)

sys.setdefaultencoding('utf8')

'''
把 ST 的 300 的 688 的 处理后 

不包含 ST  和 300 开头的创业板 688开头的科创板股票
'''
def  getallstock_list_chuli():
    print '得到 不包含 ST  和 300 开头的创业板 688开头的科创板股票 的 股票池'
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    starttime = datetime.datetime.now()

    today = starttime.strftime('%Y%m%d')
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    newShangshi = pro.new_share(start_date='20200101', end_date=today)  # 排除 新上市的公司

    news = newShangshi['ts_code']

    tamp = []
    for index, row in data.iterrows():
        name = row['name']
        code = row['ts_code']
        code_300 =  code[0:3]
        print code_300
        if (code == '688278.SH'):
            print "688278"
        if ('ST' not in name  and  code_300 !='300'and code_300 !='688'): # 不包含 ST  和 300 开头的创业板 688开头的科创板股票
            key1 = 1;
            for newcode in news:  # 排除所有新上市的公司
                # print newcode
                if (code == newcode):
                    key1 = 0;


            if( key1):
                tamp.append(row)

    tamp = pd.DataFrame(tamp, columns=['ts_code', 'symbol', 'name', 'area', 'industry', 'list_date'])
    tamp = tamp.reset_index(drop=True)
    tamp.to_csv("allstockcode_No_ST.csv")


'''
得到 不处理任何数据 的 股票池
'''
def getallstock_list():
    print '得到 不处理任何数据 的 股票池'
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    starttime = datetime.datetime.now()

    today = starttime.strftime('%Y%m%d')
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    newShangshi = pro.new_share(start_date='20200101', end_date=today)  # 排除 新上市的公司

    news = newShangshi['ts_code']

    tamp = []
    for index, row in data.iterrows():
        name = row['name']
        code = row['ts_code']
        code_300 = code[0:6]
        # print code_300
        if (code_300 == '688516'):
            print "688516"
            print1(code)
            print1(name)
        if ('ST' not in name ):  # 不包含 ST
            key1 = 1;

            if (key1):
                tamp.append(row)

    tamp = pd.DataFrame(tamp, columns=['ts_code', 'symbol', 'name', 'area', 'industry', 'list_date'])
    tamp = tamp.reset_index(drop=True)
    stockdata_path = BASE_DIR + '/jishu_stock/zYouQianJun/' + 'allstock_list' + ".csv"
    print1(stockdata_path)
    # 3 保存数据
    tamp.to_csv(stockdata_path)

if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()
    # getallstock_list_chuli()
    getallstock_list()
    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds