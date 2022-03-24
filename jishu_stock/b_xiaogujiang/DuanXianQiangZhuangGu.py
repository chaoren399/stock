#!/usr/bin/python
# -*- coding: utf8 -*-

from jishu_stock.Tool_jishu_stock import *
from jishu_stock.bChanKe.Tool_LiuTongShiZhi import LTSZ_IS_Small_100YI
from jishu_stock.z_tool.ShiTiDaXiao import *

import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
短线强庄股 DuanXianQiangZhuangGu

用 144 均线, 3 天数据判断,  

程序选出 4 天数据, 第一天在 144 下边, 第 2 天 穿越或者站上 144 , 第 3,4 天不跌破 144

人工审核  成交量在 120 日均量线 之上,  流通额 100 亿以下. 最好是热点


'''
chengongs=[]
modelname='短线强庄股'

def get_all_DuanXianQiangZhuangGu(localpath1):
    info1=  '--短线强庄股 start--   '
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
        isAn_DuanXianQiangZhuangGu_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_DuanXianQiangZhuangGu_model(data,stockcode):
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
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        # 设置两个 key
        key_1=0;  #第一天 k 线 在 144 下边
        key_2=0; # 第 2 天 K 线 穿越144
        key_3=0; #  第 3 天 K 收盘价 144 以上
        key_4=0 ; # 第 4 天 K 收盘在 144 以上

        #成交量
        #前三天成交量大于 120 日均量

        key_5=0; # 第2,3,4  成交量大于 120 日均量
        key_6=0; # 流通市值 小于 100 亿
        day1_vol=0
        day2_vol=0
        day3_vol=0
        day1_vol_v=0
        day2_vol_v=0
        day3_vol_v=0


        for index, row in data1.iterrows():
            day_144=row['ma144']
            if(index==0): #  #第一天 k 线 在 144 下边
                day0_high= row['high']
                day0_open= row['open']
                day0_close= row['close']
                # if(day0_high < day_144):
                if(day0_open < day_144 and day0_close <day_144):
                    key_1=1

                zhisundian=row['low']
            if(index==1):  # 第 2 天 K 线 穿越144
                day1_high= row['high']
                day1_low= row['low']
                day1_vol=row['vol']
                day1_vol_v=row['ma_v_120']
                if(day1_high >= day_144 and day1_low <=  day_144):
                    key_2=1
            if(index==2):#  第 3 天 K 收盘价 144 以上
                day2_close= row['close']
                if(day2_close > day_144):
                    key_3=1
                day2_vol = row['vol']
                day2_vol_v = row['ma_v_120']
            if(index==3): # 第 4 天 K 收盘在 144 以上
                day3_close= row['close']
                if(day3_close > day_144):
                    key_4=1
                day3_vol = row['vol']
                day3_vol_v = row['ma_v_120']
                mairuriqi=row['trade_date']

            # key_5=0; # 第2,3,4  成交量大于 120 日均量

            if(day1_vol > day1_vol_v and day2_vol > day2_vol_v and day3_vol > day3_vol_v):
                key_5=1


        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)

        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1):


            if(1):

                info = ''

                info = info + "--短线强庄股成功了--"  + str(riqi)
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
def test_isAn_DuanXianQiangZhuangGu_laoshi():
    # 案例 1天奈科技
    df1 = ts.pro_bar(ts_code='600804.SH',adj='qfq', start_date='20190206', end_date='20220223', ma=[5, 13, 34, 144, 169,120])
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_DuanXianQiangZhuangGu_model(data7_1,'600804.SH')

    # 案例 2

    # 案例 3

'''
测试自己的案例
'''
def test_isAn_DuanXianQiangZhuangGu_ziji():
    #自己的 案例
    df1 = ts.pro_bar(ts_code='002507.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    data7_1 = df1.iloc[0:6]  # 前7行
    isAn_DuanXianQiangZhuangGu_model(data7_1,'002507.SZ')

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

        n = 5  # 模型需要最低的数据
        # data7_4 = df.iloc[22:22 + n + 5]  # 前1个月个交易日
        data7_4 = df.iloc[22:22 + n + 22]  # 1 个月
        # data7_4 = df.iloc[22:22 + n + 120]  # 半年
        # data7_4 = df.iloc[22:22+n+250]  # 1年

        len_1 = len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_DuanXianQiangZhuangGu_model(data7_4[i:i + n], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
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


    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_DuanXianQiangZhuangGu(localpath1)
    # test_isAn_DuanXianQiangZhuangGu_laoshi()
    # test_Befor_data()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"