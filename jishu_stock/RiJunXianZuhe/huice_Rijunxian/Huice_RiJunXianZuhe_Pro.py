#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import time

import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, getRiQi_Befor_Ater_Days
from stock.settings import BASE_DIR

'''
https://tushare.pro/document/2?doc_id=109

日均线组合5-13-34 回测

测试 上一个月 每天 满足 5-13-34 的 收益率为 10% 的概率 
测试 上一个月 每天 满足 5-13-34 的 收益率为 5% 的概率 





'''

count_fuhe_rijunxian = 0
count_shouyilv_big_130 = 0

def huice_get_5_13_34_RiJunXian_Pro3(localpath1):
    info1=  '--日均线组合5-13-34  start-- 如果结果比较少,可以 缩小 data7_1 = df.iloc[0:10]  '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        df = df[['ts_code', 'trade_date', 'low', 'ma5', 'ma13', 'ma34']]
        df['ma5_13_cha'] = df['ma5'] - df['ma13']
        # data7_1 = df.iloc[0:7]  # 前7行
        # data7_1 = df.iloc[1:8]  # 前7行
        # data7_1 = df.iloc[15:22]  # 前7行
        # data7_1 = df.iloc[22:44]  # 前7行
        data7_1 = df.iloc[44:66]  # 前7行
        # print data7_1
        # isyes = huice_isRiJunxianZuHe_mode_pro3(data7_1, stock_code)

        len1 = len(data7_1)
        # print len1
        for i in range(0, len1 - 7 + 1):
            isyes = huice_isRiJunxianZuHe_mode_pro3(data7_1[i:i+7], stock_code)

    print 'count_fuhe_rijunxian='+str(count_fuhe_rijunxian)
    print 'count_shouyilv_big_130='+str(count_shouyilv_big_130)


'''
这个方法是判断 已经出现金叉 

思路:  
第一天 ma5_13_cha > 0
第二天: ma5_13_cha <0
'''
def huice_isRiJunxianZuHe_mode_pro3(df, stock_code):
    if(len(df)>0):
        df = df.reset_index(drop=True)  # 重新建立索引 ,
        #1 判断 3 个均线都是 向上趋势, 多头排列
        ma5_max= df.ix[0]['ma5']
        ma13_max= df.ix[0]['ma13']
        ma34_max= df.ix[0]['ma34']
        riqi = df.ix[0]['trade_date']
        is_DuoTou_PaiLie=0

        is_day3_jincha =0
        global  count_fuhe_rijunxian
        global  count_shouyilv_big_130

        for index, row in df.iterrows():
            if(row['ma5'] >ma5_max):
                is_DuoTou_PaiLie=1
            if(row['ma13'] >ma13_max):
                is_DuoTou_PaiLie=1
            if(row['ma34'] >ma34_max):
                is_DuoTou_PaiLie=1

            if(index ==0 and row['ma5_13_cha'] >0 ): # 第 2 个点位是 金叉
                is_day3_jincha=is_day3_jincha+1
            if(index==1 and row['ma5_13_cha'] < 0): #
                is_day3_jincha = is_day3_jincha + 1

        if (is_day3_jincha == 2 and is_DuoTou_PaiLie == 0):

            count_fuhe_rijunxian=count_fuhe_rijunxian+1

            #  根据日期 获取 近 7 天的数据, 判断是不是大于  第一天的开盘价 1.3
            if (jisuan_7days_is_success(stock_code,str(riqi))==1):
                count_shouyilv_big_130=count_shouyilv_big_130+1
            else:
                info = "-----回测 日均线组合5-13-34 成功了" + ' ----' + stock_code + ' ----' + str(riqi)
                # print info
                writeLog_to_txt(info, stock_code)



'''
  根据日期 获取 近 7 天的数据, 判断是不是大于  第一天的开盘价 1.3 
'''
def jisuan_7days_is_success(stock_code,start_date):
    end_date= str(getRiQi_Befor_Ater_Days(start_date,30))  # 间隔 20 天 成功的概率
    # print start_date
    # print end_date

    df = ts.pro_bar(ts_code=stock_code, start_date=start_date, end_date=end_date)
    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序
    df = df.reset_index(drop=True)  # 重新建立索引 ,
    high_price = df.ix[0]['open'] * 1.05
    # if (df.ix[0]['open'] > 10 and df.ix[0]['open'] < 30):
    # if (df.ix[0]['open'] > 15):
    if (1):
        for index1, row1 in df.iterrows():
            if (row1['high'] > high_price):
               return 1

    return 0



def test_get_5_13_34_RiJunXian_Pro3():
    stock_code='000026.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    # print df

    df = df[['ts_code', 'trade_date', 'low', 'ma5', 'ma13', 'ma34']]
    df['ma5_13_cha'] = df['ma5'] - df['ma13']

    data7_1 = df.iloc[0:7]  # 前7行
    # print data7_1

    # isyes = isRiJunxianZuHe_mode_pro3(data7_1, stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    huice_get_5_13_34_RiJunXian_Pro3(localpath1=localpath1)
