#!/usr/bin/python
# -*- coding: utf8 -*-


'''
判断 row 是不是涨停板, 返回 1 是涨停板, 返回 0 不是涨停板

只做 00 60 开头的 股票
'''



def isDieTingBan_pro(row):
    '''
    60  00 开头的 10%

    30 68 开头的 20%

    '''
    NUM = 0.1
    # print row
    # 最低价与开盘价相同，股票在这段时间内没有下跌
    low_close=abs(row['low']-row['close'])
    high_open=abs(row['high']-row['open'])
    # print  'low_close=' + str(low_close)
    # print  'high_open=' + str(high_open)



    pct_chg = abs(row['pct_chg'])
    # print "pct_chg" +str(pct_chg)

    key=0
    if(pct_chg > 15 or (pct_chg >9 and pct_chg< 10)):
        key=1

    # 排除 一字板
    key1=0
    if((row['open'] - row['close'])>0.8):
        key1=1

    if(low_close<NUM):
        # 最高价与收盘价相同，表示股票在接下来的时间内没有创出新高
        if(high_open < NUM):
            if(key==1 and key1==1):
              return 1
    return 0




def isZhangTingBan_pro(row):
    NUM=0.05
    # print row
    open_close= abs(row['open']-row['low'])
    close_high=abs(row['close']-row['high'])
    # print  'open_close=' + str(open_close)
    # print  'close_high=' + str(close_high)


    pct_chg = abs(row['pct_chg'])
    # print "pct_chg" +str(pct_chg)

    key=0
    if(pct_chg > 15 or (pct_chg >9 and pct_chg< 10)):
        key=1

    # 最低价与开盘价相同，股票在这段时间内没有下跌
    if(open_close < NUM):
        # 最高价与收盘价相同，表示股票在接下来的时间内没有创出新高
        if(close_high < NUM):
            if(key==1):
              return 1
    return 0


def isZhangTingBan(row):
    '''
    60  00 开头的 10%

    30 68 开头的 20%

    '''

    zhangfuMax = 9.1 # 涨幅 是不是大于 这个

    pct_chg = row['pct_chg']
    if(pct_chg > zhangfuMax ):  # 涨停板
        return 1;

    return 0;


'''
判断是还不是一字板
'''
def isYiZiBan(row):
    # if(row['open']==row['close'] and row['high']==row['low']):
    #     return 1
    if(row['open']==row['close'] ):
        return 1

    return 0

'''
是否是黄线

振幅 大于 10%

振幅，是一个股票术语，指开盘后最高价、最低价之差的绝对值与股价的百分比。

   yinxian_zhenfu =  round (((day1_high - day1_low) / day0_close) * 100,2)
'''
def isHuangXian(row,day0close):
    if(len(row) > 0):

        # print'-----'
        day1_high=row['high']
        day1_low=row['low']
        # day0_close=row['close']
        # day0_close=11.41
        day0_close=day0close
        zhenfu = round(((day1_high - day1_low) / day0_close) * 100, 2)

        if(zhenfu > 9):
            return 1

        print "zhenfu=" + str(zhenfu)


    return 0

def testIsHuangXian():
    return 1


if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    testIsHuangXian()
