#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi

from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)


'''
思路: 
首先 按照日期来遍历 ,每天的涨停板
然后 根据每天涨停板的个股信息 去查询 本次日期向前 的 20 日信息. 的数据

拿到前 10 判断连板数量 (单独一个方法)  第一天不涨停, 第 2 天涨停, 第 3 天涨停 ....

'''

'''
得到某日的涨停股票信息
'''
def get_day_ZTB(date):
    # date= '20190925'
    date= '20220407'
    pro = ts.pro_api()

    # 获取单日统计数据
    # df = pro.limit_list(trade_date=date)

    # 获取某日涨停股票，并指定字段输出
    # df = pro.limit_list(trade_date=date, limit_type='U', fields='trade_date,ts_code,close,first_time,last_time,pct_chg,amp')


    # 获取时间段统计信息
    df = pro.limit_list(start_date='20220320', end_date='20220420',limit_type='U')
    print df



def test_ZhangTingBan():
    pro = ts.pro_api()

    # 获取单日统计数据
    # df = pro.limit_list(trade_date='20190925')

    # 获取某日涨停股票，并指定字段输出
    df = pro.limit_list(trade_date='20190925', limit_type='U', fields='ts_code,close,first_time,last_time,pct_chg')

    # 获取时间段统计信息
    # df = pro.limit_list(start_date='20190920', end_date='20190925')

    print df


if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_ChouMaTuPo(localpath1)

    # test_ZhangTingBan()
    get_day_ZTB('')

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"