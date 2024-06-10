#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian, \
    writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR

''''
2021年10月15日  
亢龙有悔个股应用, 胜率 70% 以上 
https://www.yuque.com/chaoren399/eozlgk/qrbx7l/


思路, 先找 最近 4 个数据 是不是符合 亢龙有悔的条件, 完美符合,   注意 4 个数据不是 3 个
然后在判断是不是 熊市末期


'''

def get_all_KangLongYouHui_GeGu(localpath1):
    info1=  '--亢龙有悔个股应用, 胜率 70% 以上 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:66]  # 前66 就是 3 个月的数据
        # data6_1 = df.iloc[1:67]  # 前66 就是 3 个月的数据

        isAn_KangLongYouHui_GeGu_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_KangLongYouHui_GeGu_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,



        data1= data[len_data -4: len_data]  #最新的 3 个数据
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[3]['trade_date']  # 阳线的日期
        # print1(data1)
        data2 = data[len_data-4-60:len_data-4]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,


        # 设置两个 key
        key_1=0; #先判断是不是 3 个阴 一个阳
        key_2=0; #判断 阳线 低开高收

        key_3=0;# 大阴线实体必须大
        key_4=0; # 第 2 个阴线 开盘价 大于 第 3 个阴线, 最好有跳空,
        key_5=0 ; #阴线是不是有跳空

        key_6=1; # 近 3 个月 是下跌

        count1=0
        day3_open =0
        day3_close =0
        day4_open =0
        day4_close =0
        for index,row in data1.iterrows():
            if(index==0 and isYangXian(row)==0):
                count1=count1+1
            if(index==1 and isYangXian(row)==0):
                count1 = count1 + 1
            if(index==2 and isYangXian(row)==0):
                count1 = count1 + 1
                day3_open=row['open']
                day3_close=row['close']
            if(index==3 and isYangXian(row)==1):
                count1 = count1 + 1
                day4_open=row['open']
                day4_close=row['close']

        if(count1==4):
            key_1=1
            if(day4_open < day3_close and day4_close > day3_close and day4_close < day3_open):
                key_2=1
        if(key_1==1 and key_2==1):
            chazhi1=0
            chazhi2=0
            day2_open=0
            day3_open=0
            day2_close=0
            for index, row in data1.iterrows():
                if (index==1):
                    chazhi1 = ((row['close'] - row['open']) / row['open']) * 100  # (开盘价-收盘价)÷开盘价＜0.5%
                    day2_open=row['open']
                    day2_close=row['close']
                if(index==2):
                    chazhi2 = ((row['close'] - row['open']) / row['open']) * 100  # (开盘价-收盘价)÷开盘价＜0.5%
                    day3_open= row['open']
            if(chazhi1 !=0):
                dayinxina_xiaoyinxian_bilv= chazhi2/chazhi1
                if(dayinxina_xiaoyinxian_bilv > 2): # 大阴线实体必须大
                    key_3=1
            # 第 2 个阴线 开盘价 大于 第 3 个阴线, 最好有跳空,
            if(day2_open > day3_open ):
                key_4=1
                #最好有跳空,
                if(day2_close > day3_open): # 第 2 天阴线的收盘价 大于第三天 阴线的开盘价
                    key_5=1

          # 近 3 个月 是下跌

        min_low= data1.ix[0]['low']
        for index, row in data2.iterrows():
            if(row['low'] < min_low):
                key_6=0



        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        if(key_1==1 and  key_2 ==1 and key_3 ==1 and key_4==1 and key_6==1):
            info=''
            if(key_5==1):
                info='有跳空'
            else:
                info='无跳空'
            info = info+"--亢龙有悔个股胜率70%以上--" + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '个股亢龙有悔.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)




'''
测试老师的案例
'''
def test_isAn_KangLongYouHui_GeGu_laoshi():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例 1

    df1 = ts.pro_bar(ts_code='000005.SZ',adj='qfq', start_date='20170206', end_date='20180620')

    data7_1 = df1.iloc[0:66]  # 前7行
    # print data7_1
    isAn_KangLongYouHui_GeGu_model(data7_1,'002174.SZ')

    # 案例 2南玻A 000012，
    df1 = ts.pro_bar(ts_code='000012.SZ',adj='qfq', start_date='20170206', end_date='20210208')
    data7_1 = df1.iloc[0:66]  # 前7行
    # print data7_1
    isAn_KangLongYouHui_GeGu_model(data7_1,'000012.SZ')

'''
测试自己的案例
'''
def test_isAn_KangLongYouHui_GeGu_ziji():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)



'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        data7_4 = df.iloc[22:100]  # 前10个交易日
        data7_4 = df.iloc[44:122]  # 前10个交易日
        data7_4 = df.iloc[66:144]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 66 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_KangLongYouHui_GeGu_model(data7_4[i:i + 66], stock_code)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    test_isAn_KangLongYouHui_GeGu_laoshi()
    # get_all_KangLongYouHui_GeGu(localpath1)
    # test_Befor_data()