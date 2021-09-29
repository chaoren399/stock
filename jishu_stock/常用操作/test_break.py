#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode
from stock.settings import BASE_DIR


'''
break 终端for循环
'''
def test_break():

    for letter in 'Python':     # 第一个实例
       if letter == 'h':
          break
       print '当前字母 :', letter

if __name__ == '__main__':
    test_break()