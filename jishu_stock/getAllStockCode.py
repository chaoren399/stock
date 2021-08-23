#!/usr/bin/python
# -*- coding: utf8 -*-
import tushare as ts
import sys
import pandas as pd

reload(sys)

sys.setdefaultencoding('utf8')

def  getdata():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()

    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    newShangshi = pro.new_share(start_date='20200101', end_date='20210818')  # 排除 新上市的公司

    news = newShangshi['ts_code']

    tamp = []
    for index, row in data.iterrows():
        name = row['name']
        code = row['ts_code']
        if (code == '688278.SH'):
            print "688278"
        if ('ST' not in name):
            key1 = 1;
            for newcode in news:  #
                # print newcode
                if (code == newcode):
                    key1 = 0;
            if( key1):
                tamp.append(row)

    tamp = pd.DataFrame(tamp, columns=['ts_code', 'symbol', 'name', 'area', 'industry', 'list_date'])
    tamp = tamp.reset_index(drop=True)
    tamp.to_csv("allstockcode_No_ST.csv")

if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()
    getdata()
    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds