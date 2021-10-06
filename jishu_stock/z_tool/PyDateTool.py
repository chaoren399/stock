#!/usr/bin/python
# -*- coding: utf8 -*-
# for i in range(1, 10)
from datetime import datetime

from jishu_stock.Tool_jishu_stock import print1

'''
判断 2 个日期 相差 几天
    enddate = '20210709'
    startdate = '20210609'
'''
def get_date1_date2_days(startdate, enddate):
    # print1(startdate)
    # print1(enddate)
    startdate=str(startdate)
    enddate=str(enddate)
    start_day = datetime(int(startdate[0:4]), int(startdate[4:6]), int(startdate[6:8]))
    end_day = datetime(int(enddate[0:4]), int(enddate[4:6]), int(enddate[6:8]))
    return (end_day - start_day).days



if __name__ == '__main__':
    enddate = '20210720'
    startdate = '20210719'
    print get_date1_date2_days(startdate,enddate)
