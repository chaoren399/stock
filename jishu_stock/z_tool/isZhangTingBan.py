#!/usr/bin/python
# -*- coding: utf8 -*-


'''
判断 row 是不是涨停板, 返回 1 是涨停板, 返回 0 不是涨停板

只做 00 60 开头的 股票
'''

# zhangting_xishu = 1.098
# dieting_xishu = 0.903

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


zhangting_xishu = 1.098
dieting_xishu = 0.901

'''
2024年11月9日 重新判断 涨停板：
涨停： 今日最高价等于收盘价， 并且收盘价等于 昨日的收盘价 X 1.098 （其实是1.10)
跌停：今日最低价等于收盘价， 并且 收盘价等于昨日的收盘价 X 0.903（其实就是0.9）
炸板： 今日最高价等于 昨日收盘价 X 1.098 并且 收盘价小于 最高价  


  print '涨停为1,跌停为2,炸板为3-------------------'

'''
def isZhangTingBan_zzy(df):
    '''
    60  00 开头的 10%

    30 68 开头的 20%

    '''
    if(len(df) ==2) :

        data1 = df
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

        day0_close=0

        day1_open=0
        day1_close=0
        day1_high=0
        day1_low=0

        riqi = data1.ix[1]['trade_date']  # 阳线的日期

        for index, row in data1.iterrows():
            if (index == 0):
                day0_close = row['close']
            if (index == 1):
                day1_open=row['open']
                day1_close=row['close']
                day1_high=row['high']
                day1_low=row['low']

        zhangting_jiage= day0_close * zhangting_xishu
        zhangting_jiage = round(zhangting_jiage,1)  #保留 1位小数

        dieting_jiage = day0_close * dieting_xishu
        dieting_jiage = round(dieting_jiage,2)

        zhaban_yuzhi=0.15
        day1_high_zhangting_jiage = day1_high - zhangting_jiage
        zhangting_yuzhi=0.05
        day1_close_zhangting_jiage = day1_close - zhangting_jiage

        lanK_yuzhi=0.5
        day1_close_dieting_jiage=day1_close - dieting_jiage


        if(0):
            print "K线日期=" + riqi
            print str(zhangting_jiage) + '=zhangting_jiage'
            print 'day1_high - zhangting_jiage=' +str(day1_high - zhangting_jiage)
            print 'day1_close - zhangting_jiage =' +str(day1_close - zhangting_jiage )
            # print 'day1_close - dieting_jiage =' +str(day1_close - dieting_jiage )

            print 'day1_low - dieting_jiage =' + str(day1_low - dieting_jiage)
            print 'dieting_jiage='+str(dieting_jiage)

        key=9

        if(day1_high==day1_close and abs(day1_close_zhangting_jiage) < zhangting_yuzhi):
            #涨停
            key=1
        # elif(day1_low == day1_close and abs(day1_close_dieting_jiage) <lanK_yuzhi):
        elif( (day1_low - dieting_jiage)  <lanK_yuzhi):
            #跌停
            key=2
        elif( abs(day1_high_zhangting_jiage) < zhaban_yuzhi  and day1_close < day1_high):

            # 炸板
            key = 3


    else:
        print 'isZhangTingBan_zzy < 2 days '
    return key;



def isLanK_zzy(df):
    '''
    60  00 开头的 10%

    30 68 开头的 20%

    '''
    if(len(df) ==2) :

        data1 = df
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

        day0_close=0

        day1_open=0
        day1_close=0
        day1_high=0
        day1_low=0

        riqi = data1.ix[1]['trade_date']  # 阳线的日期

        for index, row in data1.iterrows():
            if (index == 0):
                day0_close = row['close']
            if (index == 1):
                day1_open=row['open']
                day1_close=row['close']
                day1_high=row['high']
                day1_low=row['low']

        zhangting_jiage= day0_close * zhangting_xishu
        zhangting_jiage = round(zhangting_jiage,1)  #保留 1位小数

        dieting_jiage = day0_close * dieting_xishu
        dieting_jiage = round(dieting_jiage,2)

        zhaban_yuzhi=0.15
        day1_high_zhangting_jiage = day1_high - zhangting_jiage
        zhangting_yuzhi=0.05
        day1_close_zhangting_jiage = day1_close - zhangting_jiage

        lanK_yuzhi=0.3
        day1_low_dieting_jiage=day1_low - dieting_jiage
        # print 'day1_low - dieting_jiage =' + str(day1_low - dieting_jiage)

        if(0):
        # if(1):
            print "K线日期=" + riqi
            print str(zhangting_jiage) + '=zhangting_jiage'
            print 'day1_high - zhangting_jiage=' +str(day1_high - zhangting_jiage)
            print 'day1_close - zhangting_jiage =' +str(day1_close - zhangting_jiage )
            # print 'day1_close - dieting_jiage =' +str(day1_close - dieting_jiage )

            print 'day1_low - dieting_jiage =' + str(day1_low - dieting_jiage)
            print 'dieting_jiage='+str(dieting_jiage)

        key=9

        if (abs(day1_low_dieting_jiage) < lanK_yuzhi):
            key=1
        isYinXian=0
        if(day1_close < day1_open):
            isYinXian=1
        if(abs(day1_high_zhangting_jiage)< zhangting_yuzhi and isYinXian==1):
            #yinxian
            key=2
        # if(day1_high_zhangting_jiage < zhangting_yuzhi and day1_open >= day0_close):
        #     key=3



    else:
        print 'isZhangTingBan_zzy < 2 days '
    return key;



def testIsHuangXian():
    return 1


if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    testIsHuangXian()
