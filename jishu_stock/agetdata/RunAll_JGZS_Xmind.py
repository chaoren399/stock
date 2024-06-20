#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
import os

from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian1 import isAn_JGZS_KanZhangYinXian1_model
from jishu_stock.JiaGeZhongShu.JGZS_QiangShiGu import isAn_JGZS_QiangShiGu_model
from jishu_stock.Tool_jishu_stock import writeLog_to_txt_nocode
from jishu_stock.zGetStockCode.Xmind.get_Xmind_Data import getXmindData

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_parent_dir_name = os.path.dirname(os.path.dirname(current_dir))
# print current_dir
print(parent_parent_dir_name)
sys.path.append(parent_parent_dir_name)

from stock.settings import BASE_DIR
import pandas as pd

def get_all_JGZS_KanZhangYinXian1_KanZhangQiangShiGu():
    info1=  '--价格中枢-all start--   '
    writeLog_to_txt_nocode(info1)
    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST_xmind.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        # stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        try:
            df = pd.read_csv(stockdata_path, index_col=0)
            df = df.reset_index(drop=False)

            data6_1 = df.iloc[0:6]  # 前6行
            # data6_1 = df.iloc[2:8]  # 前6行
            # data6_1 = df.iloc[20:32]  # 前6行
            len1 = len(data6_1)
            isAn_JGZS_KanZhangYinXian1_model(data6_1, stock_code)
            isAn_JGZS_QiangShiGu_model(data6_1, stock_code)
        except:
            print  'stock_code is null = ' + str(stock_code)


if __name__ == '__main__':
    # G8M2_yijianyunxing()
    # xmind = BASE_DIR + 'jishu_stock/agetdata/xmind.txt'  #  把 xmind 数据 粘贴到这个文件， 直接运行 getXmindData()
    getXmindData()
    get_all_JGZS_KanZhangYinXian1_KanZhangQiangShiGu()


