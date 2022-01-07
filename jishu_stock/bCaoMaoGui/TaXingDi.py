#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.aShengLv.huice.ShengLv_10_5 import jisuan_all_shouyilv_10_5
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi

from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
塔形底
https://www.yuque.com/chaoren399/byftms/vnzxrp

下跌趋势 末端
先大阴线, 后大阳线, 当中夹杂小阴阳
当中 小阴小阳 越多越好, 效果越好
典型的见底信号, 后市看涨

思路: 
先判断今天 是不是 大阳线, 且放量,

然后 去 22 日交易数据,找到 大阴线, 放量 

然后找到  从大阴线到大阳线 之间的数组. 判断 
实体比较小, 并且 最高价 低于大阴线的开盘价


TaXingDi
'''
chengongs=[]
modelname='塔形底'

isHuiceKey = 0
def get_all_TaXingDi(localpath1):
    info1=  '--塔形底 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_TaXingDi_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_TaXingDi_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 15):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-15:len_data]
        data1 = data1.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 倒序排
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        # 设置两个 key
        key_1=0; #第一天是不是 大阳线
        key_2=0; # 大阴线

        key_3=1; # 中间的小实体 都小于 4
        key_4=1; # 中间的 最高价 都小于 大阴线的开盘价
        key_5=0 ; # 大阳线的收盘价 大于 大阴线的开盘价
        key_6=0; # 大阳线 与大阴线之间必须大于 5
        key_7=0; #大阴线 的开盘价 大于 大阳线的价格中枢

        day1_yangxian_shiti=0
        day2_yinxian_open=0
        day1_yangxian_close=0
        day1_yangxian_open=0
        day2_yinxian_riqi=0
        day1_yangxian_jiagezhognshu =0
        day2_yinxian_jiagezhognshu =0
        for index, row in data1.iterrows():
            if(index==0 and isYangXian(row)==1 ):  # 大阳线
                day1_yangxian_shiti=getShiTiDaXiao(row)
                if(day1_yangxian_shiti> 4):
                    # print1(row['trade_date'])
                    day1_yangxian_close=row['close']
                    day1_yangxian_open=row['open']
                    mairuriqi= row['trade_date']
                    day1_yangxian_jiagezhognshu = round((row['high'] + row['low']) / 2, 2)
                    key_1=1
                break
        if(key_1==1):
        # if(0):

            #从大阳线后边的数据中找 大阴线
            lendata1=len(data1)
            data2 = data1[1:lendata1]
            data2 = data2.reset_index(drop=True)  # 重新建立索引 , 倒序, 从阳线后开始找大阴线
            # print1(data2)

            count=0
            day2_yinxian_shiti=0
            for index,row in data2.iterrows():
                count=count+1
                if(isYinXian(row)==1):
                    day2_yinxian_shiti=getShiTiDaXiao(row)
                    if(day2_yinxian_shiti > 7):         #大阴线
                        # print1(day2_yinxian_shiti)
                        # print1(row['trade_date'])
                        day2_yinxian_open = row['open']
                        day2_yinxian_riqi=row['trade_date']
                        day2_yinxian_jiagezhognshu = round((row['high'] + row['low']) / 2, 2)
                        key_2=1
                        break
            # print1(count)
            if(count>=5): # 总结规律, 一般 5 个交易内比较合适
                # key_6 = 0;  # 大阳线 与大阴线之间必须大于 5
                key_6=1
                data3= data2[0:count-1]  #大阳线到  大阴线之间的数据
                # print1(data3)
                for index, row in data3.iterrows():
                    day_shiti = getShiTiDaXiao(row)
                    #  key_3=0; # 中间的小实体 都小于 4.5
                    if(day_shiti > 4.5):
                        key_3=0

                    #key_4=0; # 中间的 最高价 都小于 大阴线的开盘价
                    if(row['open'] > day2_yinxian_open):
                        key_4=0


                    # print1(getShiTiDaXiao(row))

                zhisundian= getMin_low_fromDataFrame(data3)

            # key_5=0 ; # 大阳线的收盘价 大于 大阴线的开盘价
            if(day1_yangxian_close > day2_yinxian_open ):
                key_5=1
            #key_7=0; #大阴线 的开盘价 大于 大阳线的价格中枢
            if(day2_yinxian_open > day1_yangxian_jiagezhognshu ):
                key_7=1

        if(isHuiceKey == 1):
            print1(key_1)
            print1(key_2)
            print1(key_3)
            print1(key_4)
            print1(key_5)
            print1(key_5)
            print1(key_7)
            print1(day1_yangxian_shiti)
            print1(day2_yinxian_shiti)
            print1(zhisundian)
            print1(day2_yinxian_open)
            print1(day2_yinxian_riqi)
            print1(day1_yangxian_jiagezhognshu)
            print1(day2_yinxian_jiagezhognshu)
        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1 and key_6==1 and key_7==1 ):
            info = ''

            info = info + "大阴线实体="+str(day2_yinxian_shiti)
            info = info + "大阳线实体="+str(day1_yangxian_shiti)
            info = info + "--塔形底 成功了--"  +str(day2_yinxian_riqi)+'--'+ str(mairuriqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = modelname + '.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            # print1(day2_shizixing_low)
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_TaXingDi_laoshi():
    # 案例 1 002463 --塔形底 成功了20190603--沪电股份**002463.SZ
    df1 = ts.pro_bar(ts_code='002463.SZ',adj='qfq', start_date='20180206', end_date='20190603')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_TaXingDi_model(data7_1,'002463.SZ')

    # 案例 2 晶盛机电 300316  20190130

    df1 = ts.pro_bar(ts_code='300316.SZ',adj='qfq', start_date='20180206', end_date='20190130')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_TaXingDi_model(data7_1,'300316.SZ')

    # 案例 3  至纯科技 603690 20191206

    df1 = ts.pro_bar(ts_code='603690.SH',adj='qfq', start_date='20180206', end_date='20191206')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_TaXingDi_model(data7_1,'603690.SH')

'''
测试自己的案例
'''
def test_isAn_TaXingDi_ziji():
    #自己的 案例 大阴线实体=5.69大阳线实体=9.65--塔形底 成功了20211108--中国宝安--强势股票**000009.SZ
    #大阴线实体=8.68大阳线实体=5.32--塔形底 成功了--20211105--20211112--新疆众和**600888.SH
    df1 = ts.pro_bar(ts_code='600888.SH',adj='qfq', start_date='20210206', end_date='20211112')
    data7_1 = df1.iloc[0:15]  # 前7行
    isAn_TaXingDi_model(data7_1,'600888.SH')


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



        data7_4 = df.iloc[22:22 + 15 + 22]  # 1 个月
        # data7_4 = df.iloc[22:22+132+120]  # 半年
        # data7_4 = df.iloc[22:22+132+250]  # 1年

        len_1=len(data7_4)
        for i in range(0, len_1 - 15 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_TaXingDi_model(data7_4[i:i + 15], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    # jisuan_all_shouyilv(chengongs, modelname, 1.03)
    # jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)

    jisuan_all_shouyilv_10_5(chengongs, modelname, 1.10, 0.95)
    jisuan_all_shouyilv_10_5(chengongs, modelname, 1.10, 0.90)


if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_TaXingDi(localpath1)

    # test_isAn_TaXingDi_laoshi()
    test_Befor_data()
    # isHuiceKey = 1
    # test_isAn_TaXingDi_ziji()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"