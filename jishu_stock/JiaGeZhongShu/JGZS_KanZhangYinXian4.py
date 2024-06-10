#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import *
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
创建日期:2021年11月03日
更新日期:
价格中枢-看涨阴线4 (没有 3,只有 1,2,4 ,3是看跌阴线)
https://www.yuque.com/chaoren399/eozlgk/fk21cv/


价格中枢看涨阴线4
开盘价为最高价的大实体阴线有下影线
连续下跌为前提收盘价在价格中枢之下
第2周阳线收盘价在第1周收盘价之上
后期看涨50%+


JGZS_KanZhangYinXian4

'''

def get_all_JGZS_KanZhangYinXian4(localpath1):
    info1=  '--价格中枢-看涨阴线4 https://xueqiu.com/3476656801/202337480 --   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        # stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"

        df = pd.read_csv(stockdata_path, index_col=0)
        df = df.reset_index(drop=False)

        data6_1 = df.iloc[0:6]  # 前6行
        # data6_1 = df.iloc[2:8]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_JGZS_KanZhangYinXian4_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JGZS_KanZhangYinXian4_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >=2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        # print1 (data)

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        # 设置两个 key

        key_1=0; # 1 开盘价 为最高价 ,可以有一点 上影线的存在
        key_2=0; # 2 有下影线 不能太长
        key_3=0; # 3 收盘价在价格中枢之下
        key_4=0; # 4 第 2 周阳线收盘价在第一周收盘价之上
        key_5=0; # 5 阴线的实体必须大
        key_6=0; # 6 经回测发现阳线的实体不能太小


        count=0
        week1_high=0
        week1_open=0
        week1_close=0
        week1_low=0
        week1_jiagezhongshu=0
        week1_shiti=0
        week2_shiti=0

        for index,row in data1.iterrows():
            if(index==0 and isYinXian(row)==1):
                count=count+1
                week1_high=row['high']
                week1_open=row['open']
                week1_close=row['close']
                week1_low=row['low']
                week1_shiti=getShiTiDaXiao(row)

            if(index==1 and isYangXian(row)==1):
                count=count+1
                week2_close=row['close']
                week2_shiti=getShiTiDaXiao(row)


        if(count==2): #满足一阳一阴 才继续

            # 1 开盘价 为最高价 ,可以有一点 上影线的存在
            week1_shangyingxian = round(((week1_high - week1_open) / week1_open) * 100, 2)
            # print1(week1_xiayingxian)
            # if (week1_shangyingxian < 0.5):  # 两个案例 0.21,0.0,0.0
            if (week1_shangyingxian == 0):  # 两个案例 0.21,0.0,0.0
                key_1=1
            # 2 有下影线 不能太长

            week1_xiayingxian= (week1_close - week1_low) +0.0001

            week1_shitidaxiao=week1_open-week1_close
            # week1_shiti_xiayingxian_beishu=week1_shitidaxiao / week1_xiayingxian
            week1_shiti_xiayingxian_beishu = round(week1_shitidaxiao / week1_xiayingxian, 2)

            if(week1_shiti_xiayingxian_beishu >1.5):  #两个案例4.4,3.25 1.8
                key_2=1

            #3 收盘价在价格中枢之下
            week1_jiagezhongshu=round((week1_high + week1_low)/2 ,2)
            if(week1_close < week1_jiagezhongshu):
                key_3=1
            #4 第 2 周阳线收盘价在第一周收盘价之上

            if(week2_close > week1_close):
                key_4=1

            # 5 阴线的实体必须大
            if(week1_shiti>3.6):
                key_5=1

            # 6 经回测发现阳线的实体不能太小
            if(week2_shiti >0):
                key_6=1



        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(week1_shiti)
        # print1(week1_shangyingxian)
        # print1(week1_shiti_xiayingxian_beishu)
        # print1(week2_shiti)





        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1):
            info = ''
            info = info + "--价格中枢看涨阴线4--" + str(riqi)
            info=info+'上影线最好为0='+str(week1_shangyingxian)
            info=info+'--实体下影线倍数='+str(week1_shiti_xiayingxian_beishu)
            info=info+'--阴线实体='+str(week1_shiti)
            info=info+'--阳线实体='+str(week2_shiti)



            # # 统一 info管理 一个函数,每次都要执行, 并且信息 返回后,要添加到 info中,
            # # 方便后期修改,这样一改,所有的都可以执行了.
            # from jishu_stock.z_tool.InfoTool import manage_info
            # manage_info = manage_info(info, stockcode, riqi, '')
            # info = info + manage_info


            path = BASE_DIR + '/jishu_stock/zJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                '%Y-%m-%d') + '.txt'

            jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)

            path = '价格中枢看涨阴线4.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)


'''
测试老师的案例
'''
def test_isAn_JGZS_KanZhangYinXian4_laoshi():
    # 案例 1  300016
    df = ts.pro_bar(ts_code='300016.SZ', adj='qfq', freq='W', start_date='20110101', end_date='20120406')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    isAn_JGZS_KanZhangYinXian4_model(data7_1, '300016.SZ')

    # 案例 2 ：
    df = ts.pro_bar(ts_code='600106.SH', adj='qfq', freq='W', start_date='20010101', end_date='20031226')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    isAn_JGZS_KanZhangYinXian4_model(data7_1, '600106.SH')


    # 案例 3 ：
    df = ts.pro_bar(ts_code='000099.SZ', adj='qfq', freq='W', start_date='20010101', end_date='20130705')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    isAn_JGZS_KanZhangYinXian4_model(data7_1, '000099.SZ')



def test_bendi_shuju():
    stock_code = '000100.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    data7_1=df.loc['2020-05-03':'2020-04-12' ]
    print data7_1
    isAn_JGZS_KanZhangYinXian4_model(data7_1, '000100.SZ')
'''
测试自己的案例
'''
def test_isAn_JGZS_KanZhangYinXian1_ziji():
    #自己的 案例  ---价格中枢看涨阴线1--2021-10-17--雪峰科技--强势股票**603227.SH

    #不是回调状态----实体是影线的2.1--2021-10-17--东尼电子**603595.SH
    #----山西焦煤**000983.SZ

    df = ts.pro_bar(ts_code='603595.SH', adj='qfq', freq='W', start_date='20170101', end_date='20211022')
    data7_1 = df.iloc[0:6]  # 1 年有 50 周
    # print data7_1
    isAn_JGZS_KanZhangYinXian4_model(data7_1, '603595.SH')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']

        # stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
            # print df
        if (df.empty):
            continue

        df = df.reset_index(drop=False)  # 重新建立索引 ,
        # data7_4 = df.iloc[0:6]  # 1 年有 52 周
        data7_4 = df.iloc[8:12]  # 1 年有 52 周
        # data7_4 = df.iloc[12:15]  # 1 年有 52 周

        len_1=len(data7_4)
        for i in range(0, len_1 - 2 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JGZS_KanZhangYinXian4_model(data7_4[i:i + 2], stock_code)





if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_JGZS_KanZhangYinXian4(localpath1)
    # test_isAn_JGZS_KanZhangYinXian4_laoshi()  #
    # test_ziaxian_zhuan_Week()
    # test_isAn_JGZS_KanZhangYinXian4_ziji()
    # test_Befor_data()