#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import pandas as pd
import tushare as ts
import time

''''
换手率  turnover_rate
根据起始时间 得到总的换手率
https://tushare.pro/document/2?doc_id=109
'''

def get_HuanshouLv(ts_code, start_date,end_date):

    #持仓量_周线开始=20211224-结束=20220304--中间值=12.32--大于7个----换手率100----纵横通信**603602.SH
    # 换手率tor，量比vr

    df = ts.pro_bar(ts_code=ts_code, start_date=start_date, end_date=end_date, factors=['tor', 'vr'])
    turnover_rate_sum = df.iloc[:, -2].sum()
    # print turnover_rate_sum
    return turnover_rate_sum


if __name__ == '__main__':
    ts_code = '603602.SH'
    start_date = '20220304'
    end_date = '20220304'
    get_HuanshouLv(ts_code,start_date,end_date)