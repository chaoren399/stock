#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from stock.settings import BASE_DIR

import tushare as ts
import pandas as pd


# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)
'''
 #原始数据
="",代码,名称,连板数,涨停原因,开盘涨幅,当日涨幅,近10日最高涨幅,近10日涨幅,首次封板,最后封板,当日价格,攻击波,回头波,次日开盘涨幅,次日涨幅,涨停类型,涨停因子,开板数,封单量,当日换手,最新五星买卖点,最新红黄白买卖点,最新神秘C点买卖点,最新智能亮点,几天几板,所属题材,流通市值,总市值

'''

'''
#转化后数据

代码, 连板数, 封停时间, 涨停原因

'''
def test():
    #1读取 CSV 文件

    path = BASE_DIR + '/jishu_stock/bRuoFeng/data/2022年6月3日.csv'
    data = pd.read_csv(path,sep=',',encoding='GBK',header=0)
    # 2 取出重要的列数据
    # data = data.iloc[0:10]  # 前6行
    data=data.dropna(axis=0, how='any') #删除表中含有任何NaN的行
    data=data.iloc[:, [ 1,3,10,4]]  # .iloc为按位置索引提取 , # 涨停原因为 4
    data1 = data.reset_index(drop=True)

    # 3 重新组合数据
    df = pd.DataFrame(columns=['code', 'lianban', 'fengbantime','yuanyin'])
    df['code'] = data1.iloc[:,0]
    df['lianban'] = data1.iloc[:,1]
    df['fengbantime'] = data1.iloc[:,2]
    df['yuanyin'] = data1.iloc[:,3]

    #4 按照涨停原因 排序

    #(1)  把涨停原因 按照; 来分组,
    #https://blog.csdn.net/qq_45476428/article/details/124069962

    def substrings_in_string(string2):
        string2= str(string2)
        # print string2
        string3=string2.split("。")

        return string3[0]

    df['yuanyin_chuli'] = df['yuanyin'].map(lambda x: substrings_in_string(x))

    df = df.sort_values(by='yuanyin', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    df = df.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

    # print df['yuanyin_chuli']


    # 5 把涨停原因一样的 分组

    '''
    
    https://blog.csdn.net/June19/article/details/115506230
  
    groups = data.groupby(data['color'])  # 按“color”列的值分为多个文件
    # 比如color列有“red, yellow, green”三个不同类型的值，则会分为red.csv; yellow.csv; green.csv三个文件。 
    for group in groups:
        group[1].to_csv('../data_filepath/{}.csv'.format(str(group[0])), index=False, encoding='utf-8')
    
    '''

    path1=  BASE_DIR + '/jishu_stock/bRuoFeng/outdata'


    df_out= pd.DataFrame()
    groups = df.groupby(df['yuanyin_chuli'])  # 按“yuanyin”列的值分为多个文件
    for group in groups:
        len_group = len(group[1])
        # print  len(group[1])
        # print group[0]
        df2= group[1].sort_values(by='fengbantime', axis=0, ascending=True)  # 按照日期 从旧到新 排序 # 按照 涨停时间 来排序

        if(len_group>4):
            df_out=df_out.append(df2,ignore_index=True)
            # print group[1]
            print df_out
            # print df2

            # group[1].to_csv(path1+'/{}.csv'.format(str(group[0])), index=False, encoding='utf-8')

    df_out.to_csv('ss.csv')
    # df['sort_id'] = df['yuanyin_chuli'].groupby(df['fengbantime']).rank()

    # df['paixu'] = df.groupby('yuanyin_chuli',axis=0)['fengbantime'].rank(ascending=False)
    # print  df

    # print df['yuanyin']

    # for index, row in data.iterrows():
        # print row



if __name__ == '__main__':
    test()