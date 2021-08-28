#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
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
得到一只股票判断 是不是满足 7 星落长空2的标准 

3-1-2-1-1 第 9 天买入
3 阴 1 阳  2 阴 1 阳 1 阳 , 时间理论
'''




def getallstockdata_is7start2_FromLocal(localpath1):
    print "7 星落长空2   start  3-1-2-1-1 第 9 天买入 "
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        if(1):
            stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
            # df =  pd.read_csv(stockdata_path, dtype={'code': str})
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                return
            # data7_1 = df.iloc[1:9]  # 前8行
            data7_1 = df.iloc[0:8]  # 前8行
            data7_1 = data7_1.reset_index(drop=True)  # 重新建立索引 ,
            # 2 单独一个函数 判断是不是符合 7 星落长空模型
            # print data7_1

            isyes = isAn7start2_model_pro(data7_1, stock_code)


'''
#2 单独一个函数 判断是不是符合 7 星落长空模型
'''
def isAn7start2_model_pro(dataframe_df,stockcode):
    dataframe_df = dataframe_df.reset_index(drop=True)  # 重新建立索引 ,
    open_price = dataframe_df.ix[0][5]
    close= dataframe_df.ix[0][2]
    riqi = dataframe_df.ix[0][1]
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
                                    #符合 bQiXingLuoChangKong
                                        info = stockcode+"--------------------符合 七星落长空2----3-1-2-1-1 第 9 天买入------------"+str(riqi)
                                        # print info
                                        writeLog_to_txt(info,stockcode)
                                        return 1

    return 0


if __name__ == '__main__':
    import datetime
    starttime = datetime.datetime.now()
    # data_show_050002_wucelue() #无策略
    # anstock_isAn7start_model("000002")
    # getallstockdata_is7start(start_date='20210701', end_date='2021726')
    localpath1 = '/jishu_stock/stockdata/data1/'
    getallstockdata_is7start2_FromLocal(localpath1)

    endtime = datetime.datetime.now()
    print  "总共运行时长:" + str((endtime - starttime).seconds ) +"秒"