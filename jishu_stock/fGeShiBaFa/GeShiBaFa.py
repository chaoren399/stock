#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt
from stock.settings import BASE_DIR

'''
第一步 : 用  Get_Week_K_data.py 来 得到 周K 线
第二步:   计算 10 周K 线 和 60 周K 线, 葛式八法 需要的
第三步: 找到 葛式八法的点位

'''


'''
判断 2 个数据 是不是 一个正值,一个负值
'''
def isRiJunXianZuHe_2Days_data(data,stock_code):
    data = data.reset_index(drop=True)  # 重新建立索引 ,
    # print data
    if(len(data) ==2):
        a1=data.ix[0]['ma5_13_cha']
        a2=data.ix[01]['ma5_13_cha']
        if( a1 > 0 and a2 <0):
            # print a1
            # print a2
            return 1
        if(a1 <0 and a2 >0):
            # print a1
            # print a2
            return 1;

        return 0;



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_5_13_34_RiJunXian(localpath1=localpath1)
