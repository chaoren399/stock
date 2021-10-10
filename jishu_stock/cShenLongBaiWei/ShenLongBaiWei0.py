#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1
from stock.settings import BASE_DIR

''''
回测 神龙摆尾 0
https://www.yuque.com/chaoren399/eozlgk/ez5zh7

急速下跌熊市末期
(连续3根或以上阴线伴随着低开和大阴线)
小十字星
第2日阴线创新低
第3夭阳线收盘价高过第2日阴线收盘价
以亢龙有悔的方法结算和止损

思路 ,
找到 4 个数据, 满足 第一个是阴线, 第 2 个是十字星, 第 3 个是 阴线,并且是最低点, 第 4 个是 收高的阳线.

然后肉眼判断趋势.

   #  小十字星 判断条件改为收盘价 是不是等于开盘价, 如果是,那么才可以, 这样条件就比较严谨了.


'''

def get_all_isShenLongBaiWei0(localpath1):
    info1=  '--神龙摆尾0  start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:4]  # 前6行
        # data6_1 = df.iloc[0:24]  # 前6行
        data6_1 = df.iloc[0:136]  # 半年 22 * 6 =132
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ShenLongBaiwei0_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ShenLongBaiwei0_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 24):

        data1= data[4:len_data]  #  阴线之前的数据
        data = data[0:4]
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print1( data)

        # 设置两个 key
        key_1=0; #先判断3 个数据是不是满足条件  第一个是阴线,  第 3 个是 阴线,并且是最低点, 第 4 个是 收高的阳线.
        key_2=0; # 判断  第 2 个是十字星,
        key_3=0; #判断 第 4 个是不是收高
        key_4=1; # 第 3 个是最低点

        key_5=0; #单独标记 十字星 是 开盘价与收盘价相等的

        riqi =data.ix[3]['trade_date'] # 阳线的那个线

        count1=0
        day2_pct_chg=0
        day3_close=0
        day4_close=0
        day3_low=0
        for index,row in data.iterrows():
            if(index==0 and isYangXian(row)==0):
                count1=count1+1
            if(index==1 ): # 小十字星
                day2_pct_chg= row['pct_chg']
                day2_close=row['close']
                day2_open=row['open']
                chazhi = ((day2_close - day2_open) / day2_open) * 100 #  (开盘价-收盘价)÷开盘价＜0.5%
                # print1(chazhi)

                # chazhi > -0.5 这个值可以适当缩小到 -0.1 放大到-0.5
                # if(day2_open== day2_close  or (chazhi > -0.5 and   chazhi<0.5)):
                if(day2_open== day2_close  or (chazhi > -0.9 and   chazhi<0.5)):
                    key_2=1
                # if( day2_pct_chg <2 and day2_pct_chg > (-2) ):
                #     key_2 =1
                if(day2_open== day2_close):
                    key_5=1


            if(index==2 and isYangXian(row)==0): #前 3 个
                count1=count1+1
                day3_close=row['close']
                day3_low = row['low']  #创新低 第 3 个是最低点



            if(index==3 and isYangXian(row)==1 ): # 最后的阳线
                count1=count1+1
                day4_close=row['close']

                if(day4_close > day3_close):
                    key_3 =1


        if(count1 ==3):
            key_1 =1

        for index, row in data1.iterrows():
            low = row['low']
            if(low < day3_low):
                key_4=0


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)

        if(key_1==1 and key_2==1 and key_3==1 and key_4==1 ):
            info='----'
            if(key_5==1):
                info="十字星"

            info =info +  "-----神龙摆尾 0 成功了" + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)





'''
测试老师的案例
'''
def test_isAn_ShenLongBaiWei0_laoshi():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例

   #  小十字星 判断条件改为收盘价 是不是等于开盘价, 如果是,那么才可以, 这样条件就比较严谨了.所以000031 不符合小十字星

    # 下边的这 2 个 (开盘价-收盘价)÷开盘价 > -0.9
    df1 = ts.pro_bar(ts_code='000066.SZ',adj='qfq', start_date='20200101', end_date='20210510')
    df1 = ts.pro_bar(ts_code='000031.SZ',adj='qfq', start_date='20210101', end_date='20210205') #000031.SZ --大悦城
    # 下边的 2 个是小十字星
    # df1 = ts.pro_bar(ts_code='000413.SZ',adj='qfq', start_date='20200101', end_date='20210209') #十字星
    # df1 = ts.pro_bar(ts_code='600222.SH',adj='qfq', start_date='20200101', end_date='20210114')#十字星
 #自己案例
    # df1 = ts.pro_bar(ts_code='000889.SZ',adj='qfq', start_date='20200101', end_date='20211009')
    # df1 = ts.pro_bar(ts_code='000529.SZ',adj='qfq', start_date='20200101', end_date='20210729')

    # data7_1 = df1.iloc[0:6]  # 前7行
    data7_1 = df1.iloc[0:136]  # 前7行
    # print data7_1
    isAn_ShenLongBaiwei0_model(data7_1,'000889.SZ')


'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        data7_4 = df.iloc[44:190]  # 前10个交易日
        len_1=len(data7_4)

        for i in range(0, len_1 - 136 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ShenLongBaiwei0_model(data7_4[i:i + 136], stock_code)
if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # test_isAn_ShenLongBaiWei0_laoshi()
    test_Befor_data()
    # get_all_isShenLongBaiWei0(localpath1)