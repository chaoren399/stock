#!/usr/bin/python
# -*- coding: utf8 -*-

'''

silu

1-xunhuan daima   chazhao meizhipiaozi

'''
import pandas as pd

from stock.settings import BASE_DIR

def getXimndData():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    xmind = BASE_DIR + '/jishu_stock/z_stockdata/xmind.txt'

    path_xmind = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST_xmind.csv'

    df_xmind = pd.DataFrame()
    # path =  '/app/stock/stock/jishu_stock/z_stockdata/qiang_qushi_stocks.csv'
    data = pd.read_csv(path, dtype={'code': str})
    # print data
    xmind_content=''
    with open(xmind, "r") as file:
        xmind_content = file.read()

    # print xmind_content
    for index, row in data.iterrows():
        name=row['name']
        # name='川宁生物'
        if(name in xmind_content):
            df_xmind = pd.concat([df_xmind, pd.DataFrame(row).T])
            print name

    df_xmind.to_csv(path_xmind)





if __name__ == '__main__':
    getXimndData()