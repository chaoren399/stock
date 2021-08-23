#!/usr/bin/python
# -*- coding: utf8 -*-
import tushare as ts


if __name__ == '__main__':
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    #查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()


    df = pro.daily(ts_code='603393.SH', start_date='20210701', end_date='20210727')
    data7_1 = df.iloc[0:7]  # 前2行
    print data7_1