#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian, print1, \
    writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.ShiTiDaXiao import getShiTiDaXiao
from stock.settings import BASE_DIR

''''
熊市末期亢龙有悔 个股上的应用: 

https://www.yuque.com/chaoren399/eozlgk/gt5puq



连续 3 天以上阴线 , 跳空低开(不一定是缺口) 

思路:  

1 . 找出 3 个值,判断是不是 2 个阴线 一个阳线
2. 跳空低开的可以 判断一下. 

做 2 个股票, 一个是上证 50 ,一个是 上证指数


'''

def get_all_KangLongYouHui_DaPan():
    info1=  '--亢龙有悔 大盘 趋势 start--   '
    writeLog_to_txt_nocode(info1)
    zhishus=['000016.SH','000001.SH']

    starttime = datetime.datetime.now()
    today = starttime.strftime('%Y%m%d')
    # 上证50指数
    df = ts.pro_bar(ts_code='000016.SH', adj='qfq',asset='I', start_date='20180101', end_date=today)
    data6_1 = df.iloc[0:3]  # 前6行
    isAn_KangLongYouHui_DaPan_model(data6_1, '000016.SH')
    # 上证指数 000001.SH
    df = ts.pro_bar(ts_code='000001.SH', adj='qfq',asset='I', start_date='20180101', end_date=today)
    data6_1 = df.iloc[0:3]  # 前6行
    isAn_KangLongYouHui_DaPan_model(data6_1, '000001.SH')

'''
#2 单独一个函数 判断 4 个数据是不是符合模型
'''
def isAn_KangLongYouHui_DaPan_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data ==3):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data
        # 设置两个 key
        key_1=0; #先判断是不是 2 个阴一个阳
        key_2=0; # 判断 是不是 跳空低开(不一定是缺口)
        key_3=0; # 判断 最后一个阳线是不是  低开高收的阳线

        riqi=data.ix[len_data-1]['trade_date']
        #1 先判断是不是 2 个阴一个阳
        count=0
        for index, row in data.iterrows():
            # print getShiTiDaXiao(row)
            if(index==0 and isYangXian(row)==0):
                count=count+1
            if(index==1 and isYangXian(row)==0):
                count=count+1
            if(index==2 and isYangXian(row)==1):
                count=count+1
        if(count==3):
            key_1=1


        #2 判断 是不是 跳空低开(不一定是缺口)

        #3 判断 最后一个阳线是不是  低开的阳线

        day2_close = data.ix[1]['close']
        day3_open= data.ix[2]['open']
        if( day3_open < day2_close ):
            key_3=1
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        if(key_1==1 and key_3==1 ):
            info=''
            info = info+str(stockcode)
            info = info+"--大盘亢龙有悔成功了--"  + str(riqi)
            # print info
            # writeLog_to_txt(info, stockcode)

            writeLog_to_txt_nocode(info)
            path = '大盘亢龙有悔.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)



def test_isAn_KangLongYouHui_DaPan_ChengGong_anli():
    df = ts.pro_bar(ts_code='000001.SH', adj='qfq',asset='I', start_date='20180101', end_date='20211013')
    data6_1 = df.iloc[0:3]  # 前6行
    isAn_KangLongYouHui_DaPan_model(data6_1, '000016.SH')


'''
测试案例
'''
def test_isAn_KangLongYouHui_DaPan():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    pro = ts.pro_api()
    # df = ts.pro_bar(ts_code='000001.SH', adj='qfq', start_date='20160608', end_date='20160614')
    df = ts.pro_bar(ts_code='000001.SH', asset='I',freq='D',start_date='20160608',end_date='20211003 ')
    data7_1 = df.iloc[0:3]  # 前7行
    # print data7_1
    # isAn_KangLongYouHui_DaPan_model(data7_1,'000001.SZ')

    data7_2 = df.iloc[0:100]  # 前7行
    len1=len(data7_2)
    for i in range(0, len1 - 3 + 1):
        isAn_KangLongYouHui_DaPan_model(data7_2[i:i + 3], '000001.SZ')

if __name__ == '__main__':
    # test_isAn_KangLongYouHui_DaPan()
    # get_all_KangLongYouHui_DaPan()
    test_isAn_KangLongYouHui_DaPan_ChengGong_anli()