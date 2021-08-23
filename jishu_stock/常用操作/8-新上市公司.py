#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR

'''
IPO新股列表
https://waditu.com/document/2?doc_id=123
'''
ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

pro = ts.pro_api()

df = pro.new_share(start_date='20200101', end_date='20210818')

print  df['ts_code']