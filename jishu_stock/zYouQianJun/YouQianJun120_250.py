#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1
from jishu_stock.zYouQianJun.get_120_250_data import getStockCode_to_SHSZ
from stock.settings import BASE_DIR

''''
有钱君-120-250 均线交易法
https://www.yuque.com/chaoren399/eozlgk/ke82hq


'''

def get_all_120_250():
    info1=  '--有钱君-120-250 均线交易法 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/zYouQianJun/150stock.csv'  # 150个的数据
    data_150stock = pd.read_csv(path, dtype='object')

    for index,row in data_150stock.iterrows():
        stock_code_1= str(row[0])

        #1 得到股票的全称代码
        stock_code = getStockCode_to_SHSZ(stock_code_1)
        if(stock_code ==0):
            print '数据为空'+stock_code_1
        else:

            #2 开始chuli 数据

            stockdata_path = BASE_DIR + '/jishu_stock/zYouQianJun/150data/' + stock_code + '_150' + ".csv"
            df = pd.read_csv(stockdata_path, index_col=0)
            if (df is None or df.empty):
                print '--df.empty--' + str(stock_code)
                return 0
            else:

                df = df[['ts_code', 'trade_date', 'close', 'open', 'ma120', 'ma250']]
                df['close_ma120'] = df['close'] - df['ma120']
                data7_1 = df.iloc[0:12]  # 前7行
                is_150_250_jincha_mode(data7_1,stock_code)




'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def is_150_250_jincha_mode(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data > 0):
        # data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        # data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data

        # 设置两个 key
        key_1=0; # 右侧 K线 收盘价 - 120 日 的值大于零
        key_2=0; # 左侧 K 线 收盘价 -120 日 的值 小于零

        riqi=data.ix[0]['trade_date']
        close_ma120=[]
        for index,row in data.iterrows():
            close_ma120.append(row['close_ma120'])

        if(close_ma120[0] >0):
            key_1=1
        if(close_ma120[len_data-1] <0):
            key_2=1

        # print1(key_1)
        # print1(key_2)

        if(key_1==1 and  key_2 ==1):
            info = "-----有钱君-120-250 均线交易法 成功了 ----" + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)




def test_is_150_250_jincha_mode():

    start_date = '20150101'
    end_date = '20210907'

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    # stock_code='000038.SZ'
    stock_code='603259.SH' # 药明康德
    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # 打印最新的数据
    df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=end_date, ma=[120, 250])
    df = df.dropna(how='any', axis=0)  # 删除 列数据为空的 的行


    df = df[['ts_code', 'trade_date', 'close', 'open', 'ma120', 'ma250']]
    df['close_ma120'] = df['close'] - df['ma120']
    data7_1 = df.iloc[0:4]  # 前7行

    print data7_1
    is_150_250_jincha_mode(data7_1, stock_code)


if __name__ == '__main__':
    get_all_120_250()
    # test_is_150_250_jincha_mode()