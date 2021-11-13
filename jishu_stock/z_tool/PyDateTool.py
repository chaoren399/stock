#!/usr/bin/python
# -*- coding: utf8 -*-
# for i in range(1, 10)
from datetime import datetime


''''
2021-07-09 到 20210709

'''
def riqi_geshi_zhuanhua1(s):
    # s = '2019-01-20'
    ss= datetime.strptime(s, '%Y-%m-%d')  # 2019-01-20 00:00:00
    day = datetime.strftime(ss, '%Y%m%d')
    return day

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
    # print get_date1_date2_days(startdate,enddate)
    date1='2021-07-09'
    riqi_geshi_zhuanhua1(date1)