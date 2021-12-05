#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import *
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from stock.settings import BASE_DIR

'''
给你定 一个数据段, 判断里边有没有熊市末期
比如给定一个月的数据 
如果这个数据集合里边存在熊市末期, 那么返回 1, 否则返回 0 

有了这个工具真的非常 OK
'''
def hasXiongShiMoQi(data):
    len_data=len(data)
    for i in range(0, len_data - 3 + 1):
        # print "i" + str(i )+ "j"+str(i+3)
        if(isXiongShiMoQi(data[i:i + 3])==1):
            return 1
    return 0

'''

需要 3 个数据 
急速下跌熊市末期
(连续至少3根阴线有低开有中/大阴线)
创建日期: 2021年11月21日
修改日期

'''
def isXiongShiMoQi(data):
    if (data is None or data.empty):
        print '--df.empty--isXiongShiMoQi()--'
        return 0

    len_data = len(data)
    if (len_data == 0):
        print '--data --is null--isXiongShiMoQi()'
    if (len_data >= 3):

        data = data.reset_index(drop=True)  # 重新建立索引 ,
        key1=0 # 3 个阴线
        key2=0 # 有低开
        key3=0 # 有中/大阴线

        count=0
        day1_shiti=0
        day2_shiti=0
        day3_shiti=0
        day1_close=0
        day2_open=0
        day2_close=0
        day3_open=0
        # print data



        for index, row in data.iterrows():
            if(index==0 and isYinXian(row)==1):
                count=count+1
                day1_shiti=getShiTiDaXiao(row)
                day1_close=row['close']
            if(index==1 and isYinXian(row)==1):
                count=count+1
                day2_shiti = getShiTiDaXiao(row)
                day2_open=row['open']
                day2_close=row['close']

            if(index==2 and isYinXian(row)==1):
                count=count+1
                day3_shiti = getShiTiDaXiao(row)
                day3_open= row['open']

        if(count==3): # 3 个阴线
            key1=1
            # 有中/大阴线
            if(day1_shiti >1.6 or day2_shiti > 1.6 or day3_shiti > 1.6):
                key3=1

            # 有低开

            if(day2_open< day1_close or day3_open <day2_close):
                key2=1


        if(key1==1 and key2==1 and key3==1):
            return 1

    return 0

