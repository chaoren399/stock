#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts
import sys
import pandas as pd
from jishu_stock.Tool_jishu_stock import dingshi_ceshi

if __name__ == '__main__':
    print  "定时测试"
    dingshi_ceshi()
    print float(20) / float(26)