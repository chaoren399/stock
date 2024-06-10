#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
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
岛型反转缺口

思路: 找 10 天数据, 有 2 个缺口的可以选出来, 然后人工分析是不是回调的 底部

(1) 找到 下缺口: 今天的最大值 低于 昨天的最小值
(2)找到 上缺口: 今天的最小值 高于昨天的 最大值 


https://www.yuque.com/chaoren399/eozlgk/qolss2

23-（2）岛型反转缺口-案例讲解

DaoXingQueKou
'''
chengongs=[]
modelname='岛型反转缺口'

def get_all_DaoXingQueKou(localpath1):
    info1=  '--岛型反转缺口 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_DaoXingQueKou_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_DaoXingQueKou_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 10):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-10:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        riqi1 = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        len_data1=len(data1)
        # print1(data1)

        # 设置两个 key
        key_1=0;#(1) 找到 下缺口: 今天的最大值 低于 昨天的最小值
        key_2=0;#(2)找到 上缺口: 今天的最小值 高于昨天的 最大值




        for i in range(0, len_data1 - 2 + 1):
            tmpdata=  data1[i:i + 2]
            tmpdata = tmpdata.reset_index(drop=True)  # 重新建立索引 ,
            # print tmpdata

            if(key_1==0):
                day1_low = 0
                day2_high = 0
                for index, row in tmpdata.iterrows():
                    if(index==0):
                        day1_low= row['low']
                    if(index==1):
                        day2_high = row['high']
                        riqi = row['trade_date']

                if(day1_low > day2_high):  ##(1) 找到 下缺口: 今天的最大值 低于 昨天的最小值
                    key_1=1
                    # print1(day1_low)
                    # print1(day2_high)




            if(key_1==1): #(2)找到 上缺口: 今天的最小值 高于昨天的 最大值
                day1_high = 0
                day2_low = 0
                for index, row in tmpdata.iterrows():
                    if(index==0):
                        day1_high=row['high']
                    if(index==1):
                        day2_low=row['low']
                        riqi1 = row['trade_date']

                if(day2_low > day1_high):
                    key_2=1
                    break


        # print1(key_1)
        # print1(key_2)
        if(key_1==1 and  key_2 ==1):
            info = ''

            info = info + "--岛型反转缺口  成功了--"
            info = info + "下缺口:"  + str(riqi) +'--上缺口:'+str(riqi1)
            # print info
            # 统一 info管理 一个函数,每次都要执行, 并且信息 返回后,要添加到 info中,
            # 方便后期修改,这样一改,所有的都可以执行了.
            from jishu_stock.z_tool.InfoTool import manage_info
            manage_info = manage_info(info, stockcode, riqi, '')
            info = info + manage_info

            writeLog_to_txt(info, stockcode)
            path = modelname + '.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            # print1(day2_shizixing_low)
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_DaoXingQueKou_laoshi():
    # 案例 1 老师案例1 : 通宇通讯 002792
    # df1 = ts.pro_bar(ts_code='002792.SZ',adj='qfq', start_date='20170206', end_date='20181203')
    df1 = ts.pro_bar(ts_code='002792.SZ',adj='qfq', start_date='20170206', end_date='20181203')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_DaoXingQueKou_model(data7_1,'002792.SZ')

    # 案例 2 老师案例2: 600734   20190131

    df1 = ts.pro_bar(ts_code='600734.SH',adj='qfq', start_date='20170206', end_date='20190211')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_DaoXingQueKou_model(data7_1,'600734.SH')

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_DaoXingQueKou_ziji():
    #自己的 案例  --岛型反转缺口  成功了--下缺口:20220224--上缺口:20220308--深南电A**000037.SZ
    df1 = ts.pro_bar(ts_code='000037.SZ',adj='qfq', start_date='20210206', end_date='20220308')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_DaoXingQueKou_model(data7_1,'000037.SZ')

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

        n = 5  # 模型需要最低的数据
        # data7_4 = df.iloc[22:22 + n + 5]  # 前1个月个交易日
        data7_4 = df.iloc[22:22 + n + 22]  # 1 个月
        # data7_4 = df.iloc[22:22 + n + 120]  # 半年
        # data7_4 = df.iloc[22:22+n+250]  # 1年

        len_1 = len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_DaoXingQueKou_model(data7_4[i:i + n], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    # jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)


if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_DaoXingQueKou(localpath1)
    # test_isAn_DaoXingQueKou_laoshi()
    # test_isAn_DaoXingQueKou_ziji()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"