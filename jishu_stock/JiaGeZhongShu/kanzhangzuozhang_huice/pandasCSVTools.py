#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_parent_dir_name = os.path.dirname(os.path.dirname(current_dir))
# print current_dir
print(parent_parent_dir_name)
sys.path.append(parent_parent_dir_name)

from stock.settings import BASE_DIR
import pandas as pd

def exced_csv_kanzhangjiegou(pathin,pathout,date):
        path= pathin
        print pathin

        names = ['date', 'name', 'code', 'oneopen', 'oneclose', 'twoclose', 'threeclose', 'fourclose']

        data = pd.read_csv(path, dtype={'code': str}, names=names, header=None)
        # data = pd.read_csv(path, dtype={'code': str})
        df = data

        df['Return1'] = (df['oneclose'] - df['oneopen']) / df['oneopen']
        df['Return1'] = df['Return1'].apply(lambda x: round(x, 2))  # 将收益率保留四位小数


        df['Return2'] = (df['twoclose'] - df['oneopen']) / df['oneopen']
        df['Return2'] = df['Return2'].apply(lambda x: round(x, 2))  # 将收益率保留四位小数
        # print df['Return2']
        # print '+++++++++++++++++'

        df['Return3'] = (df['threeclose'] - df['oneopen']) / df['oneopen']
        df['Return3'] = df['Return3'].apply(lambda x: round(x, 2))  # 将收益率保留四位小数


        df['Return4'] = (df['fourclose'] - df['oneopen']) / df['oneopen']
        df['Return4'] = df['Return4'].apply(lambda x: round(x, 2))  # 将收益率保留2位小数
        # df= df.sum()
        # print df
        # 按列求和

        df.loc['Col_sum'] = df.iloc[1:-1, -4:].sum(axis=0).round(2)  # 对0，1行按列求和，生成新行
        # df = df.astype(float).round(2)

        print df


        df.to_csv(pathout)





    # for index, row in data.iterrows():
    #     print row

if __name__ == '__main__':

    pathin='/app/stock/stock/jishu_stock/JiaGeZhongShu/kanzhangzuozhang_huice/huicedata/2023/2023-11-12.csv'
    pathout='/app/stock/stock/jishu_stock/JiaGeZhongShu/kanzhangzuozhang_huice/huicedata/shouyi/2023-11-12-shouyi.csv'
    date='20231112'
    exced_csv_kanzhangjiegou(pathin, pathout, date)