#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
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
有惊无险1
https://www.yuque.com/chaoren399/eozlgk/vehqag
筑底后缓慢.上涨  (这里没说是 第一天是不是阳线, 但是案例都是阳线, 所以我的程序也是阳线)
高开中/大阴线(高开低走)
有惊无险1 ①之后3天价格不能跌破阴线的最低价,第4天买入


有惊无2②3天内阳线收盘价超过洗盘阴线的开盘价


思路: 
找到 5 天数据 判断是还不是 高开低走,  中/大阴线,  

改进, 拿到最近 60 天数据, 后在来判断 2022年02月12日 修改

'''
chengongs=[]
modelname='有惊无险1'
def get_all_YouJingWuXian1(localpath1):
    info1=  '--有惊无险1 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:132]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_YouJingWuXian1_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YouJingWuXian1_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 65):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-5:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0


        data2= data[len_data-5-60:len_data-5]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,




        # 设置两个 key
        key_1=0; # 判断是不是 高开低走 的大阴线, 而且是近30 天期的最高点,
        key_2=0; # 中/大阴线,
        key_3=0 # 之后 3 天的最低价 不跌破 大阴线的最低价
        key_4=1# 大阴线的 开盘价  是近30 天期的最高点,


        count=0
        day0_open=0
        day0_close=0
        day1_yinxian_shiti=0
        day1_yinxian_open=0
        day1_yinxian_low=0
        day2_low=0
        day3_low=0
        day4_low=0

        for index, row in data1.iterrows():
            if(index==0):
                day0_open= row['open']
                day0_close= row['close']
            if(index==1 and isYinXian(row)==1 ): # 大阴线
                day1_yinxian_open=row['open']
                day1_yinxian_low=row['low']
                count=count+1
                day1_yinxian_shiti = getShiTiDaXiao(row)
                zhisundian=row['low']
                riqi=row['trade_date']
            # 之后 3 天的最低价 不跌破 大阴线的最低价
            if(index==2):
                day2_low = row['low']
            if(index==3):
                day3_low = row['low']
            if(index==4):
                day4_low = row['low']
                mairuriqi=row['trade_date']

        if(count==1):
            if(day1_yinxian_open > day0_open and day1_yinxian_open > day0_close):
                key_1=1 # 判断是不是 高开低走
            if(day1_yinxian_shiti >1.6):
                key_2=1 # 中/大阴线,

            if(day2_low > day1_yinxian_low and day3_low > day1_yinxian_low and day4_low > day1_yinxian_low ):

                key_3=1 #之后 3 天的最低价 不跌破 大阴线的最低价

        for index,row in data2.iterrows():
            day_open= row['open']
            day_close= row['close']
            if(day_open > day1_yinxian_open or day_close > day1_yinxian_open ):
                key_4=0

        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(stockcode)
        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 ):

            info = ''
            # info=info+'阴线大小='+str(day2_yinxian_shiti)
            info = info + "-----有惊无险1" + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '有惊无险1.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_YouJingWuXian1_laoshi():
    # 案例 1------有惊无险1 ----000420.SZ ----20210813--吉林化纤--强势股票
    df1 = ts.pro_bar(ts_code='000420.SZ', start_date='20200206', end_date='20210819')
    data7_1 = df1.iloc[0:132]  # 前7行
    # print data7_1
    isAn_YouJingWuXian1_model(data7_1,'000420.SZ')

    # 案例 2-----有惊无险1 ----600188.SH ----20210831--兖州煤业
    df1 = ts.pro_bar(ts_code='600188.SH',adj='qfq', start_date='20210206', end_date='20210906')
    data7_1 = df1.iloc[0:132]  # 前7行
    # print data7_1
    isAn_YouJingWuXian1_model(data7_1,'600188.SH')

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_YouJingWuXian1_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_YouJingWuXian1_model(data7_1,'002507.SZ')

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
        n=65
        data7_4 = df.iloc[22:42]  # 前10个交易日
        data7_4 = df.iloc[22:22+n+22]  # 1 个月
        # data7_4 = df.iloc[22:22+n+120]  # 半年
        len_1=len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_YouJingWuXian1_model(data7_4[i:i + n], stock_code)


    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)

if __name__ == '__main__':

    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_YouJingWuXian1(localpath1)
    # test_isAn_YouJingWuXian1_laoshi()
    test_Befor_data()

    # jisuan_all_shouyilv(chengongs, modelname, 1.07)

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"