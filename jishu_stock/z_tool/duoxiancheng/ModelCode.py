#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from stock.settings import BASE_DIR
import pandas as pd


'''
modelcode 根据传入的模型名字, 获取模型编码
'''
def get_modelcode(modelname):
    # modelname='一箭双雕'
    #/Users/mac/PycharmProjects/gitproject/stock/jishu_stock/z_stockdata/
    path = BASE_DIR + '/jishu_stock/z_stockdata/模型编码.csv'
    data = pd.read_csv(path, sep=',', header=None, engine='python')

    data.columns = ['modelcode', 'name']

    for index, row in data.iterrows():
        modelcode = row['modelcode']
        name = row['name']

        if( modelname == name ):
            return modelcode

    return 'xxxx'



if __name__ == '__main__':

    # modelname = '出水芙蓉'
    modelname = 'XiaoV'
    print get_modelcode(modelname)