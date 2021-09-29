#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode
from stock.settings import BASE_DIR

''''
缺口理论, 凌波微步
https://www.yuque.com/chaoren399/kb/ayfh2g

价格筑底 后  要有几天的横盘, 1-2 周吧, 3 天也可以

1, 找到 6 日的数据 

2 ,第一天 ,第 2 天是 缺口, 且第 2 天是阳线  第 3,4,5,6 天中  最小值 大于 第一天的 最大值


'''

def get_all_LingBoWeiBu(localpath1):
    info1=  '--缺口理论, 凌波微步 start--   '
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[2:8]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_LingBoWeiBu_model(data6_1, stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_LingBoWeiBu_model(data,stockcode):
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
        riqi = data.ix[3]['trade_date']  # 阳线的日期

        # 设置两个 key
        key_1=0;
        key_2=0;


        if(key_1==1 and  key_2 ==1):
            info = "-----缺口理论, 凌波微步  成功了" + ' ----' + stockcode + ' ----' + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)




def test_get_5_13_34_RiJunXian_Pro3():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    # 打印最新的数据
    df1 = ts.pro_bar(ts_code='600050.SZ', start_date='20200617', end_date='20200624')

    data7_1 = df1.iloc[0:6]  # 前7行
    # print data7_1
    isAn_LingBoWeiBu_model(data7_1,'000038.SZ')


if __name__ == '__main__':
    localpath1 = '/jishu_stock/stockdata/data1/'
    # test_get_5_13_34_RiJunXian_Pro3()
    get_all_LingBoWeiBu(localpath1)