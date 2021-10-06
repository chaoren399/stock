# -*- coding: utf8 -*-

import tushare as ts
import sys
import pandas as pd

# res = pd.DataFrame(columns=('ts_code'))
# res = res.append([{'ts_code':'ddd'}], ignore_index=True)
# print res

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
