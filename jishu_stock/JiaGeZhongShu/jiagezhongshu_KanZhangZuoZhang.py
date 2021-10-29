#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    jiagezhongshu_writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
创建日期: 2021年10月29日
更新日期:
价格中枢-看涨做涨
https://www.yuque.com/chaoren399/eozlgk/nzv2b4/


上涨初期或中期
实体较大有上下影线的阳线
实体的1/2恰好是中枢价
收盘价在中枢价之上
上下影线都不长且等长
第2周高开高走低开不能做
后期发力上攻
大阳线最低价止损

jiagezhognshu_KanZhangZuoZhang
'''

def get_all_jiagezhognshu_KanZhangZuoZhang(localpath1):
    info1=  '--价格中枢-看涨做涨 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():

        stock_code = row['ts_code']

        stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        if (df.empty):
            continue

        df = df.reset_index(drop=False)  # 重新建立索引 ,
        data6_1 = df.iloc[0:8]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_jiagezhognshu_KanZhangZuoZhang_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_jiagezhognshu_KanZhangZuoZhang_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        # print1(data1)
        riqi = data1.ix[0]['trade_date']  # 阳线的日期


        # 设置两个 key
        key_0=0; # 0第一周第 2 周都是 阳线
        key_1=0;  #1实体的1/2恰好是中枢价
        key_2=0; # 2收盘价 在中枢价之上
        key_3=0; # 3上下影线 都不会死很长, 且等长 ,

        key_4=0; # 4第 2 周 刚开高走 的阳线.  周四买入也可以.
        key_5=0; #第一周实体较大, 我这里大于 1 来测试一下
        key_6=0; #上下影线都不长, 比实体要小

        week1_shangyingxian=0
        week1_xiayingxian=0
        week1_shiti=0
        week1_open=0
        week1_close=0
        week1_shiti_yiban=0 # 是的 1/2
        jiagezhongshu =0
        count=0
        week2_open=0
        shiti_yingxian=0
        shangyingxian_xiayingxian=0
        for index, row in data1.iterrows():
            if(index==0 and isYangXian(row)==1):
                count=count+1
                week1_shangyingxian=getyangxian_shangyingxian_daxiao(row)
                week1_xiayingxian=getyangxian_xiayingxian_daxiao(row)
                jiagezhongshu = get_jiagezhongshu(row)
                week1_shiti=getShiTiDaXiao(row)
                week1_open=row['open']
                week1_close=row['close']

            if(index==1 and isYangXian(row)==1):
                count=count+1
                week2_open=row['open']

         # 0第一周第 2 周都是 阳线
        if(count ==2):
            key_0=1
            #1 实体的1/2恰好是中枢价
            week1_shiti_yiban = (week1_open+week1_close)/2 # 实体的一半
            jiagezhongshu_week1_shiti_yiban=abs( (jiagezhongshu) - week1_shiti_yiban) # 价格中枢 - 实体一半的差值
            jiagezhongshu_week1_shiti_yiban = round(jiagezhongshu_week1_shiti_yiban,2)
            if( jiagezhongshu_week1_shiti_yiban < 0.1):
                key_1=1

            #2 收盘价 在中枢价之上
            if(week1_close > jiagezhongshu):
                key_2=1

            #3 上下影线 等长
            # shangyingxian_xiayingxian=abs(week1_shangyingxian -week1_xiayingxian) # 上影线-下影线的绝对值
            # if(  shangyingxian_xiayingxian< 0.12 ):
            #     key_3=1

            week1_xiayingxian= week1_xiayingxian+0.0001
            shangyingxian_xiayingxian=week1_shangyingxian /week1_xiayingxian # 上影线-下影线的绝对值

            if(  shangyingxian_xiayingxian< 1.51 and shangyingxian_xiayingxian > 0.5):
                key_3=1

            #4  第 2 周 刚开高走 的阳线.  周四买入也可以.
            gaokai = week2_open - week1_close
            if(  gaokai> -0.05 ):  # 案例中 最小的是一个是 - 0.01
                key_4=1


           #5 第一周实体较大, 我这里大于 1 来测试一下
            if(week1_shiti > 1):
                key_5=1

            #6 上下影线都不长, 比实体要小

            tmp_week1=week1_close-week1_open  # 这里的实体长度是纯 价格 因为下边一步 相除后就抵消了.
            week1_shangyingxian=week1_shangyingxian+0.001 # 为了防止除数为 0
            # print1()
            shiti_yingxian_jibei=tmp_week1/week1_shangyingxian
            if( shiti_yingxian_jibei >2): #实体的长度 大于 上影线的长度
                key_6=1


        # print1(key_0)
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(gaokai)
        # print1(shangyingxian_xiayingxian)
        # print1(jiagezhongshu_week1_shiti_yiban)
        # print1(week1_shiti)
        # print1(shiti_yingxian)



        if(key_0==1 and key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1 and key_6==1 ):
        # if(key_0==1 and key_1==1 and  key_2 ==1 and key_4==1 and key_5==1 and key_6==1 ):
        #     print1(shangyingxian_xiayingxian)
            info = ''
            info=info+'价格中枢-实体一半=' +str(jiagezhongshu_week1_shiti_yiban)
            info=info+'---上影线是下的几倍=' +str(shangyingxian_xiayingxian)
            info=info+'---阳线实体=' +str(week1_shiti)
            info=info+'---实体是影线的几倍=' +str(shiti_yingxian_jibei)

            info = info + "--价格中枢-看涨做涨--" + str(riqi)
            # print info
            # writeLog_to_txt(info, stockcode)

            path = BASE_DIR + '/jishu_stock/zJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                '%Y-%m-%d') + '.txt'

            jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试老师的案例
'''
def test_isAn_jiagezhognshu_KanZhangZuoZhang_laoshi():

    # 案例 1
    df = ts.pro_bar(ts_code='300157.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20200807')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_jiagezhognshu_KanZhangZuoZhang_model(data7_1, '300157.SZ')

    # 案例 2  得到的数据不对
    df = ts.pro_bar(ts_code='600089.SH', adj='qfq', freq='W', start_date='20170101', end_date='20201225')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_jiagezhognshu_KanZhangZuoZhang_model(data7_1, '600089.SH')

    # 案例 3 000155

    df = ts.pro_bar(ts_code='000155.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20201225')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_jiagezhognshu_KanZhangZuoZhang_model(data7_1, '000155.SZ')

    # 案例 4
    df = ts.pro_bar(ts_code='000409.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20210226')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_jiagezhognshu_KanZhangZuoZhang_model(data7_1, '000409.SZ')



'''
测试自己的案例
'''
def test_isAn_jiagezhognshu_KanZhangZuoZhang_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_jiagezhognshu_KanZhangZuoZhang_model(data7_1,'002507.SZ')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        data7_4 = df.iloc[22:42]  # 前10个交易日
        len_1=len(data7_4)
        for i in range(0, len_1 - 3 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_jiagezhognshu_KanZhangZuoZhang_model(data7_4[i:i + 3], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_jiagezhognshu_KanZhangZuoZhang(localpath1)
    test_isAn_jiagezhognshu_KanZhangZuoZhang_laoshi() #测试老师的案例