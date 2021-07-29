#!/usr/bin/python
# -*- coding: utf8 -*-

import tushare as ts
import pandas as pd
from pandas import DataFrame

from stock.settings import BASE_DIR
import sys

reload(sys)

sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    path = BASE_DIR + '/jishu_stock/七星落长空/data/stockcodelist.csv'
    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        print row['ts_code']
    # print data