#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions
from jishu_stock.Tool_jishu_stock import is_small_to_big, print1

'''
判断 5-13-34 是否是 向上趋势, 如果都是上升趋势 返回 3 如果有一个是上升,其他 2 个不上升,返回 1
data 是从旧到新排序 
number  是从哪个位置开始, 默认是 0
'''
def is5_13_34_XiangShang(data,number):
    if (data is None or data.empty):
        print '--df.empty--'
        return 0
    len_data = len(data)
    if (len_data == 0):
        print  '--data --is null'
    if (len_data >0):
        startweizhi=number
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        data1=data[startweizhi:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        ma5 = []
        ma13 = []
        ma34 = []

        for index, row in data1.iterrows():
            ma5.append(row['ma5'])
            ma13.append(row['ma13'])
            ma34.append(row['ma34'])
        # print1(ma5)
        # print1(ma13)
        # print1(ma34)
        count = 0
        if (is_small_to_big(ma5) == 1): # 判断由大到小是有问题的, 单独写一个  由小到大的函数
            count = count + 1
        if (is_small_to_big(ma13) == 1):
            count = count + 1
        if (is_small_to_big(ma34) == 1):
            count = count + 1

        # print1(count)
        return count
