#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

import tushare as ts
import sys
import pandas as pd
from jishu_stock.Tool_jishu_stock import dingshi_ceshi


'''
如何优雅高效的撸数据？
https://tushare.pro/document/1?doc_id=230

'''

import tushare as ts

pro = ts.pro_api()

# start_date = '20200701'
# end_date = '20211201'


ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
#在循环提取数据时，首先我们可以通过交易日历拿到一段历史的交易日。

#获取20200101～20200401之间所有有交易的日期
df = pro.trade_cal(exchange='SSE', is_open='1',
                            start_date='20200701',
                            end_date='20211201',
                            fields='cal_date')

# print(df.head())

df = pro.daily(trade_date='20200701')
print df

#循环过程中，为了保持数据提取的稳定性，可以先建立一个专门的函数，实现一个重试机制：

def get_daily(self, ts_code='', trade_date='', start_date='', end_date=''):
    for _ in range(3):
        try:
            if trade_date:
                df = self.pro.daily(ts_code=ts_code, trade_date=trade_date)
            else:
                df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
                time.sleep(1)
        else:
                return df

# 然后通过在循环中调取数据：
for date in df['cal_date'].values:
     df = get_daily(date)
     print df

# if __name__ == '__main__':
#     print  "定时测试"
#     dingshi_ceshi()
#     print float(20) / float(26)