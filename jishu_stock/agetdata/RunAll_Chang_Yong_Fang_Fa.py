#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
import os

from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian1 import get_all_JGZS_KanZhangYinXian1
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian2 import get_all_JGZS_KanZhangYinXian2
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian4 import get_all_JGZS_KanZhangYinXian4
from jishu_stock.JiaGeZhongShu.JGZS_QiangShiGu import get_all_JGZS_QiangShiGu
from jishu_stock.LongZhan_YuYe.LongZhanYuYe import isAn_LongZhanYuYe_model
from jishu_stock.Tool_jishu_stock import get_all_codes_from_tool
from jishu_stock.zGetStockCode.Xmind.get_Xmind_Data import getXmindData
from stock.settings import BASE_DIR

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_parent_dir_name = os.path.dirname(os.path.dirname(current_dir))
# print current_dir
print(parent_parent_dir_name)
sys.path.append(parent_parent_dir_name)

import pandas as pd

def f1():
    localpath1 = '/jishu_stock/z_stockdata/data1/'

    stock_codes = get_all_codes_from_tool()  # 获取所有股票代码

    for index, item in enumerate(stock_codes):
        # print index, item
        stock_code = item
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:30]  # 前6行
        data6_1 = df.iloc[0:132]  # 前6行
        data6_1 = df.iloc[0:136]  # 前6行
        # data6_1 = df.iloc[2:136]  # 前6行
       #  8 龙战于野
        isAn_LongZhanYuYe_model(data6_1, stock_code)




def f():
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_JGZS_QiangShiGu(localpath1)
    # 3  看涨阴线1 上涨初期
    get_all_JGZS_KanZhangYinXian1(localpath1)
    # 4 看涨阴线 2 回调位置
    get_all_JGZS_KanZhangYinXian2(localpath1)

    #5 看涨阴线4
    get_all_JGZS_KanZhangYinXian4(localpath1)
    getXmindData()


if __name__ == '__main__':

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_JGZS_QiangShiGu(localpath1)
    f1()
