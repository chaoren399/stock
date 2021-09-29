#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, isYangXian
from stock.settings import BASE_DIR

''''
神龙摆尾 0
https://www.yuque.com/chaoren399/eozlgk/ez5zh7

急速下跌熊市末期
(连续3根或以上阴线伴随着低开和大阴线)
小十字星
第2日阴线创新低
第3夭阳线收盘价高过第2日阴线收盘价h
以亢龙有悔的方法结算和止损

思路 ,找到到前 6 个数据,  然后 3 个是阴线,  第 4 个是十字星,  第 5 个阴线, 第 6 个是阳线
'''

def get_all_isShenLongBaiWei0_fromLoca(localpath1):
    info1=  '--神龙摆尾0  start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:6]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ShenLongBaiwei0_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ShenLongBaiwei0_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data

        # 设置两个 key
        key_1=0; #是不是满足  3 个是阴线,  第 4 个是十字星,  第 5 个阴线, 第 6 个是阳线
        key_2=0;
        riqi =data.ix[0]['trade_date']

        count1=0
        for index,row in data.iterrows():
            if(index==0 and isYangXian(row)==0):
                count1=count1+1
            if(index==1 and isYangXian(row)==0):
                count1=count1+1

            if(index==2 and isYangXian(row)==0): #前 3 个
                count1=count1+1

            if(index==3 ): # 小十字线
                day4_open=row['open']
                day4_close=row['close']
                if(abs(day4_open - day4_close) <=0.05):
                    # print row['trade_date']

                    count1=count1+1

            if(index==4 and isYangXian(row)==0): #第 5 个阴
                count1=count1+1
                # print row

            if(index==5 and isYangXian(row)==1): #第 6 个阳
                count1=count1+1

        if(count1 ==6):
            key_1 =1


        if(key_1==1 ):
            info = "-----神龙摆尾 0 成功了" + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)




def test_isAn_ShenLongBaiwei0_model():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # 打印最新的数据
    df1 = ts.pro_bar(ts_code='000045.SZ ', start_date='20200617', end_date='20210925')

    data7_1 = df1.iloc[0:6]  # 前7行
    # print data7_1
    isAn_ShenLongBaiwei0_model(data7_1,'000045.SZ ')


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_isShenLongBaiWei0_fromLoca(localpath1)
    # test_isAn_ShenLongBaiwei0_model()