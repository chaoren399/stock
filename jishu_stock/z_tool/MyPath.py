#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from stock.settings import BASE_DIR

'''
处理 程序的所有 路径问题
'''



'''
path1 = BASE_DIR + '/jishu_stock/zJieGuo/12月/' + datetime.datetime.now().strftime(
        '%Y-%m-%d') + '.csv'
'''



'''
# 日数据的目录 ,后期方便更新
根据 stock_code 的到 日线的路径 path
localpath1 = '/jishu_stock/stockdata/data1/'
stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
'''

def getdaydata_path_with_stockcode(stock_code):
    localpath1 = '/jishu_stock/stockdata/data1/'
    DayData_DIR = BASE_DIR + localpath1 + stock_code + ".csv"

    return DayData_DIR

'''
# 周数据的目录 ,后期方便更新
根据 stock_code 的到 周线的路径
WeekData_DIR=  BASE_DIR + '/jishu_stock/stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
'''

def getweekdata_path_with_stockcode(stock_code):
    WeekData_DIR = BASE_DIR + '/jishu_stock/stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    return WeekData_DIR


if __name__ == '__main__':
    print  "定时测试"
    # dingshi_ceshi()

    # print float(20) / float(26)