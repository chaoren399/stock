#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.aShengLv.huice.ShengLv_One_Two import jisuan_all_shouyilv_one_two
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
专门用来测试, 第 3 天买入, 第 4 天卖出的这种快速玩法的胜率,也就是赚多少钱

涨停板后 跳空的大阴线

想法来源: 
金海高科 2021年12月15日 昨天 是一个涨停板, 今天来了一个跳空高开的大阴线




ZTB_YinXian_TiaoKong

'''
chengongs=[]
chengongs1=[]
modelname='跳空缺口阴线'



def get_all_ZTB_YinXian_TiaoKong(localpath1):
    info1=  '--昨天 是一个涨停板, 今天来了一个跳空高开的大阴线  start--   '
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
        isAn_ZTB_YinXian_TiaoKong_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ZTB_YinXian_TiaoKong_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 4):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-4:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi =0  # 阳线的日期
        mairuriqi=0
        zhisundian=0

        mairujiage = 0
        maichujiage = 0
        # print1(data1)

        data2= data[len_data-4-1:len_data-4]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #1-昨天 是一个涨停板, 今天来了一个跳空高开的大阴线
        key_2=0; # 2阴线放量
        key_3=0  ; #3  阴线实体不能太大, 最好小于 1




        count=0
        day1_close=0
        day2_open=0
        day2_close=0
        day1_amount=0
        day2_amount=0
        day3_open=0
        day4_close=0
        day2_yinxian_shiti=0

        for index,row in data1.iterrows():
            if(index==0 and isZhangTingBan(row)==1):
                count=count+1
                day1_close=row['close']

                day1_amount=row['amount']
                zhisundian=row['low']
            if(index==1 and isYinXian(row)==1):
                count=count+1
                day2_open= row['open']
                day2_close= row['close']

                day2_amount=row['amount']

                riqi=row['trade_date']
                day2_yinxian_shiti=getShiTiDaXiao(row)
                mairuriqi = row['trade_date']

            if(index==2):
                #第 3 天 买入
                day3_open = row['open']
                mairujiage=day3_open

            if(index==3):
                #第 4 天卖出
                day4_close = row['close']
                maichujiage=day4_close


        if(count==2):
            if(day2_open > day1_close and day2_close > day1_close): #-1昨天 是一个涨停板, 今天来了一个跳空高开的大阴线
                key_1=1

            if(day1_amount < day2_amount): # 2阴线放量
                key_2=1
             # key_3=0  ; #3  阴线实体不能太大, 最好小于 1
            if(day2_yinxian_shiti <1):
                key_3=1




        # print1(key_1)
        # 增加 key_2  胜率提高  增加 key3 后 反而不好
        # if(key_1==1 and key_2==1 and key_3==1 ):
        if(key_1==1 and key_2==1 and key_3==1):
            info = ''
            ma60_10 = is_60_10_WEEK_ShangZhang(stockcode, mairuriqi)
            if (ma60_10['ma60xiangshang']==1):
                info = info + "--60周线向上--"
            if (ma60_10['ma10xiangshang']==1):
                info = info + "--10周线向下--"

            if(ma60_10['ma60xiangshang']==1 and ma60_10['ma10xiangshang']!=1):
                info = info + "--阴线实体"  + str(day2_yinxian_shiti)
                info = info + "--涨停板后 跳空的大阴线 成功了--"  + str(riqi)
                # print info
                writeLog_to_txt(info, stockcode)

                path = modelname+'.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)

                chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
                chengongs.append(chenggong_code)  #

                chenggong_code1={'stockcode':stockcode,'mairujiage':mairujiage,'maichujiage':maichujiage,'riqi':riqi}
                # print1(day2_shizixing_low)
                chengongs1.append(chenggong_code1)


'''
60周均线是不是一直上涨的
'''
def is_60_10_WEEK_ShangZhang(stock_code,riqi):
    # print1(riqi)
    df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20180101', end_date=str(riqi))

    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

    # 将 date 设定为 index
    df.set_index('trade_date', inplace=True)
    # print df
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行

    # print df
    df_week = df

    df_week['WeekMa10'] = df_week['close'].rolling(10).mean()
    df_week['WeekMa60'] = df_week['close'].rolling(60).mean()
    df_week['Week60-10'] = df_week['WeekMa60'] - df_week['WeekMa10']
    df_week['Week10-60'] = df_week['WeekMa10'] - df_week['WeekMa60']  # G8 买 2 用到

    df_week = df_week.dropna(how='any', axis=0)  # 删除 列数据为空的 的行
    df_week.sort_index(axis=1, ascending=False)
    df_week = df_week.sort_values(by='trade_date', axis=0, ascending=False)  # 按照日期 从新到旧 排序
    # print  df_week[0:10]
    df_week = df_week[0:8] #一年有 48 周
    df_week1 = df_week[0:3] #一年有 48 周
    WeekMa60=[]
    WeekMa10=[]
    for index, row in df_week.iterrows():
        WeekMa60.append(row['WeekMa60'])
    for index, row in df_week1.iterrows():
        WeekMa10.append(row['WeekMa10'])

    # print1(WeekMa10)
    # print1(WeekMa60)



    ma60xiangshang=0
    ma10xiangshang=0
    if(is_big_to_small(WeekMa60)==1):
        ma60xiangshang=1
        # return 1
    if(is_small_to_big(WeekMa10)==1): #
        ma10xiangshang=1
        # return 2
    ma60_10 = {'ma60xiangshang': ma60xiangshang, 'ma10xiangshang': ma10xiangshang}
    return ma60_10




'''
测试老师的案例

  '000030.SZ:20211115',
  '000400.SZ:20211115',
  '000998.SZ:20211110',
  '002006.SZ:20211116',
  '002017.SZ:20211110',
  
'''
def test_isAn_ZTB_YinXian_TiaoKong_laoshi():

    # 案例 1
    df1 = ts.pro_bar(ts_code='000030.SZ',adj='qfq', start_date='20210206', end_date='20211117')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZTB_YinXian_TiaoKong_model(data7_1,'000030.SZ')
    # 案例 2 000400
    df1 = ts.pro_bar(ts_code='000400.SZ',adj='qfq', start_date='20210206', end_date='20211117')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZTB_YinXian_TiaoKong_model(data7_1,'000400.SZ')
    # 案例 3
    df1 = ts.pro_bar(ts_code='000998.SZ',adj='qfq', start_date='20210206', end_date='20211112')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZTB_YinXian_TiaoKong_model(data7_1,'000998.SZ')
    # 案例 4
    df1 = ts.pro_bar(ts_code='002006.SZ',adj='qfq', start_date='20210206', end_date='20211118')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZTB_YinXian_TiaoKong_model(data7_1,'002006.SZ')

    # 案例 6    '002017.SZ:20211110',
    df1 = ts.pro_bar(ts_code='002017.SZ',adj='qfq', start_date='20210206', end_date='20211112')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZTB_YinXian_TiaoKong_model(data7_1,'002017.SZ')

'''
测试自己的案例
'''
def test_isAn_ZTB_YinXian_TiaoKong_ziji():
    #自己的 --60周线向上----阴线实体0.15--涨停板后 跳空的大阴线 成功了20211109--科达制造--强势股票**600499.SH

    # '603010.SH--mairu_riq:20210602--maichu_riq:20210615'
    df1 = ts.pro_bar(ts_code='603010.SH',adj='qfq', start_date='20200206', end_date='20210603')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZTB_YinXian_TiaoKong_model(data7_1,'603010.SH')

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
        n=5


        # data7_4 = df.iloc[22:22+n+10]  #1 个月
        # data7_4 = df.iloc[22:22+n+22]  #1 个月
        data7_4 = df.iloc[22:22+n+120]  # 半年
        # data7_4 = df.iloc[22:22+132+250]  # 1年

        len_1=len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ZTB_YinXian_TiaoKong_model(data7_4[i:i + n], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()

    jisuan_all_shouyilv_one_two(chengongs1, modelname)

    jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    # jisuan_all_shouyilv(chengongs, modelname, 1.30)



if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_ZTB_YinXian_TiaoKong(localpath1)
    # test_Befor_data()
    test_isAn_ZTB_YinXian_TiaoKong_ziji()
    # test_isAn_ZTB_YinXian_TiaoKong_laoshi()



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"