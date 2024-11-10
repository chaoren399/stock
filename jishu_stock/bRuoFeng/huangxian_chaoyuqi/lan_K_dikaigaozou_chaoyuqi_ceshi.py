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
from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan, isHuangXian, isZhangTingBan_zzy, isLanK_zzy
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''

蓝线-低开高走-超预期

https://www.yuque.com/chaoren399/zxadsn/fvihngh1odvegr9g

lan_K_chaoyuqi

'''
chengongs=[]
modelname='lan_K_chaoyuqi'
cn_name='蓝线-低开高走-超预期'
#BASE_DIR + '/jishu_stock/z_stockdata/模型编码.csv'


def get_all_lan_K_chaoyuqi(localpath1):
    info1 = '--蓝线-低开高走-超预期 start--'
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:40]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_lan_K_chaoyuqi_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_lan_K_chaoyuqi_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 10):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-2:len_data]   #  要计算 振幅 需要 前一天数据， 所以需要4个
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[1]['trade_date']  # 阳线的日期
        mairuriqi = riqi  # 第一天买入， 第2天卖出

        # print1(data1)

        data2= data[len_data-7:len_data-1]   #  要计算 振幅 需要 前一天数据， 所以需要4个
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,



        # 设置两个 key
        key_1=0; # 第1天 lan K
        key_2=0; # 5天内出现国涨停板

        keyreturn=isLanK_zzy(data1)

        if(keyreturn==2 or keyreturn==4):
            key_1=1



        #2 判断是否5天内出现国涨停板


        # print len(data2)
        len_data2=len(data2)
        count=0
        for i in range(0,len_data2):
            if(i<len_data2-1):
              # print 'i='+str(i) +','+ str(i+1)
              dataK = data2.loc[i:i+1]
              if(isZhangTingBan_zzy(dataK) ==1):
                  count=count +1


        if(count>=1):
            key_2=1



        if (0):
            print key_1
            print key_2



        if(key_1==1 & key_2==1 ):
        # if(key_1==1 ):
            info = ''

            info = info +cn_name +"--"+ str(mairuriqi)
            # print len(data)
            # print info

            writeLog_to_txt(info, stockcode)

            path = modelname+'.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)








'''
测试老师的案例 -测试  蓝K-跌停板
'''
def test_isAn_lan_K_chaoyuqi_model_laoshi_LanK():
    # 案例 1 海立股份**600619.Sh
    st_code='600619.SH'
    # df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20241022')
    # df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20241101')
    # df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20241010')
    # df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20241011')
    df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20240924')


    data7_1 = df1.iloc[0:100]  # 前7行
    # print data7_1
    isAn_lan_K_chaoyuqi_model(data7_1,st_code)

    # 案例 2 上海电气 **601727.SH
    st_code='601727.SH'
    df1 = ts.pro_bar(ts_code=st_code,adj='qfq', start_date='20210206', end_date='20241101')

    data7_1 = df1.iloc[0:30]  # 前7行
    # print data7_1
    # isAn_lan_K_chaoyuqi_model(data7_1,st_code)






if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/z_stockdata/data1/'


    # test_isAn_lan_K_chaoyuqi_model_laoshi_LanK()
    get_all_lan_K_chaoyuqi(localpath1)
    # get_all_lan_K_chaoyuqi_from_Qiang_QuShi(localpath1)



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"