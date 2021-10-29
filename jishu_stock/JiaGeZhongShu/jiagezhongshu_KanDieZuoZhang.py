#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd

from jishu_stock.GeShiBaFa.Get_Week_K_data_From_Ts import getAllWeekKdata
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename, writeLog_to_txt_path, jiagezhongshu_writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.PyDateTool import get_date1_date2_days
from jishu_stock.z_tool.getMin_Max import getMin_fromDataFrame
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
价格中枢 看跌做涨
https://www.yuque.com/chaoren399/eozlgk/va1wks/

前提: 下跌谷底, 筑底后的低位

周K线有.上影线的阳线
上影线比实体长一倍以上
占全部K线的一-半以上

收盘价在价格中枢之?下
1下跌后筑底的低位
以这波下跌最低价做止损
第二周最好低开
周中(周四或周五)
之后价格围绕开盘价小幅波动(小K线)
后期先看跌后看涨周中逢低买入

思路  获取周线的最后 2 个数据, 判断 第一个数据是不是符合


完成 key1- key6 , 但是满足条件的很多, 所以要判断 ,最低点 与 目前为数据 差距多少个数值

思路循环 第一遍找到最小值, 然后  循环第 2 遍 计算 距离 
KanDieZuoZhang

案例 3 600006 东风汽车   上影线比实体长1倍=1.90909090909  
'''

def get_all_jiagezhongshu_KanDieZuoZhang(localpath1):
    info1=  '--价格中枢 看跌做涨 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    if (len(data) > 0):

        # print len(data)
        # print '1111111'
        for index, row in data.iterrows():
            stock_code = row['ts_code']
            stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                continue

            df = df.reset_index(drop=False)  # 重新建立索引 ,
            df = df.iloc[0:100]  # 1 年有 52 周
            # df = df.iloc[1:101]  # 1 年有 52 周
            # 1 m 是 上涨的部分 之选 2-4 周
            # 2 n 是下降部分  选择 4-10
            # df=df.iloc[2:8]  # 只找最近 1 个月的
            # print df

            isAn_KanDieZuoZhang_model(df, stock_code)
            count = count + 1
'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_KanDieZuoZhang_model(data,stockcode):
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
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        # 第 1 周
        key_1=0; # 第一周是阳线
        key_2=0; #上影线比 实体长 1 倍
        key_3=0; #上影线占全部 k线的一半以上
        key_4=0; # 第一周阳线的收盘价 在价格中枢之下

        #第 2 周
        # 下一周阴阳无所谓，但最好低开（即开盘价低于上一周的收盘价），
        # 并且是小实体的周K线，这周价格围绕上一周的开盘价小幅波动；
        key_5=0 ;#小实体的周K线
        key_6=0; # 最好低开 这周价格围绕上一周的开盘价小幅波动；


        week1_high=0
        week1_open=0
        week1_close=0
        week1_low=0

        week2_shiti=0
        week2_close=0
        week2_high=0
        week2_low=0
        for index, row in data1.iterrows():
            if(index==0): # 第一周
                if(isYangXian(row)==1): #第一周是阳线
                    key_1=1
                # 判断上影线
                week1_high=row['high']
                week1_open=row['open']
                week1_close=row['close']
                week1_low=row['low']


            if(index==1):  # 第 2 周
                # print week1_close
                week2_open=row['open']
                week2_close=row['close']
                week2_shiti = getShiTiDaXiao(row)

                week2_high=row['high']
                week2_low=row['low']
                #阳线 最好低开 这周价格围绕上一周的开盘价小幅波动；
                if(week2_low <week1_close and week2_high > week1_close):
                    if(week2_open <=week1_close ): #最好低开（即开盘价低于上一周的收盘价）
                        key_6=1




        week1_shangyingxian_changdu=week1_high-week1_close
        week1_shiti_changdu = week1_close - week1_open
        if(week1_shiti_changdu>0):  #除数必须大于 0 ,而且 第一周必须有实体才可以
            shangyingxian_bi_shiti= format(week1_shangyingxian_changdu / week1_shiti_changdu,'.2f')

            if(float(shangyingxian_bi_shiti) > 1.9):#上影线比 实体长 1 倍
                key_2=1

        # 3上影线占全部 k线的一半以上
        week1_quanbu_changdu=week1_high -week1_low
        if(week1_shangyingxian_changdu > week1_quanbu_changdu/2):
            key_3=1
        #4第一周阳线的收盘价 在价格中枢之下
        jiage_zhongshu=  (week1_high + week1_low ) / 2 #● 价格中枢 = ( 最高价 + 最低价) ÷ 2
        if(week1_close  < jiage_zhongshu):
            key_4=1


        #----第二部分---- 判断第 2 周
        if(week2_shiti < 1.5 and week2_shiti>0.1): # 小实体
            key_5=1

        # print1(data1)
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(key_6)
        # print1(week1_shangyingxian_changdu)
        # print1(week1_shiti_changdu)
        # print '上影线比实体长1倍=' +str(week1_shangyingxian_changdu / week1_shiti_changdu)
        # print1(week1_quanbu_changdu)
        # print1(week2_shiti)
        # print1(week1_close)
        # print1(jiage_zhongshu)
        # print1(week2_shiti)
        # print1(week2_open)
        # print1(week2_close)

        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1 and key_6==1):
            row = getMin_fromDataFrame(data)
            min_date = row['trade_date']
            days = get_date1_date2_days(min_date, riqi)
            # print1(days/7)
            if( (days/7)< 13):

                info = ''
                info=info+'价格中枢='+str(jiage_zhongshu)
                info=info+'-第2周最高价='+str(week2_high)
                # info=info+'-上影线长度='+str(week1_shangyingxian_changdu)#week1_shangyingxian_changdu > week1_quanbu_changdu
                # info=info+'-全部长度='+str(week1_quanbu_changdu)#week1_shangyingxian_changdu > week1_quanbu_changdu
                info=info+'-与最小值相差'+str(days/7)+'周'
                info=info+'-上影线比实体长1倍大于2最好='+str(shangyingxian_bi_shiti)
                info = info + "-----价格中枢 看跌做涨  成功了" + ' ----' + stockcode + ' ----' + str(riqi)

                path = BASE_DIR + '/jishu_stock/zJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                    '%Y-%m-%d') + '.txt'

                jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)







'''
测试老师的案例
'''
def test_isAn_KanDieZuoZhang_laoshi():
    # 案例 1
    # df1 = ts.pro_bar(ts_code='000408.SZ',adj='qfq', start_date='20210206', end_date='20210518')
    # data7_1 = df1.iloc[0:30]  # 前7行
    # # print data7_1
    # isAn_KanDieZuoZhang_model(data7_1,'002174.SZ')




    # 案例 1 000070  特发信息 这个案例 只能在 同花顺 选择 除权 才能 对上数据,
    df = ts.pro_bar(ts_code='000070.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20181206')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    # print data7_1
    isAn_KanDieZuoZhang_model(data7_1, '000070.SZ')

    # 案例 2   000516.SZ ----20200522--国际医学
    df = ts.pro_bar(ts_code='000516.SZ',  adj='qfq',freq='W', start_date='20170101', end_date='20200529')
    data7_1 = df.iloc[0:100]  # 前7行
    isAn_KanDieZuoZhang_model(data7_1, '000516.SZ')

    # 案例 3 600006 东风汽车   上影线比实体长1倍=1.90909090909
    df = ts.pro_bar(ts_code='600006.SH',  adj='qfq',freq='W', start_date='20170101', end_date='20190118')
    data7_1 = df.iloc[0:100]  # 前7行
    isAn_KanDieZuoZhang_model(data7_1, '600006.SH')

'''
测试自己的案例
'''
def test_isAn_KanDieZuoZhang_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002958.SZ',adj='qfq',freq='W',  start_date='20210206', end_date='20211025')
    data7_1 = df1.iloc[0:100]  # 前7行
    isAn_KanDieZuoZhang_model(data7_1,'002958.SZ')
    #价格中枢=3.97-与最小值相差10周-上影线比实体长1倍 大于2最好=8.00--
    # ---价格中枢 看跌做涨  成功了 ----002958.SZ ----20211015--青农商行

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']

        stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
            # print df
        if (df.empty):
            continue

        df = df.reset_index(drop=False)  # 重新建立索引 ,
        data7_4 = df.iloc[30:138]  # 1 年有 52 周

        len_1=len(data7_4)
        for i in range(0, len_1 - 100 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_KanDieZuoZhang_model(data7_4[i:i + 100], stock_code)



if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    getAllWeekKdata(localpath1) #每周运行钱需要先下载数据
    get_all_jiagezhongshu_KanDieZuoZhang(localpath1)
    # test_isAn_KanDieZuoZhang_laoshi()
    # test_Befor_data()
    # test_isAn_KanDieZuoZhang_ziji()