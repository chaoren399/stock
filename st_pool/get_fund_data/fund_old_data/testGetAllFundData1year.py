#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import requests
import time

import pandas as pd

from st_pool.get_fund_data.fund_old_data.get_fund_old_data import get_urls
from stock.settings import BASE_DIR

def test():
        fundpool_path = BASE_DIR + '/st_pool/get_fund_data/基金池.csv'
        df_1 = pd.read_csv(fundpool_path, dtype=object)
        codes = df_1.iloc[:,1].values

        info = []
        # codes = ['000172']
        # codes = ['000172','000577','110031']
        i = 0;
        str1 = ''
        for code in codes:
            time.sleep(10)  #//睡觉
            x = get_urls(code)
            # x = get_urls_fundata_5yeas(code) #获取 5 年基金数据

if __name__ == '__main__':
    test()
