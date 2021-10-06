#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1, \
    getRiQi_Befor_Ater_Days, getMin_low_fromDataFrame
from jishu_stock.z_tool.isZhangTingBan import isAn_ZhangtingBan
from stock.settings import BASE_DIR

import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)


''''
神龙摆尾 2 
https://www.yuque.com/chaoren399/eozlgk/ul1oun

思路:  

1. 拿出 30 天数据, 先判断当天day1是不是 30 个数据的最高点,而且是阳线

2. 满足条件一以后, 找涨停板 day2,  day1和 day2 之间的必须大于 等于 5 天. 取出 day1 和 day2的数组 A

3. 数组 A 内的最低价必须大于 涨停板 day2的收盘价, 否则失败 


'''

def get_all_ShenLongBaiWei2(localpath1):
    info1=  '--神龙摆尾 2   start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # 处理 成交量 5 日均量线
        df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        df['amount_5'] = df['amount'].rolling(5).mean()
        df['amount_10'] = df['amount'].rolling(10).mean()
        df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
        df = df.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序



        data6_1 = df.iloc[0:30]  # 前6行

        len1 = len(data6_1)
        isAn_ShenLongBaiWei2_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 30 个数据是不是符合模型
'''
def isAn_ShenLongBaiWei2_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        # data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data
        riqi = data.ix[0]['trade_date']  # 阳线的日期
        riqi1=data.ix[0]['trade_date']  # 涨停板阳线的日期 下边会更新

        # 设置两个 key
        key_1=0; # 1. 拿出 30 天数据, 先判断当天day1是不是 30 个数据的最高点,而且是阳线

        key_2=0;#满足条件一以后, 找涨停板 day2,  day1和 day2 之间的必须大于 等于 5 天. 取出 day1 和 day2的数组 A

        key_3 =1; # 3. 数组 A 内的最低价必须大于 涨停板 day2的收盘价, 否则失败

        key_4=0 # 4 .  5日均量线 下穿 10 日均量线
        key_5=0 # 5. 判断涨停板 之前的 1 个月是横盘 ,方法,找到涨停板前 22 个交易日的 最小值a, 之前 的 60 天数据的最小值不能小于 a

        #第一步:  1. 拿出 30 天数据, 先判断当天day1是不是 30 个数据的最高点,而且是阳线

        day1_close=0

        for index, row in data.iterrows():
            if(index==0 and isYangXian(row) ==1):
                key_1=1
                day1_close=row['close']
            close= row['close']
            if(close > day1_close):
                key_1=0
        #第二步: #满足条件一以后, 找涨停板 day2,  day1和 day2 之间的必须大于 等于 5 天. 取出 day1 和 day2的数组 A

        if(key_1==1):

            data1=data
            data1 = data1.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
            data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
            # print1(data1)
            count=0
            day2_zhangtingban_close=0
            for index, row in data1.iterrows():
                count=count+1
                if(isAn_ZhangtingBan(row)==1): # 把第一天为涨停板的 过滤掉  如果是涨停板
                    day2_zhangtingban_close=row['close']
                    riqi1= row['trade_date']
                    break
            if((len_data -count) >=5 ):
                key_2=1

            # 第 3 步 3. 数组 A 内的最低价必须大于 涨停板 day2的收盘价, 否则失败
            data2=data[0:(len_data -count)]
            # print data2
            # print1(count)


            for index, row in data2.iterrows():
                low_price= row['low'] #

                if(low_price < day2_zhangtingban_close):
                    key_3=0

        # print1(key_1)
        # print1(key_2)
        # print1(key_3)

        if(key_1==1 and key_2==1 and key_3==1 ):
            info=''
            if(isJunLiangXian_5_10(data2)==1):
                key_4=1
            # print1(key_4)
            if(key_4==1):
                if (is_HengPan(riqi1, stockcode) == 1): # key_5
                    info = "--下跌横盘"
                    key_5=1
                # print1(key_5)
                info = info+"-----神龙摆尾 2  成功了" + ' ----' + stockcode +'--'+ "涨停板日期"+str(riqi1)+' ----' + str(riqi)
                # print info
                writeLog_to_txt(info, stockcode)


'''

key_5=0 # 5. 判断涨停板 之前的 1 个月是横盘 ,方法,找到涨停板前 22 个交易日的 最小值a,
 
 之前 的 60 天数据的最小值不能小于 a
 
    #思路, 前一个月的横盘最小值,  有的时候 最小值不是在这个横盘中出现, 所以,我们要
    # 往前 在找近半年的数据,  比如横盘 3 个月, 我们就找 之前的 第 4 个月的最小值,
    

'''
def  is_HengPan(enddate,stockcode):

    #思路, 前一个月的横盘最小值,  有的时候 最小值不是在这个横盘中出现, 所以,我们要
    # 往前 在找近半年的数据,  比如横盘 3 个月, 我们就找 之前的 第 4 个月的最小值,

    date_before_22= getRiQi_Befor_Ater_Days(enddate,-22)
    # print1(date_before_22)

    df = ts.pro_bar(ts_code=str(stockcode),adj='qfq', start_date=str(date_before_22), end_date=str(enddate))
    min_22= getMin_low_fromDataFrame(df)

    date_before_88 = getRiQi_Befor_Ater_Days(enddate,-88)
    date_before_66 = getRiQi_Befor_Ater_Days(enddate,-66)

    df1 = ts.pro_bar(ts_code=str(stockcode),adj='qfq', start_date=str(date_before_88), end_date=str(date_before_66))
    min_66 = getMin_low_fromDataFrame(df1)
    # print1(min_22)
    # print1(min_66)
    if(min_66 >  min_22):
        return 1

    return 0


'''
判断  5日均量线 下穿 10 日均量线
'''
def isJunLiangXian_5_10(data):
    # df = ts.pro_bar(ts_code=str(stock_code), adj='qfq', start_date=str(start_date), end_date=str(end_date), ma=[5,10])
    # data.columns=data['ts_code','trade_date']
    # , ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount, ma5, ma_v_5, ma13, ma_v_13, ma34, ma_v_34, ma10, ma_v_10

    df = data[[ 'trade_date', 'amount','amount_5','amount_10']]
    x= df.copy()
    x['amount_5_10']=x.loc[:,'amount_5'] - x.loc[:,'amount_10']
    data = x


    key1=0
    key2=0 #  只要判断 amount_5_10 异号就可以 , 一个正 一个负
    for index, row in data.iterrows():
        amount_5_10=row['amount_5_10']
        if(amount_5_10<0):
            key1=1
        if(amount_5_10> 0):
            key2=1
    # print1(key1)
    # print1(key2)
    if(key1==1 and key2==1):
        return 1
    return 0




'''
测试老师的案例
'''
def test_isAn_ShenLongBaiWei2_laoshi():


    # 案例 1 游族网络 002174.SZ
    # -----神龙摆尾 2  成功了 ------涨停板日期20210323 ----20210406--游族网络
    # df = ts.pro_bar(ts_code='002174.SZ',adj='qfq', start_date='20210106', end_date='20210406')


    # 案例 2 长安汽车 000625.SZ
    # -----神龙摆尾 2  成功了 ------涨停板日期20210416 ----20210511--长安汽车--强势股票

    df = ts.pro_bar(ts_code='000625.SZ', adj='qfq', start_date='20210206', end_date='20210511')


    # 案例 3 华侨城A 获取的数据开盘价等不准确有问题, 所以测试失败

    # df = ts.pro_bar(ts_code='000069.SZ', start_date='20210106', end_date='20210303')
    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    df['amount_5'] = df['amount'].rolling(5).mean()
    df['amount_10'] = df['amount'].rolling(10).mean()
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
    df = df.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序

    # print1(df)
    data7_2 = df.iloc[0:30]  # 前7行
    # print data7_2
    isAn_ShenLongBaiWei2_model(data7_2, '000625.SZ')






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

        df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        df['amount_5'] = df['amount'].rolling(5).mean()
        df['amount_10'] = df['amount'].rolling(10).mean()
        df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
        df = df.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序


        # data7_4 = df.iloc[0:30]  # 前10个交易日
        data7_4 = df.iloc[22:60]  # 前10个交易日
        len_1=len(data7_4)
        # print1(stock_code)

        for i in range(0, len_1 - 20 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ShenLongBaiWei2_model(data7_4[i:i + 30], stock_code)




if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # test_isAn_ShenLongBaiWei2_laoshi()
    test_Befor_data()
    # test_isAn_ShenLongBaiWei2_ziji()

    # get_all_ShenLongBaiWei2(localpath1)

