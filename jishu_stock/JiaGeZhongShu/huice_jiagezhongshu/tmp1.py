#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts
import sys

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode
from stock.settings import BASE_DIR
import pandas as pd
import time

if __name__ == '__main__':
    df1 = ts.pro_bar(ts_code='000001.SZ',adj='qfq', start_date='20210801', end_date='20211105')

    print df1[0:2]