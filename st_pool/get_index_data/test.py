#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts
import sys
import pandas as pd
from jishu_stock.Tool_jishu_stock import dingshi_ceshi
from st_pool.get_index_data.JiaoYiE.GetDayliyJiaoYiE import get_HS_index_data
from stock.settings import BASE_DIR

if __name__ == '__main__':

    df = get_HS_index_data() # 下载数据
    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    df = df.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。


    # print df
    data = []
    for index, row in df.iterrows():
        date = row['trade_date'] # '20190116'

        amount = round(row['amount'] /1000000000,2) # 单位 万亿 保留 2 位有效数字
        xx = [int(date), amount]

        data.append(xx)

    print data