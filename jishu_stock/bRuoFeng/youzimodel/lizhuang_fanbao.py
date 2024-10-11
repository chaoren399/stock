#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.StockCode_Tool import getSockCode_from_SZSH601899
from jishu_stock.z_tool.email import webhook
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

立桩反包

https://www.yuque.com/chaoren399/zxadsn/bvq80d3ccgho84zq


lizhuang_fanbao

'''
chengongs=[]
modelname='lizhuang_fanbao'
#BASE_DIR + '/jishu_stock/z_stockdata/模型编码.csv'

def get_all_lizhuang_fanbao(localpath1):
    info1 = '--立桩反包  start--'
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:4]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_lizhuang_fanbao_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_lizhuang_fanbao_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-3:len_data]   # huoqu suo xuyao de shuju1
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0  # 第一天买入， 第2天卖出
        zhisundian = 0
        # print1(data1)



        # 设置两个 key
        key_1=0; # 第1天 涨停

        key_2=0; # 第2天 大面
        key_3=0 ; #第3天 阳线







        for index,row in data1.iterrows():


            if(index==0 and isZhangTingBan(row)==1):
                key_1=1

            if(index==1 and isYinXian(row)==1):
                key_2=1
            if(index==2 and isYangXian(row)==1):
                key_3=1
                mairuriqi = row['trade_date']


        if (0):
            print key_1
            print key_2
            print key_3


        if(key_1==1 & key_2==1 and key_3==1 ):
        # if(key_1==1 ):
            info = ''

            info = info + "lizhuang_fanbao--"  + str(mairuriqi)
            # print len(data)
            # print info

            writeLog_to_txt(info, stockcode)

            path = modelname+'.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
            # print1(day2_shizixing_low)
            chengongs.append(chenggong_code)




'''
测试老师的案例
'''
def test_isAn_lizhuang_fanbao_model_laoshi():
    # 案例 1 捷荣技术**002855.SZ
    st_code='002855.SZ'
    df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20231221')

    data7_1 = df1.iloc[0:100]  # 前7行
    # print data7_1
    # isAn_lizhuang_fanbao_model(data7_1,st_code)

    # 案例 2 YING FEI TUO
    st_code='002528.SZ'
    df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20221222')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_lizhuang_fanbao_model(data7_1,st_code)

    # 案例 3 文一科技**600520.SH
    st_code='600520.SH'
    df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20231106')
    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    isAn_lizhuang_fanbao_model(data7_1,st_code)


if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/z_stockdata/data1/'

    # test_isAn_lizhuang_fanbao_model_laoshi()
    get_all_lizhuang_fanbao(localpath1)
    # get_all_lizhuang_fanbao_from_Qiang_QuShi(localpath1)



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"