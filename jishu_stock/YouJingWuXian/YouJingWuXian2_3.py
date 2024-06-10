#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
有惊无险2-3  第一天大阴线, 第 2,3  天如果是阳线 收盘价 不能超过 阴线的开盘价 (最低价呢?), 
 第 4 天 阳线收 盘价 超过阴线开盘价
https://www.yuque.com/chaoren399/eozlgk/vehqag

有惊无2②
3天内阳线收盘价超过洗盘阴线的开盘价


思路: 
我把 有惊无险 2  分成,  有惊无险2-1,有惊无险 2-2,有惊无险 2-3

有惊无险2-1  第一天突破 阳线
找到 大阴线, 后判断 阳线收盘价超过洗盘阴线的开盘价

有惊无险2-2  第2天突破 阳线
找到 大阴线, 后判断 之后1天价格不能跌破阴线的最低价
有惊无险2-3  第3天突破 阳线
找到 大阴线, 后判断 之后2天价格不能跌破阴线的最低价

先把 有惊无险2-1 做了 找3 个数据

YouJingWuXian2_3

'''
chengongs=[]
modelname='有惊无险2_3'

def get_all_YouJingWuXian2_3(localpath1):
    info1=  '--有惊无险2_3start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:300]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_YouJingWuXian2_3_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_YouJingWuXian2_3_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    # if(len_data >= 125):
    if(len_data >= 65):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-5:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)
        mairuriqi = 0
        zhisundian = 0



        # 设置两个 key  第一天大阴线, 第 2 天 阳线收 盘价 超过阴线开盘价
        key_1=0; # 判断是不是 高开低走,
        key_2=0; # 中/大阴线,
        key_3=0 # 找到 大阴线, 后判断 阳线收盘价超过洗盘阴线的开盘价
        key_4 = 1  # 大阴线的 开盘价  是近30 天期的最高点,

        key_5=1 # 第 第 2,3 天 开盘价 收盘价 不能超过 阴线的开盘价

        # data2= data[len_data-5-120:len_data-5]  # 测试 半年内最大值的胜率
        data2= data[len_data-5-60:len_data-5]  # 测试 1 年内最大值的胜率
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        count=0
        day0_open=0
        day0_close=0
        day1_yinxian_shiti=0
        day1_yinxian_open=0

        day2_open=0
        day2_close=0
        day3_open=0
        day3_close=0

        day4_yangxian_close=0
        for index,row in data1.iterrows():
            if(index==0):
                day0_open=row['open']
                day0_close=row['close']

            if(index==1 and isYinXian(row)==1): #大阴线

                day1_yinxian_open=row['open']
                count=count+1
                day1_yinxian_shiti = getShiTiDaXiao(row)
                zhisundian=row['low']
                riqi=row['trade_date']

            if(index==2 ):
                day2_open=row['open']
                day2_close=row['close']
            if(index==3 ):
                day3_open=row['open']
                day3_close=row['close']

            if(index==4 and isYangXian(row)==1): #阳线收盘价高过阴线开盘价
                day4_yangxian_close=row['close']
                count = count + 1
                mairuriqi=row['trade_date']
        if(count==2): #符合 阴阳
            if(day1_yinxian_open > day0_open and day1_yinxian_open > day0_close):
                key_1=1

            if(day1_yinxian_shiti>1.6):
                key_2=1
            if(day4_yangxian_close > day1_yinxian_open):
                key_3=1
            if(day2_close > day1_yinxian_open or day2_open > day1_yinxian_open or
                    day3_open > day1_yinxian_open or day3_close > day1_yinxian_open ):#第23天收盘价不能高过阴线
                key_5=0

        for index,row in data2.iterrows():
            day_open= row['open']
            day_close= row['close']
            if(day_open > day1_yinxian_open or day_close > day1_yinxian_open ):
                key_4=0


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(day2_yinxian_shiti)
        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1):
            info = ''
            # info=info+'阴线大小='+str(day2_yinxian_shiti)
            info = info + "-----有惊无险2_3-----" + str(riqi)
            # print info

            # 统一 info管理 一个函数,每次都要执行, 并且信息 返回后,要添加到 info中,
            # 方便后期修改,这样一改,所有的都可以执行了.
            from jishu_stock.z_tool.InfoTool import manage_info
            manage_info = manage_info(info, stockcode, riqi, '')
            info = info + manage_info

            writeLog_to_txt(info, stockcode)
            path = '有惊无险2.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_YouJingWuXian2_3_laoshi():
    # 案例 1-阴线大小=3.38-----有惊无险2-1 ----300114.SZ ----20210802----强势股票
    df1 = ts.pro_bar(ts_code='300114.SZ',adj='qfq', start_date='20210206', end_date='20210804')
    data7_1 = df1.iloc[0:65]  # 前7行
    # print data7_1
    isAn_YouJingWuXian2_3_model(data7_1,'300114.SZ')



    # 案例 3

'''
测试自己的案例
'''
def test_isAn_YouJingWuXian2_3_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_YouJingWuXian2_3_model(data7_1,'002507.SZ')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
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
            isAn_YouJingWuXian2_3_model(data7_4[i:i + n], stock_code)


    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_YouJingWuXian2_3(localpath1)
    # test_isAn_YouJingWuXian2_3_laoshi()
    test_Befor_data()

