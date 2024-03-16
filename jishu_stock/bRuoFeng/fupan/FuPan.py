#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import sys

from jishu_stock.z_tool.PyDateTool import getMonthNumber

reload(sys)
sys.setdefaultencoding('utf8')

from stock.settings import BASE_DIR
import pandas as pd


# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)


'''
每天 复盘 的时候 用来排序的

'''
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

    yuefen = str(getMonthNumber())

    path_dir = BASE_DIR + '/jishu_stock/bRuoFeng/data/' + yuefen + '/'
    path_dir_out= BASE_DIR + '/jishu_stock/bRuoFeng/data_out/' + yuefen + '/' # 输出目录

    print  '输出目录'
    print path_dir_out

    if not os.path.exists(path_dir_out): #如果文件夹不存在就创建
        os.mkdir(path_dir_out)

    files=[]
    for filename in os.listdir(path_dir):
        files.append(filename)
    files.sort() # 对目录里的文件名 排序

    print files[-1]
    filename_day = files[-1]  #取出最后一个文件的名字

    path = path_dir+ filename_day   # 每天导出的数据目录 '/jishu_stock/bRuoFeng/data/2022年6月3日.csv'
    data = pd.read_csv(path,sep=',',encoding='GBK',header=0)
    # 2 取出重要的列数据
    # data = data.iloc[0:10]  # 前6行

    data=data.iloc[:, [ 1,3,10,4,2]]  # .iloc为按位置索引提取 , # 涨停原因为 4
    data = data.dropna(axis=0, how='any')  # 删除表中含有任何NaN的行
    data1 = data.reset_index(drop=True)

    # 3 重新组合数据
    df = pd.DataFrame(columns=['code', 'lianban', 'fengbantime','yuanyin','name'])
    df['code'] = data1.iloc[:,0]
    df['lianban'] = data1.iloc[:,1]
    df['fengbantime'] = data1.iloc[:,2]
    df['yuanyin'] = data1.iloc[:,3]
    df['name'] = data1.iloc[:,4]

    #4 按照涨停原因 排序

    #(1)  把涨停原因 按照; 来分组,
    #https://blog.csdn.net/qq_45476428/article/details/124069962

    def substrings_in_string(string2):
        string2= str(string2)
        string3=string2.split("。")

        return string3[0]

    df['yuanyin_chuli'] = df['yuanyin'].map(lambda x: substrings_in_string(x))

    #(2) 把首板 改成 1

    def gaishouban(string):
        ss=string
        if(string =='首板'):
            ss='="1"'

        return ss

    df['lianban'] = df['lianban'].map(lambda x: gaishouban(x))

    #(3) 把封板时间放到 名称后边
    df['names'] = df['name']+df['fengbantime']


    df = df.sort_values(by='yuanyin', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    df = df.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。



    # 5 把涨停原因一样的 分组

    '''
    
    https://blog.csdn.net/June19/article/details/115506230
  
    groups = data.groupby(data['color'])  # 按“color”列的值分为多个文件
    # 比如color列有“red, yellow, green”三个不同类型的值，则会分为red.csv; yellow.csv; green.csv三个文件。 
    for group in groups:
        group[1].to_csv('../data_filepath/{}.csv'.format(str(group[0])), index=False, encoding='utf-8')
    
    '''


    df_out= pd.DataFrame()
    groups = df.groupby(df['yuanyin_chuli'])  # 按“yuanyin”列的值分为多个文件
    for group in groups:
        len_group = len(group[1])
        df2= group[1].sort_values(by='fengbantime', axis=0, ascending=True)  # 按照日期 从旧到新 排序 # 按照 涨停时间 来排序

        df2= df2.sort_values(by='lianban', axis=0, ascending=False)

        if(len_group>2): # 只对 涨停原因 大于 2 的 有效
            df_out=df_out.append(df2,ignore_index=True)

    #6 重新 组合数据,输出

    # df_out1 = pd.DataFrame(columns=['code', 'lianban', 'fengbantime','yuanyin','name'])
    df_out1 = pd.DataFrame(columns=['code', 'lianban', 'names','yuanyin_chuli'])

    df_out1['code']=df_out['code']
    df_out1['lianban']=df_out['lianban']
    df_out1['names']=df_out['names']
    df_out1['yuanyin_chuli']=df_out['yuanyin_chuli']

    print df_out1.iloc[0:2]
    path_out = path_dir_out +'排序' +filename_day
    df_out1.to_csv(path_out)




if __name__ == '__main__':
    test()