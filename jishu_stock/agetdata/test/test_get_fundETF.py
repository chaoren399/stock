#!/usr/bin/python
# -*- coding: utf8 -*-

import tushare as ts




if __name__ == '__main__':
    pro = ts.pro_api()

    df = pro.fund_basic(market='E')
    print df