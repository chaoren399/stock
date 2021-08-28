#!/usr/bin/python
# -*- coding: utf8 -*-
# for i in range(1, 10)
from datetime import datetime

''''

'''

def riqi():
    i = datetime.datetime.now()
    print ("当前的日期和时间是 %s" % i)
    print ("ISO格式的日期和时间是 %s" % i.isoformat())
    print ("当前的年份是 %s" % i.year)
    print ("当前的月份是 %s" % i.month)
    print ("当前的日期是  %s" % i.day)
    print ("dd/mm/yyyy 格式是  %s/%s/%s" % (i.day, i.month, i.year))
    print ("当前小时是 %s" % i.hour)
    print ("当前分钟是 %s" % i.minute)
    print ("当前秒是  %s" % i.second)

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print datetime.datetime.now().strftime('%Y-%m-%d')
'''
当前日期 减去 20 个天

'''
def  Riqi_jia_3tian():
    # !/usr/bin/python
    # coding=UTF-8
    import datetime
    day1riqi = '20210809'
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    # the_date = datetime.datetime(y, m, d)
    result_date = cur_day + datetime.timedelta(days=-30)
    # result_date = result_date.strftime('%Y-%m-%d')
    result_date = result_date.strftime('%Y%m%d')
    print result_date


'''
判断 2 个日期 相差 几天
'''
def Riqi_xiangcha_jitian():
    cur_day = datetime(2019, 07, 11)
    next_day = datetime(2019, 7, 31)
    if ((next_day - cur_day).days > 10):
        print((next_day - cur_day).days)  # 1

    day1riqi = '20210709'
    day2riqi = '20210609'
    # print day[0:4]
    # print day[4:6]
    # print day[6:8]
    # cur_day = datetime(20210709)
    # next_day = datetime(20210809)
    print((next_day - cur_day).days)  # 1

    cur_day = datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    next_day = datetime(int(day2riqi[0:4]), int(day2riqi[4:6]), int(day2riqi[6:8]))
    print((next_day - cur_day).days)  # 1
    if ((cur_day - next_day).days > 7):
        print("ok1")

''''
python计算，指定的日期，后n天，前n天是哪一天


'''
def test():
    # !/usr/bin/python
    # coding=UTF-8
    import datetime

    def getday(y=2017, m=8, d=15, n=0):
        the_date = datetime.datetime(y, m, d)
        result_date = the_date + datetime.timedelta(days=n)
        d = result_date.strftime('%Y-%m-%d')
        return d

    print getday(2017, 8, 15, 21)  # 8月15日后21天
    print getday(2017, 9, 1, -10)  # 9月1日前10天


if __name__ == '__main__':
    # Riqi_xiangcha_jitian()
    Riqi_jia_3tian()
    # test()
