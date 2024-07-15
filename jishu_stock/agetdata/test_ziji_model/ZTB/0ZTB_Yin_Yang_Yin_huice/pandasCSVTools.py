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
'''
ZTB_Yin_Yang_Yin_jieguo
'''
def exced_csv_ZTB_Yin_Yang_Yin_jieguo(pathin,pathout,date):
        path= pathin
        print pathin

        names = ['date', 'name', 'code', 'oneopen', 'oneclose']

        data = pd.read_csv(path, dtype={'code': str}, names=names, header=None)
        # data = pd.read_csv(path, dtype={'code': str})
        df = data

        df['Return1'] = (df['oneclose'] - df['oneopen']) / df['oneopen']
        df['Return1'] = df['Return1'].apply(lambda x: round(x, 2))  # 将收益率保留四位小数



        # df= df.sum()
        # print df
        # 按列求和

        # df.loc['Col_sum'] = df.iloc[1:-1, -4:].sum(axis=0).round(2)  # 对0，1行按列求和，生成新行
        # df = df.astype(float).round(2)

        print df


        df.to_csv(pathout)





    # for index, row in data.iterrows():
    #     print row

if __name__ == '__main__':

    pathin='/app/stock/stock/jishu_stock/agetdata/test_ziji_model/ZTB/0ZTB_Yin_Yang_Yin_huice/huicedata/1.csv'
    pathout='/app/stock/stock/jishu_stock/agetdata/test_ziji_model/ZTB/0ZTB_Yin_Yang_Yin_huice/huicedata/out.csv'
    date='20231112'
    exced_csv_ZTB_Yin_Yang_Yin_jieguo(pathin, pathout, date)