# -*- coding: utf8 -*-

import tushare as ts
import sys
import pandas as pd


ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
pro = ts.pro_api()
stock_code='002017.SZ'

# df = pro.daily(ts_code=stock_code)
# df = ts.pro_bar(ts_code='002017.SZ', adj='qfq', start_date='20201128', end_date='20201228')
# df = pro.daily(ts_code='002017.SZ', start_date='20201128', end_date='20201228')
df = pro.daily(ts_code='002017.SZ')
df.to_csv("111V.csv")
print df