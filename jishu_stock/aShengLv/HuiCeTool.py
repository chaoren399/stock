#!/usr/bin/python
# -*- coding: utf8 -*-
import collections
import csv
import datetime
import time

from jishu_stock.Tool_jishu_stock import get_Stock_Name_byKanzhanghuice
from jishu_stock.z_tool.PyDateTool import getDayNumberYMD

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


'''
回测工具类

'''


'''
跟具当看涨做张第2个阳线， 获取下周买入价格，第1,2,3,4周收盘价格
'''

def get_oneweekOpenClosePrice_twoweekClose(code,date):
    # ts_code='603389.SH'
    ts_code=code
    # start_date='20231105'
    start_date=date
    today = getDayNumberYMD()
    # print today
    end_date=today
    # df = ts.pro_bar(ts_code='000155.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20201225')
    # df = ts.pro_bar(ts_code=ts_code, adj='qfq', freq='W', start_date=start_date, end_date=end_date)
    df=''
    try:
        # 这里是可能会出错的代码

        df = ts.pro_bar(ts_code=ts_code, adj='qfq', freq='W', start_date=start_date, end_date=end_date)
        lendf = len(df)
        data7_1 = df.iloc[lendf - 4:lendf]  # 1 年有 50 周

        data1 = data7_1

        data1 = data1.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

        # print df
        huice_info = str(date) + get_Stock_Name_byKanzhanghuice(code) + ',' + code + ','
        # print data1
        for index, row in data1.iterrows():
            if (index == 0):
                huice_info = huice_info + str(row['open']) + ',' + str(row['close']) + ','
                # print huice_info
            if (index == 1):
                huice_info = huice_info + str(row['close']) + ','
            if (index == 2):
                huice_info = huice_info + str(row['close']) + ','
            if (index == 3):
                huice_info = huice_info + str(row['close'])

        # print huice_info
        # print '--------------------------+++++++--'
        return huice_info

        '''
        日期，股票,买入价,第一周卖,第2周卖,第3周卖,第4周卖
        '''
    except Exception as e:
        # 这里处理错误，比如打印错误信息，或者记录日志
        print(e)
        # 接着执行其他代码
    # if(len(df) < 4):
    #     print "get_oneweekOpenClosePrice_twoweekClose + df length < 4"
    #     return 0

def test_feiyada():
    ts_code='000026.SZ'
    start_date='20231112'
    get_oneweekOpenClosePrice_twoweekClose(ts_code,start_date)

if __name__ == '__main__':
    print 'HuiceTool'
    ts_code='603389.SH'
    start_date='20231105'
    # get_oneweekOpenClosePrice_twoweekClose(ts_code,start_date)
    # test_feiyada()
