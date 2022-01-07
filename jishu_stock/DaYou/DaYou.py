#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYangXian, is_big_to_small, \
    is_small_to_big, isYinXian, writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from jishu_stock.z_tool.getMin_Max import getMin_fromDataFrame
from jishu_stock.z_tool.is5_13_34_ShangZhang import is5_13_34_XiangShang, is5_10_20_XiangShang_dayou
from stock.settings import BASE_DIR

import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
大有  上涨初期洗盘模型
这模型是中继模型，缓慢上涨到急速拉升这样一个节奏转换的点。
https://www.yuque.com/chaoren399/eozlgk/exwpcp

● 四连阳（没有至少，多一天少一天都不行）
群里交流后 一定是 4 个阳, 之前不能有 5 阳,也就是 需要 7 天的数据, 第一天的必须阴, 然后 4 个阳

'''
chengongs=[]
modelname='大有'
def get_all_DaYou(localpath1):
    info1=  '--大有  上涨初期洗盘模型 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:7]  # 前7行
        # data6_1 = df.iloc[1:8]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_DaYou_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_DaYou_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 7):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,


        data1 = data[len_data-6:len_data]  # 用来判断第一天是不是收阳
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[5]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0

        data2 = data[len_data-6-1:len_data-6]  # 阳线之前的数据
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        data3 = data[len_data-6-1:len_data]  # 阳线之前的数据
        data3 = data3.reset_index(drop=True)  # 重新建立索引 ,

        # print1( data1)


        # 设置两个 key
        key_1=0; # 是不是满足  4 个阳 1 个阴 1 个阳
        key_2=1; #第6天阳线的收盘价高过前5天所有K线的实体，第6天的阳线可以是涨停板也可以不是，
                 # 不是更好，不然上涨动能就被提前消耗，后续爆发将减弱。

        key_3=0; # 后来发现,4 连阳之前必须是阴线的.

        key_4=0; #阳线阴线 实体不能太大, 小于 3.5

        key_5_1=0; #5日均线的方向是否向上
        key_5_2=0; #10日均线的方向是否向上
        key_5_3=0; #34日均线的方向是否向上

        count=0


        yinxian_shiti=0
        yangxian_shiti1=0
        yangxian_shiti2=0
        yangxian_shiti3=0
        yangxian_shiti4=0
        yangxian_shiti5=0
        for index,row in data1.iterrows():
            if(index==0 and isYangXian(row)==1):#阳线 第 1天
                count=count+1
                yangxian_shiti1 = getShiTiDaXiao(row)
            if(index==1 and isYangXian(row)==1):#阳线 第 2天
                count=count+1
                yangxian_shiti2 = getShiTiDaXiao(row)
            if(index==2 and isYangXian(row)==1):#阳线 第 3天
                count=count+1
                yangxian_shiti3 = getShiTiDaXiao(row)
            if(index==3 and isYangXian(row)==1):#阳线 第 4天
                count=count+1
                yangxian_shiti4 = getShiTiDaXiao(row)
            if(index==4 and isYinXian(row)==1): # 阴线
                count=count+1
                yinxian_shiti=getShiTiDaXiao(row)
            if(index==5 and isYangXian(row)==1): #阳线 第 6 天
                count=count+1
                yangxian_shiti5=getShiTiDaXiao(row)
                mairuriqi=row['trade_date']

        if(count==6):
            key_1=1
        if(key_1==1):
            day6_close = data1.ix[5]['close']
            for index, row in data1.iterrows():
                if(index <5 and row['close'] >  day6_close  ):
                    key_2=0
                if(index <5 and row['open'] > day6_close  ):
                    key_2=0

        for index,row in data2.iterrows(): #4 连阳之前必须是阴线的.
            if(index==0 and isYinXian(row)==1):
                key_3=1

        if (key_1 == 1 and key_2 == 1 and key_3 == 1):
            if (float(yangxian_shiti1) < 3.5 and float(yangxian_shiti2) < 3.5
                    and float(yangxian_shiti3) < 3.5 and float(yangxian_shiti4) < 3.5
                    and float(yangxian_shiti5) < 3.5 and abs(float(yangxian_shiti4)) < 3.5):
                key_4=1

        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1):

        zhisundian = getMin_fromDataFrame(data1)['low']

        if(key_1==1 and  key_2 ==1 and key_3==1 ):

            count3=is5_13_34_XiangShang(data3,0)
            info=''
            # if(count3==3):
            if(is5_10_20_XiangShang_dayou(data1, 0)==1):
            # if(1):

                info=info+'5-13-34 有 '+str(count3)+'个上升-'

                if( key_4==1):
                    info=info+'实体满足小于3.5'
                else:
                    info=info+'-----------'
                # info=info+'-阳=' + str(yangxian_shiti1)
                # info=info+'-' + str(yangxian_shiti2)
                # info=info+'-' + str(yangxian_shiti3)
                # info=info+'-' + str(yangxian_shiti4)
                # info = info+'-' + str(yangxian_shiti5) + ',' +'阴线=' + str(yinxian_shiti)

                info = info+"-----大有,上涨初期,洗盘模型,下跌后横盘半年以上 ---- " + str(riqi)
                # print info
                writeLog_to_txt(info, stockcode)

                path = '大有.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)

                chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
                chengongs.append(chenggong_code)



'''
测试老师的案例
'''
def test_isAn_DaYou_laoshi():

    import pandas as pd
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)


    # 案例 1
    df1 = ts.pro_bar(ts_code='000070.SZ',adj='qfq', start_date='20210206', end_date='20210610',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:7]  # 前7行
    isAn_DaYou_model(data7_1,'000070.SZ')
    # 案例 2
    df1 = ts.pro_bar(ts_code='600200.SH',adj='qfq', start_date='20200206', end_date='20210331',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:7]  # 前7行
    isAn_DaYou_model(data7_1,'600200.SH')
    # 案例 3
    df1 = ts.pro_bar(ts_code='300007.SZ',adj='qfq', start_date='20210206', end_date='20210531',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:7]  # 前7行
    isAn_DaYou_model(data7_1,'300007.SZ')





'''
测试自己的案例
'''
def test_isAn_DaYou_ziji():


    #自己的 案例 海康威视
    # df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    # data7_1 = df1.iloc[0:7]  # 前7行
    # isAn_DaYou_model(data7_1,'002507.SZ')



    #-----大有  上涨初期洗盘模型  ----002434.SZ ----20210825--万里扬


    # 自己的 案例
    # df1 = ts.pro_bar(ts_code='002727.SZ', adj='qfq', start_date='20210206', end_date='20211011')
    # data7_1 = df1.iloc[0:7]  # 前7行
    #
    # isAn_DaYou_model(data7_1, '002727.SZ')

    # 案例 1
    df1 = ts.pro_bar(ts_code='600741.SH', adj='qfq', start_date='20210206', end_date='20211017',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:7]  # 前7行
    isAn_DaYou_model(data7_1, '600741.SH')



def ceshi_xueyuan_anli():

    df1 = ts.pro_bar(ts_code='603383.SH', adj='qfq', start_date='20210206', end_date='20211021',ma=[5, 13, 34])
    data7_1 = df1.iloc[0:7]  # 前7行
    isAn_DaYou_model(data7_1, '603383.SH')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        data7_4 = df.iloc[22:42]  #  上个月的数据
        data7_4 = df.iloc[22:22+7+22]  #  上个月的数据
        data7_4 = df.iloc[22:22+7+120]  #  半年的数据
        len_1=len(data7_4)

        for i in range(0, len_1 - 7 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_DaYou_model(data7_4[i:i + 7], stock_code)


    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    jisuan_all_shouyilv(chengongs, modelname, 1.30)

if __name__ == '__main__':

    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_DaYou(localpath1)
    # test_isAn_DaYou_laoshi()#测试老师案例
    # test_isAn_DaYou_ziji()
    test_Befor_data()
    # ceshi_xueyuan_anli()

    # jisuan_all_shouyilv(chengongs, modelname, 1.10)

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"