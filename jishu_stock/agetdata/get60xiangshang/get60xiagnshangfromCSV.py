#!/usr/bin/python
# -*- coding: utf8 -*-
import csv
import datetime

import tushare as ts
import sys
import pandas as pd
from jishu_stock.Tool_jishu_stock import dingshi_ceshi, print1
from jishu_stock.z_tool.MyPath import getweekdata_path_with_stockcode
from jishu_stock.z_tool.PyDateTool import getMonthNumber, getDayNumberYMD
from jishu_stock.z_tool.isShangZhang_60Week import  is_60WEEK_ShangZhang_with_number
from stock.settings import BASE_DIR

day_jieguo_path = BASE_DIR + '/jishu_stock/zJieGuo/'+str(getMonthNumber())+'月/' + datetime.datetime.now().strftime(
        '%Y-%m-%d') + '.csv'

'''
把每天处理万的 CSV 文件单独的过滤 符合 60 周向上的数据
'''
def get60_xiangshang_from_csv():
    #1 得到 stockcode
    # df = pd.read_csv(path1, sep=',', header=None, engine='python')
    data = pd.read_csv(day_jieguo_path, dtype={'code': str})

    inpath = BASE_DIR + '/jishu_stock/agetdata/everyday/'  + datetime.datetime.now().strftime(
        '%Y-%m-%d') + '.csv'
    for index,row in data.iterrows():
        modename =  row['modename']
        modecode =  row['modecode']
        info =  row['info']
        stockcode = info.split('**')[1]
        # print1(stockcode)

        # 2 获取周线数据 并判断是不是向上
        if(is_60WEEK_ShangZhang_with_number(stockcode,getDayNumberYMD(),4)==1):
            with open(inpath, 'a') as csvfile:
                fieldnames = ['modecode', 'modename', 'info']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'modecode': modecode, 'modename': modename, 'info': info})

            # print stockcode




if __name__ == '__main__':
    print  "定时测试"
    get60_xiangshang_from_csv()

    # print float(20) / float(26)