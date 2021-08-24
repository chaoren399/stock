#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt
from stock.settings import BASE_DIR


'''
神龙摆尾

1# 找到 涨停板
'''


def getallstockdata_isShenLongBaiWei_fromLocal(localpath1):
    print "神龙摆尾   start "
    # path = BASE_DIR + '/jishu_stock/bQiXingLuoChangKong/data/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/xiadiecodes.csv'
    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        # localpath1 ='/jishu_stock/stockdata/data1/'
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        # df =  pd.read_csv(stockdata_path, dtype={'code': str})
        df = pd.read_csv(stockdata_path, index_col=0)
        # print df
        if (df.empty):
            continue
            # 1 得到 第一个 7 交易日数据
            # iloc只能用数字索引，不能用索引名
        data7_1 = df.iloc[0:40]  # 前10个交易日
        # data7_1 = data7_1.reset_index(drop=True)  # 重新建立索引 ,
        # print data7_1
        # 2 单独一个函数 判断是不是符合  神龙摆尾
        isyes = isAnShenLongBaiwei_model(data7_1, stock_code)
        if (isyes == '1'):
            # liststocks.append(stock_code)
            print "几个了---------------------------------------:"

def isAnShenLongBaiwei_model(data,stock_code):

    '''
    60  00 开头的 10%

    30 68 开头的 20%

    '''
    # print  stock_code[0:2]

    data = data.reset_index(drop=True)  # 重新建立索引 ,
    # print data
    qianzhui_code= stock_code[0:2]
    zhangfuMax = 9 # 涨幅 是不是大于 这个
    if(qianzhui_code =='00' or qianzhui_code =='60'):
        zhangfuMax=9.1
    elif(qianzhui_code=="30" or qianzhui_code=='68'):
        zhangfuMax=19
    count =0;


    for index, row in data.iterrows():

        if(index==0): # 最新的一天, 阳线突破实体
            day1open = row['open']
            day1close= row['close']
            day1riqi = row['trade_date']
            if( day1close - day1open >0 ): #如果是阳线
                # print "阳线 继续"
                continue
            else: break
        if (index == 1):  #
            day1_1open = row['open']
            day1_1close = row['close']
            day1_1riqi = row['trade_date']
        if (index == 2):  #
            day1_2open = row['open']
            day1_2close = row['close']
        if (index == 3):  #
            day1_3open = row['open']
            day1_3close = row['close']
        if (index == 4):  #
            day1_4open = row['open']
            day1_4close = row['close']
        if (index == 5):  #
            day1_5open = row['open']
            day1_5close = row['close']


        # print index
        pct_chg = row['pct_chg']


        #1 找到涨停板, 还有 突破涨停板的最后一天, 判断 之间的天数是不是大于 7 天,
        #2 找到 最后一天相邻的 5 个交易日,判断是不是在箱体内

        if(pct_chg > zhangfuMax):  # 涨停板
            day2riqi = row['trade_date']
            # 涨幅 10%的那一个行
            day2DayangxianClose = row['close']
            day2Dayangxianopen = row['open']

            if(day1close > day2DayangxianClose and  day1open >day2Dayangxianopen and day1open < day2DayangxianClose):


                if( (day1riqi - day2riqi) > 7): #1 找到涨停板, 还有 突破涨停板的最后一天, 判断 之间的天数是不是大于 7 天,

                    # 2 找到 最后一天相邻的 5 个交易日,判断是不是在箱体内
                    if(day1_1open < day2DayangxianClose and day1_1open > day2Dayangxianopen
                    and day1_1close < day2DayangxianClose and day1_1close > day2Dayangxianopen):


                        if(day1_2open < day2DayangxianClose and day1_2open > day2Dayangxianopen
                        and day1_2close < day2DayangxianClose and day1_2close > day2Dayangxianopen):
                            if(day1_3open < day2DayangxianClose and day1_3open > day2Dayangxianopen
                            and day1_3close < day2DayangxianClose and day1_3close > day2Dayangxianopen):
                                if(day1_4open < day2DayangxianClose and day1_4open > day2Dayangxianopen
                                and day1_4close < day2DayangxianClose and day1_4close > day2Dayangxianopen):
                                    if(day1_5open < day2DayangxianClose and day1_5open > day2Dayangxianopen
                                    and day1_5close < day2DayangxianClose and day1_5close > day2Dayangxianopen):



                                        info = stock_code + "  " + str(pct_chg) + "--------- 神龙摆尾---------" + str(day2riqi) + " 突破阳线日期"+str(day1riqi)
                                        print info
                                        writeLog_to_txt(info)

                                        return 1;
        count = count + 1

    return 0;

if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # getallstockdata_isShenLongBaiWei('20210701', '20210805')
    # anstock_isShenLongBaiWei_model('000539.SZ','20210701', '20210805')
    localpath1 = '/jishu_stock/stockdata/data1/'
    getallstockdata_isShenLongBaiWei_fromLocal(localpath1)

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds