#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, \
    writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR

''''
缺口理论, 蜻蜓点水
https://www.yuque.com/chaoren399/eozlgk/buoxgc
https://www.yuque.com/docs/share/1c643c50-f296-491d-bcb5-8843849d873b?# 《2-蜻蜓点水-缺口理论—》

1, 找到 6 日的数据

2 ,第一天 ,第 2 天是 缺口, 第 2 天的 最小值 大于 第一天的 最大值

3 .  第 3,4,5,6 天中  最小值 小于 第一天的最大值就可以.

'''

def get_all_QingTingDianShui(localpath1):
    info1=  '--缺口理论, 蜻蜓点水 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:8]  # 前8行 至少 7 行
        data6_1 = df.iloc[2:10]  # 前8行 至少 7 行

        len1 = len(data6_1)
        isAnQingTingDianShui_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAnQingTingDianShui_model(data,stockcode):
    if(len(data) >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data

        # 设置两个 key
        key_1=0;
        key_2=0;

        #2 ,第一天 ,第 2 天是 缺口, 第 2 天的 最小值 大于 第一天的 最大值
        day2_low= data.ix[1]['low']
        day1_high=data.ix[0]['high']
        # print 'day1_high' +str(day1_high)
        riqi=data.ix[0]['trade_date']


        # 条件一
        if(day2_low > day1_high):
            key_1 =1
        # print1(key_1)
        # 条件 2  3 .  第 3,4,5,6 天中  最小值 小于 第一天的最大值就可以.
        #改进, 之后 的最低值不能 覆盖缺口

        data1 = data[2:len(data)]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        count1=0
        # print data1

        for index, row in data1.iterrows():
            count1=count1+1
            low1= row['low']
            # print1(low1)
            if(low1 < day1_high): # 遇到 填补缺口后,
                key_2=1
                # print row['trade_date']
                # print count1

                data2= data1[count1:len(data1)]
                # print data2
                for index1, row1 in data2.iterrows():
                    low2= row1['low']
                    if(low2 < day1_high):
                        key_2=0
                        return  #这个  return 不能忽略 , 条件不满足过多中断

        if(key_1==1 and  key_2 ==1):
            info = "-----缺口理论, 蜻蜓点水 成功了 ----"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '蜻蜓点水.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)




def test_get_all_QingTingDianShui():

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # 打印最新的数据  2020 年数据 不太准确,测试有误差
    # df1 = ts.pro_bar(ts_code='000038.SZ', adj='qfq',start_date='20210219', end_date='20210302')  # 成功 数据20210218 错了一天

    df1 = ts.pro_bar(ts_code='000070.SZ', adj='qfq', start_date='20200617', end_date='20200630') # 成功了



    # data7_1 = df1.iloc[0:6]  # 前7行
    data7_1 = df1.iloc[0:8]  # 前7行
    # print data7_1
    isAnQingTingDianShui_model(data7_1,'000070.SZ')


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # test_get_all_QingTingDianShui()
    get_all_QingTingDianShui(localpath1)