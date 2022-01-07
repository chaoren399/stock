#!/usr/bin/python
# -*- coding: utf8 -*-
import collections
import csv
import datetime
import time

from jishu_stock.z_tool.duoxiancheng.ModelCode import get_modelcode
from stock.settings import BASE_DIR
import pandas as pd
import tushare as ts


'''
把 list 数据保存为文件, 方便 回测
这个函数要每次写文件都要覆盖之前的, 而不是追加, 且是固定路径.
需求, 回测胜率的时候 chengongs 是成功的结果,
我们要等很久才能给拿出结果, 计算胜率更快, 不用等之前的运算了.

Python txt文件读取写入字典的方法（json、eval）
https://www.cnblogs.com/xiexiaokui/p/10788828.html
'''

path = BASE_DIR + '/jishu_stock/aShengLv/huice_linsh/' + 'result.txt'
def wirteList_to_txt(list):
    file = open(path, 'w')
    file.write(str(list));
    file.close()

def getList_from_txt():
    fr = open(path, 'r+')
    dic = eval(fr.read())  # 读取的str转换为字典

    # print(dic)
    fr.close()
    return dic
