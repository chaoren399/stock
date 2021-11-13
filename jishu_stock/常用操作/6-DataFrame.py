# -*- coding: utf8 -*-

import tushare as ts
import sys
import pandas as pd

# res = pd.DataFrame(columns=('ts_code'))
# res = res.append([{'ts_code':'ddd'}], ignore_index=True)
# print res


'''' 
根据日期过滤 

df.loc['2021-10-31': '2021-10-10']

如果不可以, 先把 索引改为日期型的:
    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)  有的时候 数据本来就是以日期为索引的,
    
    data = data.reset_index(drop=False)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。


'''

'''
    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    
'''

'''

    df = pd.DataFrame(columns=['姓名', '年龄', '性别'])
    print(df)
    line = {'姓名': '张三', '年龄': 24, '性别': '男'}
    df = df.append(line, ignore_index=True)
    print(df)
'''

# res = pd.DataFrame(columns=('lib', 'qty1', 'qty2'))
# res = res.append([{'qty1':10.0}], ignore_index=True)
# print(res.head())

codes=['1','2']

# data_frame = DataFrame(data_array,index=None,columns = ['a','b','c','d'])
sss = pd.DataFrame(codes,columns=['ts_code'])
sss.to_csv("xiadiecodes.csv")


def test():
    Qiang_stock = pd.DataFrame()
    Qiang_stock.append([{'ts_code': '1111'}], ignore_index=True)
    print Qiang_stock

if __name__ == '__main__':
    # test()
    df = pd.DataFrame(columns=['姓名'])
    print(df)
    line = {'姓名': '张三'}
    df = df.append(line, ignore_index=True)
    print(df)
