#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

from stock.settings import BASE_DIR
import pandas as pd
import tushare as ts

'''
time.sleep(0.03)  # //睡觉
'''

'''
给信息 还有路径 写入文件
'''

def writeLog_to_txt_path(info ,path):
    with open(path, "a") as f:
        f.write(info + '' + "\n")

'''
固定路径的写入
'''
def writeLog_to_txt(info,code):
    path = BASE_DIR + '/jishu_stock/JieGuo/' + datetime.datetime.now().strftime(
        '%Y-%m-%d') + '.txt'

    if(isInQiangShi_gupiaochi(code)):
        info = info +'--强势股票--'

    info= info+'--'+get_Stock_Name(code)
    print info

    with open(path, "a") as f:
        f.write(info + '' + "\n")



'''
从 dataframe 中 找到 每日K 线中最低值 中最小的 那个数值
'''
def  getMin_low_fromDataFrame(data):
    Mindata= data.ix[0]['low']
    for index ,row in data.iterrows():
        if( Mindata > row['low']):  # 近 10 天的最小值
            Mindata = row['low']
    return Mindata
'''
从 dataframe 中 找到 每日K 线中最高值 high 中最大的 那个数值
'''
def getMax_High_fromDataFrame(data):
    maxData = data.ix[0]['high']
    for index , row in data.iterrows():
        if(maxData < row['high']):
            maxData = row['high']
    return maxData

'''
获取 之前 -30 , 1 天之前的日期
'20210813'
'''
def getRiQi_Befor_Ater_Days(date,numdays):
    day1riqi = str(date)
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    result_date = cur_day + datetime.timedelta(days=numdays)
    try:
        result_date = result_date.strftime('%Y%m%d')
    except Exception as e:
        print e


    return result_date

'''
获取 之前 30 天之前的日期
'20210813'
'''
def getRiQi_Befor_30Days(date):
    day1riqi = str(date)
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    result_date = cur_day + datetime.timedelta(days=-30)
    try:
        result_date = result_date.strftime('%Y%m%d')
    except Exception as e:
        print e


    return result_date
'''
获取 之前 60 天之前的日期
'20210813'
'''
def getRiqi_Befor_60Days(date):
    day1riqi = str(date)
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    result_date = cur_day + datetime.timedelta(days=-60)
    try:
        result_date = result_date.strftime('%Y%m%d')
    except Exception as e:
        print e
    return result_date

'''
判断是不是上涨趋势 
因为是要获取网络数据 ,所以 尽量要在 for 循环中加入条件

得到 最近 30 天 数据'low'的最小值,min_7days
得到 60 天 数据的 数据'low'的最小值  min_30days

发现 判断 最小值   要比 判断最大值 更好一些   起码 最近 2 个月是上涨的
'''
def isShangZhang_QuShi(data):
    date_1day = data.ix[0]['trade_date']
    stock_code = data.ix[0]['ts_code']

    data_7days = data.iloc[0:7]
    min_7days = getMin_low_fromDataFrame(data)
    date_30days = getRiQi_Befor_30Days(date_1day)
    date_60days = getRiqi_Befor_60Days(date_1day)
    #得到近期数据

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    pro = ts.pro_api()
    pro = ts.pro_api()
    df30 = pro.daily(ts_code=stock_code, start_date=date_30days, end_date=date_1day)
    df60 = pro.daily(ts_code=stock_code, start_date=date_60days, end_date=date_1day)

    min_30days = getMin_low_fromDataFrame(df30)
    min_60days = getMin_low_fromDataFrame(df60)
    if(min_30days > min_60days ):
        # print  '----上涨趋势----'+stock_code
        return 1
    return 0



'''
给出 股票代码 得到 股票的名字
'''
def  get_Stock_Name(code):
    path = path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    data = pd.read_csv(path)
    for index, row in data.iterrows():
        if (row['ts_code'] == code):
            return row['name']


'''
判断一只股票是不是 在强势股票池中
'''
def isInQiangShi_gupiaochi(code):
    path =  path = BASE_DIR + '/jishu_stock/stockdata/强势和我的股票池.csv'
    data = pd.read_csv(path)

    count = 0
    if (len(data.columns) == 1):  # 只有一列股票代码,没有股票名称
        for index, row in data.iterrows():
            if(row['ts_code'] == code):

                return 1
    return 0
if __name__ == '__main__':
    # isInQiangShi_gupiaochi('603041.SH')
    print get_Stock_Name('603040.SH')


