#!/usr/bin/python
# -*- coding: utf8 -*-
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR


df = ts.pro_bar(ts_code='300068.SZ', start_date='20210628', end_date='20210728', ma=[5, 13, 34])
df.to_csv("5.csv")
