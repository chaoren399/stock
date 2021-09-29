#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

from stock.settings import BASE_DIR
import pandas as pd
import tushare as ts



''''
东方财富 导出的数据代码没有 后缀  只能这样处理

批量处理
把 000809 这样的代码 转化为 000809.SZ 

列名 自己加上: ts_code

'''
def stock_code_zhuanhuan_dongfangcaifu():

    # no_houzhui_path= BASE_DIR + '/jishu_stock/stockdata/z_code/小树股票池_NO_HOUZHUI.csv'
    no_houzhui_path= BASE_DIR + '/jishu_stock/stockdata/z_code/有钱君股票池_NO_HOUZHUI.csv'
    data1 = pd.read_csv(no_houzhui_path,dtype='object')

    data_list=[]
    for index, row in data1.iterrows():
        # print row['ts_code']
        code_with_houzhui= get_houzhui_code(row['ts_code'])
        if(not  code_with_houzhui == 0):
            data_list.append(code_with_houzhui)


    name = ['ts_code']
    test = pd.DataFrame(columns=name,data=data_list)  # 数据有1列，列名为ts_code

    print(test)
    test.to_csv('testcsv.csv', encoding='gbk',index = False)



'''
根据 code 得到 code.SZ
把 000809 这样的代码 转化为 000809.SZ 
'''
def get_houzhui_code(code):
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    data = pd.read_csv(path)
    for index, row in data.iterrows():
        code_no_houzhui=row['ts_code'][0:6]
        if(code ==code_no_houzhui):
            return  row['ts_code']

    return 0


if __name__ == '__main__':
    stock_code_zhuanhuan_dongfangcaifu()