#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode
from stock.settings import BASE_DIR


'''
龙战于野
https://www.yuque.com/chaoren399/eozlgk/hafzse

第一步先判断 模型
 获取近 3 天的数据, 

第一天 涨停
第二天 大阴线
第三天, 阳线收盘价 高过阴线开盘价  

第二步 再判断是不是下跌趋势
获取 近 7 天的最低值, 并判断 是近 30 天的最低值, 思路 当前日期的近 7 天的最低点,  判断 半年的 最低点是不是 小于那个值
然后

案例 : 常山北明 000158  20210420

从之前的 10 个里边 成功可以做到 0.9
'''
def getallstockdata_isLongZhan_YuYe(localpath1):
    info1=  '----龙战于野  低位涨停  次日大阴线 第 3 日高过  阴线 开盘价 start----'
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        # print df
        if (df.empty):
            continue
        # data7_1 = df.iloc[0:20]
        data7_1 = df.iloc[0:3]
        len1= len(data7_1)
        for i in range(0, len1 - 3 + 1):
            isAn_LongZhanYuYe_model(data7_1[i:i + 3], stock_code)


def test_getallstockdata_isLongZhan_YuYe():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    pro = ts.pro_api()
    stock_code='000158.SZ'
    # print 'stockcode'+stock_code
    df = pro.daily(ts_code='000158.SZ', start_date='20210401', end_date='20210422')
    data= df[0: 3]
    # print data
    isAn_LongZhanYuYe_model(data, stock_code)

def isAn_LongZhanYuYe_model(data,stock_code):
    if(len(data)==3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data

        riqi = data.ix[0]['trade_date']
        isZhangtingban = 0
        isYinxian = 0
        isday3yangxian = 0
        for index, row in data.iterrows():

            if(index ==0) : #第一天
                # print data
                qianzhui_code = stock_code[0:2]
                zhangfuMax = 9  # 涨幅 是不是大于 这个
                if (qianzhui_code == '00' or qianzhui_code == '60'):
                    zhangfuMax = 9.1
                elif (qianzhui_code == "30" or qianzhui_code == '68'):
                    zhangfuMax = 19
                count = 0;
                pct_chg = row['pct_chg']

                if (pct_chg > zhangfuMax):  # 涨停板
                    isZhangtingban=1
                    # print 'isZhangtingban=1'

            if(index == 1): #第 2 天是个大阴线
                day2_close=row['close']
                day2_open=row['open']

                day2_pct_chg = row['pct_chg']
                if(day2_open > day2_close and abs(day2_pct_chg)>4):
                    isYinxian=1
                    # print 'day2_close'+str(day2_close)
                    # print 'day2_open'+str(day2_open)
                    # print 'isYinxian=1'

            if(index==2): #第 3 天 阳线,收盘价高过阴线开盘价
                day3_close = row['close']
                day3_open = row['open']
                # print 'day3_close = ' + str(day3_close)
                # print 'day3_open = ' + str(day3_open)
                # print 'day2_open = ' +str(day2_open)
                # print 'isYinxian=' + str(isYinxian)
                if(day3_open < day3_close and  isYinxian==1 and  day3_close > day2_open):
                    isday3yangxian =1
                    # print 'isday3yangxian =1'

            if(isZhangtingban ==1 and isYinxian==1 and  isday3yangxian ==1):
                info =  stock_code + "  " + str(pct_chg) + "--- 龙战于野 低位第1天涨停 第2天大阴线 第3天阳线高过阴线  ------" + str(riqi)
                # print 'day2_pct_chg=' + str(abs(day2_pct_chg))
                writeLog_to_txt(info, stock_code)




if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()
    localpath1 = '/jishu_stock/stockdata/data1/'

    getallstockdata_isLongZhan_YuYe(localpath1)
    # test_getallstockdata_isLongZhan_YuYe()




    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds

    '''
    追求的 比较符合的 趋势
    '''