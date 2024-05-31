#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from pandas import DataFrame

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isInQiangShi_gupiaochi, \
    get_Stock_Name, writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR


'''
鱼跃龙门  佛系翻倍
思路找到 月线  15 年6 月份  到 18 年 下跌的
先计算 18 年 1 月到 12 月 的最小值, 然后比较 15 年 5 月 到 17 年 12 月的所有值

然后找 最近5 个月上涨的 

这是老师的思路,  月线个股牛熊转换周期 7-8 年
横盘至少 2-3 年的时间,  

看了同学们的成绩,我才发现,自己这周做的太少了, 没有计划,像苍蝇一样的乱飞.
下周我要制定计划了.


测试一个股票转化为 月 K 

 2015 - 2020 年 有 72 个数据
 
 2021 年 9 月份  总共有 81 条数据. 有 9 个 符合
 2021 年 10月份  总共有 81 条数据.

'''

def getallstockdata_isYuYueLongMen_fromLocal():
    print '------start 鱼跃龙门  佛系翻倍---'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'

    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    if(len(data)>0):

        # print len(data)
        # print '1111111'
        for index, row in data.iterrows():
            stock_code = row['ts_code']
            stockdata_path = BASE_DIR + '/jishu_stock/stockdata/MONTH_DATA_K/' + stock_code + '_Month' + ".csv"
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                continue
            is_YuYueLongMen_model(df, stock_code)


'''

思路找到 月线  15 年6 月份  到 18 年 下跌的
先计算 18 年 1 月到 12 月 的最小值, 然后比较 15 年 5 月 到 17 年 12 月的所有值

 #1 找到 从 15 年5 月 到 17 年 12 月 的数据
 #2 找到 18 年 1 月到 12 月的数据 并计算最小值
 
#3 获取最近 2 个月的数据
'''
def is_YuYueLongMen_model(data, stock_code):
    # print stock_code

    if(len(data) >=80):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index()  # 重新建立索引 , 保留日期
        # print data
        #1 找到 从 15 年5 月 到 17 年 12 月 的数据
        df_15_17 = data[5:36]
        df_15_17 = df_15_17.reset_index(drop=True)
        # print df_15_17

        #2 找到 18 年 1 月到 12 月的数据 并计算最小值
        df_2018 = data[36:48]
        df_2018 = df_2018.reset_index(drop=True)
        # print df_2018
        min_2018=df_2018.ix[0]['low']
        date1= df_2018.ix[0]['trade_date']
        for index, row in df_2018.iterrows():
            if(row['low'] < min_2018):
                min_2018 = row['low']
                date1 = row['trade_date']
        # print str(min_2018 ) +'---'+ str(date1)
        # print df_2018

        key_isxiangjiang_2015_2018=1
        for index, row in df_15_17.iterrows():
            if(row['low'] < min_2018) : # 如果有小于 2018 年最小值的,那么就不符合要求
                key_isxiangjiang_2015_2018=0
                return

        #3 获取最近 3个月的数据
        data_len= len(data)
        df_2021_5=data[data_len-3:data_len]  # 获取最近 3 个月是不是上涨
        df_2021_5 = df_2021_5.reset_index(drop=True)
        # print df_2021_5
        key_is_shangzhang_5=0#  判断近 5 个月是不是上涨
        data_5_month=[]
        for index, row in df_2021_5.iterrows():
            data_5_month.append(row['close'])
        # print data_5_month
        if(is_small_to_big(data_5_month)==1):
            key_is_shangzhang_5=1
        if(key_isxiangjiang_2015_2018==1 and key_is_shangzhang_5==1):
            info = stock_code + "-----鱼跃龙门  佛系翻倍-----------"

            path = BASE_DIR + '/jishu_stock/zJieGuo/YuYueLongM/' + 'Yu' + datetime.datetime.now().strftime(
                '%Y-%m-%d') + '.txt'
            if (isInQiangShi_gupiaochi(stock_code)):
                info = info + '--强势股票--'
            info = info + '--' + get_Stock_Name(stock_code)
            print info
            #/Users/mac/PycharmProjects/gitproject/stock/jishu_stock/zJieGuo/YuYueLongM
            with open(path, "a") as f:
                f.write(info + '' + "\n")

            path = '鱼跃龙门.txt'
            writeLog_to_txt_path_getcodename(info, path, stock_code)
            return


'''
数组 是由小到大排列  返回 1  ,否则 0 
'''
def is_small_to_big(data):
    len_data = len(data)
    if(len_data > 0):
        is_small_to_big_flag=1
        for i in range(0, len_data - 1):
            # week10_60s[i:i+1]
            if (data[i] > data[i + 1]):
                is_small_to_big_flag = 0

        if(is_small_to_big_flag == 1):
            return 1
    return 0
'''
测试一只股票是不是 鱼跃龙门
'''
def test_is_YuYueLongMen_model():

    # stock_code = '000001.SZ'
    # stock_code = '000060.SZ' #中金岭南
    # stock_code = '002454.SZ' #松芝股份
    # stock_code = '002533.SZ' #金杯电工
    # stock_code = '002536.SZ' #飞龙股份
    stock_code = '000059.SZ' #飞龙股份
    stock_code = '000158.SZ' #飞龙股份
    stockdata_path = BASE_DIR + '/jishu_stock/stockdata/MONTH_DATA_K/' + stock_code + '_Month' + ".csv"
    print "测试---test_is_YuYueLongMen_model "
    df = pd.read_csv(stockdata_path, index_col=0)
    # print df[0:3]
    is_YuYueLongMen_model(df, stock_code)


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    localpath = '/jishu_stock/stockdata/data1/'
    today = starttime.strftime('%Y%m%d')
    # test_is_YuYueLongMen_model()
    getallstockdata_isYuYueLongMen_fromLocal()

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds / 60