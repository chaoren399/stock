#!/usr/bin/python
# -*- coding: utf8 -*-


'''
SH601899
SZ000400
'''
import pandas as pd




def getSockCode_from_SZSH601899(code):
    if ('SZ' in code ):
        # print code
        sz=code.split('SZ')
        code= str(sz[1]) +'.SZ'
        # print sz[0]
        return code
    elif ('SH' in code):
        sh = code.split('SH')
        code = str(sh[1]) +'.SH'
        return code
    return None


def test():

    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    path = '/jishu_stock/z_stockdata/qiang_qushi_stocks.csv'

    data = pd.read_csv(path, dtype={'code': str})
    all_count=0
    for index, row in data.iterrows():
        code = row['代码']
        # stock_code = row['ts_code']
        # print row
        code = getSockCode_from_SZSH601899(code)
        if(code):
            print code

if __name__ == '__main__':
    test()