# -*- coding: utf8 -*-

import tushare as ts
import sys
import pandas as pd

# res = pd.DataFrame(columns=('ts_code'))
# res = res.append([{'ts_code':'ddd'}], ignore_index=True)
# print res


# res = pd.DataFrame(columns=('lib', 'qty1', 'qty2'))
# res = res.append([{'qty1':10.0}], ignore_index=True)
# print(res.head())

codes=['1','2']

# data_frame = DataFrame(data_array,index=None,columns = ['a','b','c','d'])
sss = pd.DataFrame(codes,columns=['ts_code'])
sss.to_csv("xiadiecodes.csv")