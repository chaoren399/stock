#!/usr/bin/python
# -*- coding: utf8 -*-

'''

silu

1-xunhuan daima   chazhao meizhipiaozi

'''
import pandas as pd

from stock.settings import BASE_DIR


def tihuan():
    path = BASE_DIR + '/jishu_stock/z_stockdata/allstockcode_all.csv'
    # path =  '/app/stock/stock/jishu_stock/z_stockdata/qiang_qushi_stocks.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        name=row['name']
        code_name=row['name']+'-'+row['ts_code']
        search_text = name
        replace_text = code_name
        tihuan_str(search_text, replace_text)
        print code_name
        # print row['ts_code']
        # print row['name']

        # stock_code = row['代码']

def tihuan_str(search_text,replace_text):
    # search_text='中文在线'
    # replace_text='中文在线-22233'

    path='/app/stock/stock/jishu_stock/zGetStockCode/TiCaiKu/ticat1.txt'

    # 打开文件并读取内容
    # with open(path, "r", encoding="utf-8") as file:
    with open(path, "r") as file:
        content = file.read()

    # 使用 replace() 方法替换文本
    new_content = content.replace(search_text, replace_text)

    # 将新内容写回文件
    with open(path, "w") as file:
    # with open(path, "w", encoding="utf-8") as file:
        file.write(new_content)




if __name__ == '__main__':
    search_text='中文在线'
    replace_text='中文在线-22233'
    # tihuan_str(search_text, replace_text)

    tihuan()

    # tihuan()