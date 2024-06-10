#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian, isYinXian, \
    writeLog_to_txt_path_getcodename, getMin_low_fromDataFrame
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from jishu_stock.z_tool.isXiongShiMoQi import hasXiongShiMoQi
from stock.settings import BASE_DIR

''''
柳暗花明 底部反转模型
https://www.yuque.com/chaoren399/eozlgk/bl5cum

熊市末期急速下跌
连续3日以上的阴线
包含低开和大阴线
止跌阳线阳线的收盘价高过前一日阴线开盘价
以最低点作为止损

思路: 找到 4个数据

编写日期: 2021年10月15日
更新日期: 2021年11月28日

新方法:
扎到 60天数据,
分为 2 个数组, 第一个数组包含 今天和昨天B的数据, 判断昨天是不是最低点, 今天是不是阳线符合条件.

第 2 个数组 的最低点必须 大于 昨天B, 并且 有熊市末期,急速下跌

柳暗花明 底部强势上涨  , 每天标记 ,后期出现 比如出水芙蓉等模型可以加仓
'''
chengongs=[]
modelname='柳暗花明'

def get_all_LiuAnHuaMing2(localpath1):
    info1=  '--柳暗花明 底部反转模型  每天标记 ,后期出现 比如出水芙蓉等模型可以加仓--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:136]  # 前6行
        # data6_1 = df.iloc[1:136]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_LiuAnHuaMing2_model(data6_1, stock_code)

'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_LiuAnHuaMing2_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 14):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1=data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        # print1( data1)
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0

        data2 = data[len_data - 2-130:len_data - 2] #
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        data3 = data[len_data-10:len_data - 1]  #
        data3 = data3.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; #1判断是不是止跌沿线,
        key_2=0; #2是否有 熊市末期

        key_3=0; # 3 判断近期的最低点是不是 昨天 B
        key_4=0; # 4 阳线实体大于 2 这样排除很多

        count=0
        day1_yinxian_open=0
        day2_yangxian_close=0
        day1_yinxian_low=0
        day2_yangxianshiti=0
        for index,row in data1.iterrows():
            if(index==0 and isYinXian(row)):
                count=count+1
                day1_yinxian_open=row['open']
                day1_yinxian_low=row['low']
            if(index==1 and isYangXian(row)):
                count=count+1
                day2_yangxian_close=row['close']
                day2_yangxianshiti=getShiTiDaXiao(row)
                mairuriqi=row['trade_date']
        if(count==2):
            # 1判断是不是止跌沿线,
            if(day2_yangxian_close >= day1_yinxian_open):
                key_1=1
            # 2是否有 熊市末期
            if(hasXiongShiMoQi(data3)==1):
                key_2=1

            # 3 判断近期的最低点是不是 昨天 B

            befor_mini= getMin_low_fromDataFrame(data2)
            zhisundian= befor_mini
            if(befor_mini > day1_yinxian_low):
                key_3=1

            if(day2_yangxianshiti > 2):
                key_4=1

        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)



        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1):
            info=''
            info = info+'阳线实体='+str(day2_yangxianshiti)
            info = info+ "-----柳暗花明 底部反转 ----"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)

            path = '柳暗花明.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            chengongs.append(chenggong_code)



'''
测试老师的案例
'''
def test_isAn_LiuAnHuaMing2_laoshi():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例 1600200.SH ----20210128--江苏吴中
    df1 = ts.pro_bar(ts_code='600200.SH',adj='qfq', start_date='20200206', end_date='20210202')
    data7_1 = df1.iloc[0:136]  # 前7行
    isAn_LiuAnHuaMing2_model(data7_1,'600200.SH')


    # 案例 2000157.SZ ----20181016--中联重科
    df1 = ts.pro_bar(ts_code='000157.SZ',adj='qfq', start_date='20180206', end_date='20181019')
    data7_1 = df1.iloc[0:136]  # 前7行
    # print df1.iloc[0:7]  # 前7行
    isAn_LiuAnHuaMing2_model(data7_1,'000157.SZ')

    # 案例 3太龙药业600222 失败案例 原因是,最低点有 2 个,不过我的程序是跑不出来这种失败案例的.

    df1 = ts.pro_bar(ts_code='600222.SH',adj='qfq', start_date='20200206', end_date='20201229')
    data7_1 = df1.iloc[0:136]  # 前7行
    isAn_LiuAnHuaMing2_model(data7_1,'600222.SH')

'''
测试自己的案例
'''
def test_isAn_LiuAnHuaMing2_ziji():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)

    #自己的 案例 -----柳暗花明 底部反转 ----000710.SZ ----20210820--贝瑞基因
    df1 = ts.pro_bar(ts_code='000710.SZ',adj='qfq', start_date='20180206', end_date='20210820')
    data7_1 = df1.iloc[0:136]  # 前7行
    # print df1.iloc[0:7]  # 前7行
    isAn_LiuAnHuaMing2_model(data7_1,'000710.SZ')

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


        data7_4 = df.iloc[22:168]  # 前10个交易日
        data7_4 = df.iloc[22:22+136+22]  # 1个月
        # data7_4 = df.iloc[22:22+136+120]  # 半年
        # data7_4 = df.iloc[22:22+136+250]  # 1年
        len_1=len(data7_4)

        for i in range(0, len_1 - 136 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_LiuAnHuaMing2_model(data7_4[i:i + 136], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    # jisuan_all_shouyilv(chengongs, modelname, 1.15)


if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # test_isAn_LiuAnHuaMing2_laoshi()
    # get_all_LiuAnHuaMing2(localpath1)
    test_Befor_data()
    # jisuan_all_shouyilv(chengongs, modelname, 1.03)

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"