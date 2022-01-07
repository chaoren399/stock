#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions
from jishu_stock.Tool_jishu_stock import is_small_to_big, print1



'''
齐头并进
判断是不是 太阳花 一样的向上趋势,  
3 跟 K 线不能 相交 ,5 大于 10 大于 20

如果满足 返回 1
data 是从旧到新排序 
number  是从哪个位置开始, 默认是 0

大有 专用
'''

def is5_10_20_XiangShang_dayou(data, number):
    if (data is None or data.empty):
        print '--df.empty--'
        return 0
    len_data = len(data)
    if (len_data == 0):
        print  '--data --is null'
    if (len_data > 0):
        startweizhi = number
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        data1 = data[startweizhi:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

        key_1=1 # 只要有一项不符合就Wie0
        ma5s = []
        ma10s = []
        ma20s = []

        for index, row in data1.iterrows():
            ma5 = row['ma5']
            ma10 = row['ma10']
            ma20 = row['ma20']

            ma5s.append(ma5)
            ma10s.append(ma10)
            ma20s.append(ma20)
            if(ma5 < ma10 or ma5 < ma20 or ma10 < ma20): #,3 跟 K 线不能 相交 ,5 大于 10 大于 20
                key_1=0
                # print1('ma5 < ma10 ')
            # if(not(row['close'] > ma10 and row['open'] > ma10 )): # 且K 线 开盘价和收盘价 不能跌破 10 日均线,
            #     key_1=0


        if (is_small_to_big(ma5s) != 1):  # 判断由大到小是有问题的, 单独写一个  由小到大的函数
            key_1=0
            # print1(ma5s)
        if (is_small_to_big(ma10s) != 1):
            key_1=0
            # print1(ma10s)
        if (is_small_to_big(ma20s) != 1):
            key_1=0
            # print1(ma20s)

        # print1(ma20s)
        return key_1


'''

判断是不是 太阳花 一样的向上趋势, K 线在 10 日均线之上 , 且K 线 开盘价和收盘价 不能跌破 10 日均线,
3 跟 K 线不能 相交 ,5 大于 10 大于 20

如果满足 返回 1
data 是从旧到新排序 
number  是从哪个位置开始, 默认是 0

反客为主 专用
'''

def is5_10_20_XiangShang_fankeweizhu(data, number):
    if (data is None or data.empty):
        print '--df.empty--'
        return 0
    len_data = len(data)
    if (len_data == 0):
        print  '--data --is null'
    if (len_data > 0):
        startweizhi = number
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        data1 = data[startweizhi:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

        key_1=1 # 只要有一项不符合就Wie0
        ma5s = []
        ma10s = []
        ma20s = []

        for index, row in data1.iterrows():
            ma5 = row['ma5']
            ma10 = row['ma10']
            ma20 = row['ma20']

            ma5s.append(ma5)
            ma10s.append(ma10)
            ma20s.append(ma20)
            if(ma5 < ma10 or ma5 < ma20 or ma10 < ma20): #,3 跟 K 线不能 相交 ,5 大于 10 大于 20
                key_1=0
                # print1('ma5 < ma10 ')
            if(not(row['close'] > ma10 and row['open'] > ma10 )): # 且K 线 开盘价和收盘价 不能跌破 10 日均线,
                key_1=0


        if (is_small_to_big(ma5s) != 1):  # 判断由大到小是有问题的, 单独写一个  由小到大的函数
            key_1=0
            # print1(ma5s)
        if (is_small_to_big(ma10s) != 1):
            key_1=0
            # print1(ma10s)
        if (is_small_to_big(ma20s) != 1):
            key_1=0
            # print1(ma20s)

        # print1(ma20s)
        return key_1


'''
5-10-20
判断是不是 太阳花 一样的向上趋势, K 线在 5 日均线之上 , 3 跟 K 线不能 相交 ,且K 线不能跌破 10 日均线

如果满足 返回 1
data 是从旧到新排序 
number  是从哪个位置开始, 默认是 0

一箭双雕专用
'''


def is5_10_20_XiangShang_yijianshuangdiao(data, number):
    if (data is None or data.empty):
        print '--df.empty--'
        return 0
    len_data = len(data)
    if (len_data == 0):
        print  '--data --is null'
    if (len_data > 0):
        startweizhi = number
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        data1 = data[startweizhi:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

        key_1=1 # 只要有一项不符合就Wie0
        ma5s = []
        ma10s = []
        ma20s = []

        for index, row in data1.iterrows():
            ma5 = row['ma5']
            ma10 = row['ma10']
            ma20 = row['ma20']

            ma5s.append(ma5)
            ma10s.append(ma10)
            ma20s.append(ma20)
            if(ma5 < ma10 or ma5 < ma20 or ma10 < ma20):
                key_1=0
                # print1('ma5 < ma10 ')
            if(row['close'] < ma5 ): # 如若 K 线的 收盘价 低于 MA5 日均,那么也失败
                key_1=0




        if (is_small_to_big(ma5s) != 1):  # 判断由大到小是有问题的, 单独写一个  由小到大的函数
            key_1=0
            # print1(ma5s)
        if (is_small_to_big(ma10s) != 1):
            key_1=0
            # print1(ma10s)
        if (is_small_to_big(ma20s) != 1):
            key_1=0
            # print1(ma20s)

        # print1(ma20s)
        return key_1




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
