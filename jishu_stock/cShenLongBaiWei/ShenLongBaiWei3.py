#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR


'''
神龙摆尾 3
'''


def getallstockdata_isShenLongBaiWei3_fromLocal(localpath1):
    print "神龙摆尾3   start "

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        name = row['name']
        if ('ST' not in name):

            stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
            # df =  pd.read_csv(stockdata_path, dtype={'code': str})
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                return
                # 1 得到 第一个 7 交易日数据
                # iloc只能用数字索引，不能用索引名
            data7_1 = df.iloc[0:3]  # 前10个交易日
            # data7_1 = data7_1.reset_index(drop=True)  # 重新建立索引 ,
            # print data7_1
            # 2 单独一个函数 判断是不是符合  神龙摆尾
            isyes = isAnShenLongBaiwei_model(data7_1, stock_code)
            if (isyes == '1'):
                # liststocks.append(stock_code)
                print "几个了---------------------------------------:"

def isAnShenLongBaiwei_model(dataframe_df,stock_code):

    '''
    60  00 开头的 10%

    30 68 开头的 20%

    '''
    # print  stock_code[0:2]

    dataframe_df = dataframe_df.reset_index(drop=True)  # 重新建立索引 ,
    if ( not (len(dataframe_df) == 3)):
        return

    # print dataframe_df
    qianzhui_code= stock_code[0:2]
    zhangfuMax = 9 # 涨幅 是不是大于 这个
    if(qianzhui_code =='00' or qianzhui_code =='60'):
        zhangfuMax=9.1
    elif(qianzhui_code=="30" or qianzhui_code=='68'):
        zhangfuMax=29
    count =0;


    pct_chg_day1 = dataframe_df.ix[2][8]

    riqiday1 = dataframe_df.ix[2][1]
    # print open
    # print close

    if (pct_chg_day1 > zhangfuMax): # 1. 第一个涨停板
        pct_chg_day2 = dataframe_df.ix[1][8]
        open_day2= dataframe_df.ix[1][2]
        close_day2=dataframe_df.ix[1][5]
        if(pct_chg_day2 > 5 and open_day2 < close_day2) : #2 ,第二日阳线 放量, 且 振幅 5% 以上
            pct_chg_day3 = dataframe_df.ix[0][8]
            if(pct_chg_day3 > 0):
                info =  stock_code + "  " + str(pct_chg_day1) + "--------- 神龙摆尾3---------" + str(riqiday1)
                print  info
                path = BASE_DIR + '/jishu_stock/JieGuo/' + datetime.datetime.now().strftime(
                    '%Y-%m-%d') + '.txt'
                with open(path, "a") as f:
                    f.write(info + '' + "\n")
                return 1



    return 0;

if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # getallstockdata_isShenLongBaiWei('20210701', '20210805')
    # anstock_isShenLongBaiWei_model('000539.SZ','20210701', '20210805')
    localpath1 = '/jishu_stock/stockdata/data2/'
    getallstockdata_isShenLongBaiWei3_fromLocal(localpath1)

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds