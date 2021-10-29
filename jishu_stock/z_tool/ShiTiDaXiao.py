#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR

'''
处理 K线的 函数,  有 实体大小, 上影线长度, 下影线长度
'''


'''
获取 价格中枢的值
价格中枢 = ( 最高价 + 最低价) ÷ 2
'''
def get_jiagezhongshu(row):
    # chazhi = format(((row['high'] + row['low']) / 2) , '.2f')
    chazhi = (row['high'] + row['low']) / 2
    return chazhi

'''
得到阳线的下影线长度
'''
def getyangxian_xiayingxian_daxiao(row):
    chazhi= row['open']-row['low']

    return chazhi
'''
得到阳线的上影线长度
'''
def getyangxian_shangyingxian_daxiao(row):
    chazhi = row['high'] - row['close']

    return chazhi

'''
小十字星 是 0.5 以下
 
 小阴线和小阳线的波动范围一般在0.6--1.5；
 中阴线和中阳线的波动范围一般在1.6-3.5；
 大阴线和大阳线的波动范围在3.6以上。
 
 返回的是  带 2 位数的小数 都是实体.
'''

'''
如果导入不了,可以复制下边的一行
from jishu_stock.z_tool.ShiTiDaXiao import  getShiTiDaXiao
'''

def getShiTiDaXiao(row):

    chazhi = format(((row['close'] - row['open']) / row['open']) * 100, '.2f')

    return abs(float(chazhi))




def test():
    df1 = ts.pro_bar(ts_code='600053.SH',adj='qfq', start_date='20210206', end_date='20211020',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:1]  # 前4行
    print data7_1
    for index, row in data7_1.iterrows():
        print getShiTiDaXiao(row)

    print '  大阴线和大阳线的波动范围在3.6以上'

if __name__ == '__main__':
    test()
