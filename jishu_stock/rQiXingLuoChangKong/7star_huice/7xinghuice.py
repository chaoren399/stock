#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from pandas import DataFrame

from jishu_stock.Tool_jishu_stock import writeLog_to_txt
from stock.settings import BASE_DIR
data1 = {
    'ts_code':['Ohio','Ohio','Ohio','Nevada','Nevada','Nevada1','Nevada2'],
    'trade_date':[2000,2001,2002,2001,2002,2001,2002],
    'open':[1.5,1.7,3.6,2.4,2.9,2.4,2.912],
    'high':[1.5,1.7,3.6,2.4,2.9,2.4,2.9],
    'low':[1.5,1.7,3.6,2.4,2.9,2.4,2.9],
    'close':[1.6,1.8,3.5,2.3,2.4,2.3,2.2],
    'pre_close':[1.5,1.7,3.6,2.4,2.9,2.4,2.9],
    'change':[1.5,1.7,3.6,2.4,2.9,2.4,2.9],
    'pct_chg':[-1.5,1.7,3.6,-2.4,-2.9,-2.4,-2.91],
    'vol':[1.5,1.7,3.6,2.4,2.9,2.4,2.9],
    'amount':[1.5,1.7,3.6,2.4,2.9,2.4,2.911]
}

# frame2 = pd.DataFrame(data,index=['one','two','three','four','five'],columns=['year','state','pop','debt'])
# monidata = pd.DataFrame(data1,index=['Ohio','Ohio','Ohio','Nevada','Nevada','Nevada1','Nevada2'])
monidata = pd.DataFrame(data1,index=['Ohio','Ohio','Ohio','Nevada','Nevada','Nevada1','Nevada2'],columns=['ts_code','trade_date','open','high','low','close','pre_close','change','pct_chg','vol','amount'])


liststocks = []


'''

下跌过程中会出现 七星吗？ 很少， 
一般出现在底部，不是底部都会出现， 而是出现了就是底



做一个测试 回测


找到7月份所有的七星， 然后第二天买入， 然后  计算 最高价 只要大于3% 就卖出，  然后时间相差多久。  

计算成功率 

2万元的 3% 是 600元。 
'''




def getallstockdata_is7start_FromLocal(localpath1):
    print "7 星落长空1  start "
    # path = BASE_DIR + '/jishu_stock/rQiXingLuoChangKong/data/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/z_stockdata/xiadiecodes.csv'

    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})

    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        # df =  pd.read_csv(stockdata_path, dtype={'code': str})

        df = pd.read_csv(stockdata_path, index_col=0)
        # print df
        if (df.empty):
            continue
        # data7_1 = df.iloc[16:38]  # 7 月份的
        data7_1 = df.iloc[37:59]  # 6 月份的
        # data7_1 = df.iloc[1:8]  # 前7行
        # 2 单独一个函数 判断是不是符合 7 星落长空模型
        isAn7start_model_pro(data7_1, stock_code)  # 七星 1
        # isAn7start2_model_pro(data7_1, stock_code) # 七星 2


def isAn7start_model_pro(dataframe_df,stockcode):
    len1 = len(dataframe_df)
    # print len1
    for i in range(0,len1-7+1):
        # print "i" + str(i )+ "j"+str(i+3)
        # print dataframe_df[i:i+3]
        # isKanglongyouhui_3Days_data(dataframe_df[0:3])
        isAn7start_model(dataframe_df[i:i+7],stockcode)

'''
#2 单独一个函数 判断是不是符合 7 星落长空模型
'''
def isAn7start_model(dataframe_df,stockcode):
    dataframe_df = dataframe_df.reset_index(drop=True)  # 重新建立索引 ,
    open_price = dataframe_df.ix[0][5]
    close= dataframe_df.ix[0][2]
    riqi = dataframe_df.ix[0][1]
    # print open
    # print close
    if(len(dataframe_df)==7):
        pct_chg_7 = dataframe_df.ix[0][5] -dataframe_df.ix[0][2]  # 涨跌幅
        if (pct_chg_7 > 0): #阳
            #3-2-1-1 最后一天是阴线
            pct_chg_6 = dataframe_df.ix[1][5] -dataframe_df.ix[1][2] # 收盘-开盘
            if(pct_chg_6< 0):#阴
                #3-2-1-1  倒数第 2 天 是阳线
                pct_chg_5 = dataframe_df.ix[2][5]-dataframe_df.ix[2][2]  # 收盘-开盘
                if(pct_chg_5>0):#阳
                    pct_chg_4 = dataframe_df.ix[3][5] -dataframe_df.ix[3][2] # 收盘-开盘

                    if(pct_chg_4 > 0):#阳
                        pct_chg_3 = dataframe_df.ix[4][5] -dataframe_df.ix[4][2] # 收盘-开盘
                        if(pct_chg_3<0):#阴
                            pct_chg_2 = dataframe_df.ix[5][5] -dataframe_df.ix[5][2] # 收盘-开盘
                            if(pct_chg_2<0):#阴
                                pct_chg_1 = dataframe_df.ix[6][5] -dataframe_df.ix[6][2] # 收盘-开盘
                                if(pct_chg_1 < 0):#阴
                                    #符合 rQiXingLuoChangKong
                                    info=  stockcode+"--------------------回测符合 七星落长空 3-2-1-1----------------"+str(riqi)
                                    print info
                                    info1= stockcode+','+str(riqi)
                                    writeLog_to_txt(info1)
                                    return 1
    return 0





def isAn7start2_model_pro(dataframe_df,stockcode):
    len1 = len(dataframe_df)
    # print len1
    for i in range(0,len1-8+1):
        # print "i" + str(i )+ "j"+str(i+3)
        # print dataframe_df[i:i+3]
        # isKanglongyouhui_3Days_data(dataframe_df[0:3])
        isAn7start2_model(dataframe_df[i:i+8],stockcode)
'''
#2 单独一个函数 判断是不是符合 7 星落长空2模型
'''
def isAn7start2_model(dataframe_df,stockcode):
    dataframe_df = dataframe_df.reset_index(drop=True)  # 重新建立索引 ,
    open_price = dataframe_df.ix[0]['open']
    close= dataframe_df.ix[0]['close']
    riqi = dataframe_df.ix[0]['trade_date']
    # print open
    # print close
    if(len(dataframe_df)==8):

        pct_chg_8 = dataframe_df.ix[7][5] -dataframe_df.ix[7][2]  # 涨跌幅  阴
        if(pct_chg_8 <0 ): # 3 阴 1 阳  2 阴 1 阳 1 阳 , 时间理论 3 阴
            pct_chg_7 = dataframe_df.ix[6][5] -dataframe_df.ix[6][2]  # 涨跌幅
            if (pct_chg_7 < 0): #3 阴 1 阳  2 阴 1 阳 1 阳 , 时间理论 3 阴

                pct_chg_6 = dataframe_df.ix[5][5] -dataframe_df.ix[5][2] # 收盘-开盘
                if(pct_chg_6< 0):#3 阴 1 阳  2 阴 1 阳 1 阳 , 时间理论 3 阴

                    pct_chg_5 = dataframe_df.ix[4][5]-dataframe_df.ix[4][2]  # 收盘-开盘
                    if(pct_chg_5>0):# 1 阳  2 阴 1 阳 1 阳 , 时间理论 1 阳
                        pct_chg_4 = dataframe_df.ix[3][5] -dataframe_df.ix[3][2] # 收盘-开盘

                        if(pct_chg_4 < 0):# 2 阴 1 阳 1 阳 , 时间理论 2 阴
                            pct_chg_3 = dataframe_df.ix[2][5] -dataframe_df.ix[2][2] # 收盘-开盘
                            if(pct_chg_3<0):#2 阴 1 阳 1 阳 , 时间理论 2 阴
                                pct_chg_2 = dataframe_df.ix[1][5] -dataframe_df.ix[1][2] # 收盘-开盘
                                if(pct_chg_2>0):#1 阳 1 阳 , 时间理论 1 阳
                                    pct_chg_1 = dataframe_df.ix[0][5] -dataframe_df.ix[0][2] # 收盘-开盘
                                    if(pct_chg_1>0):#1 阳 , 时间理论 1 阳
                                    #符合 rQiXingLuoChangKong
                                        info = stockcode+"--------------------回测符合 七星落长空2----3-1-2-1-1 第 9 天买入------------"+str(riqi)
                                        print info
                                        info1 = stockcode+','+str(riqi)
                                        writeLog_to_txt(info1)
                                        return 1

    return 0

if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()
    # data_show_050002_wucelue() #无策略
    # anstock_isAn7start_model("000002")
    # getallstockdata_is7start(start_date='20210701', end_date='2021726')
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    getallstockdata_is7start_FromLocal(localpath1=localpath1)

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds

