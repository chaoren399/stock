#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time
import tushare as ts
import pandas as pd

from jishu_stock.GeShiBaFa.GeShiBaFa_Pro import isAn_GEShi8_model
from stock.settings import BASE_DIR

'''
之前是自己 转换的, 但是 tsture  提供了周线, 现在 来测试一下 

https://waditu.com/document/2?doc_id=144  (这是 没有复权 后的数据, 跟 同花顺 的数据对比一致.)

经测算 ts官方提供的周数据比较好用 2021年09月27日


'''


def getAllWeekKdata(localpath1):
    print '日K 转换为 周K'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})

    starttime = datetime.datetime.now()
    today = starttime.strftime('%Y%m%d')

    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        outpath= BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code +'_Week'+ ".csv"

        count = count+1
        print str(count) +'--'+str(stock_code)

        time.sleep(0.03)  # //睡觉2021
        # df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20180101', end_date='20210922')
        df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20150101', end_date=str(today))
        # print df
        cover_day_K_to_Week_K(df,outpath)



def cover_day_K_to_Week_K(df,outpath):
    if(len(df)==0):
        return 0
    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序
    # df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    # df.set_index('trade_date', inplace=True)

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    # print df
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行

    # print df
    df_week = df

    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    df_week['Week10-60'] = df_week['WeekMa10'] - df_week['WeekMa60']  # G8 买 2 用到

    df_week = df_week.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print  df_week[0:10]

    df_week.to_csv(outpath)

    return 1

'''
测试一个股票转化为 周 K 
'''
def test_cover_day_K_to_Week_K():


    stock_code='000001.SZ'
    outpath = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"

    localpath1 = '/jishu_stock/stockdata/data1/'
    stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)

    cover_day_K_to_Week_K(df, outpath)



'''
https://waditu.com/document/2?doc_id=144


测试 不复权 的成功 
'''
def test_getTushare_Week_k_bufuquan():
    pro = ts.pro_api()

    # df = pro.weekly(ts_code='000001.SZ',start_date='20180101', end_date='20210920',
    #                  fields='ts_code,trade_date,open,high,low,close,vol,amount')

    df = pro.weekly(ts_code='000685.SZ',start_date='20180101', end_date='20210922',
                     fields='ts_code,trade_date,open,high,low,close,vol,amount')


    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序
    # df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    # df.set_index('trade_date', inplace=True)

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    # print df
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行

    # print df
    df_week =df

    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    df_week['Week10-60'] = df_week['WeekMa10'] - df_week['WeekMa60']  # G8 买 2 用到

    df_week = df_week.dropna(how='any', axis=0)#删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序

    # print df_week[0:8]
    df = df_week

    df1 = df.iloc[0:4]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据
    df2 = df.iloc[0:8]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据

    isAn_GEShi8_model(df1,df2, '000685.SZ')

'''

复权数据的获取 

https://tushare.pro/document/2?doc_id=109

前复权  周数据 


-----葛式八法---000685.SZ ----9.45--强势股票----中山公用


'''
def test_getTushare_Week_k_fuquan():

    df = ts.pro_bar(ts_code='000685.SZ', adj='qfq',freq	='W',start_date='20180101', end_date='20210922')

    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    # print df
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行

    # print df
    df_week = df

    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    df_week['Week10-60'] = df_week['WeekMa10'] - df_week['WeekMa60']  # G8 买 2 用到

    df_week = df_week.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print  df_week[0:10]

    # print df[0:10]

    df = df_week

    df1 = df.iloc[0:4]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据
    df2 = df.iloc[0:8]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据

    isAn_GEShi8_model(df1,df2, '000685.SZ')
if __name__ == '__main__':
    import datetime
    starttime = datetime.datetime.now()


    # test1()
    localpath1 = '/jishu_stock/stockdata/data1/'
    getAllWeekKdata(localpath1)  # 默认是运行当天的日期 可以 手动修改日期  #周 5 下午 4 点数据不准
    #下次测试一下  晚上 6 点的数据
    # 周五的 晚上 8 点以后是可以


    # test_cover_day_K_to_Week_K() #测试一个股票转化为 周 K

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds