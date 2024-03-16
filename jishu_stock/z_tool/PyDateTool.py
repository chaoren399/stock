#!/usr/bin/python
# -*- coding: utf8 -*-
# for i in range(1, 10)
from datetime import datetime


'''
获取 之前 -30 , 1 ,2 3,天之前的日期

之前的是 负数
之后的是 正数
'20210813'

getRiQi_Befor_Ater_Days('20210813',-3)
'''
def get_date_Befor_Ater_Days(date,numdays):
    if(date):
        day1riqi = str(date)
        # print day1riqi
        import datetime
        cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
        result_date = cur_day + datetime.timedelta(days=numdays)
        try:
            result_date = result_date.strftime('%Y%m%d')
        except Exception as e:
            print e


        return result_date


# 处理日期 YYYYMMDD  把 2018-01-07  转化为  20180107
# df_week['trade_date'] = df_week['trade_date'].astype(str).replace('-', '')

'''
得到当天的日期
%Y%m%d
'''
def getDayNumberYMD():
    starttime = datetime.now()
    today = starttime.strftime('%Y%m%d')
    return today


'''
得到当天的日期 %Y-%m-%d
'''
def getDayNumberY_M_D():
   return datetime.datetime.now().strftime('%Y-%m-%d')

'''
得到当前的月份
'''
def getMonthNumber():

    return datetime.now().month


''''
2021-07-09 到 20210709

'''
def riqi_geshi_zhuanhua1(s):
    # s = '2019-01-20'
    ss= datetime.strptime(s, '%Y-%m-%d')  # 2019-01-20 00:00:00
    day = datetime.strftime(ss, '%Y%m%d')
    return day
'''
2022年06月05日 转化:
/Users/mac/PycharmProjects/gitproject/stock/jishu_stock/bRuoFeng/zhangtingkaiban/zhangtingkaiban.py
ate_chuli()

'''

'''
输入日期 格式: 2022年06月05日

处理日期 , 如果是周五,就要 +3, 其他的+1
'''
def date_chuli_1(date):
    import re
    s = date.decode('utf-8')  # 举个栗子是字符串s，为了匹配下文的unicode形式，所以需要解码
    p = re.compile(ur'[\u4e00-\u9fa5]')  # 这里是精髓，[\u4e00-\u9fa5]是匹配所有中文的正则，因为是unicode形式，所以也要转为ur

    year=int( p.split(s)[0])  # 使用re库的split切割
    yue = int(p.split(s)[1] ) # 使用re库的split切割
    day =int (p.split(s)[2] ) # 使用re库的split切割
    from datetime import datetime
    # christmas = datetime(2013, 2, 25)
    christmas = datetime(year, yue, day)
    date_YMD= christmas.strftime('%Y%m%d')


    import datetime
    # zhouji = datetime.date(year,yue, day).isoweekday()
    zhouji = datetime.date(year,yue, day).isoweekday()

    date_out=''
    if(zhouji ==5):

        date_out = get_date_Befor_Ater_Days(date_YMD, 3)
        # print date_out
    else:
        date_out = get_date_Befor_Ater_Days(date_YMD, 1)

    # print date_out
    return date_out

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