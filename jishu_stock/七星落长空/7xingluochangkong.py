#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from pandas import DataFrame

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
获取所有股票的代码 
https://tushare.pro/document/2?doc_id=25
'''

def getallstockdata_is7start():
    path = BASE_DIR + '/jishu_stock/七星落长空/data/stockcodelist.csv'
    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        anstock_isAn7start_model(row['ts_code'])
        count=count+1
        # print "第"+str(count)+"个"
        # print code

'''
得到一只股票判断 是不是满足 7 星落长空的标准 
'''

def anstock_isAn7start_model(stock_code):

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    pro = ts.pro_api()
    # print 'stockcode'+stock_code
    # df = pro.daily(ts_code='000002.SZ', start_date='20210701', end_date='2021726')
    try:
        df = pro.daily(ts_code=stock_code, start_date='20210701', end_date='2021726')
        if(df.empty):
            return
        # 1 得到 第一个 7 交易日数据
        # iloc只能用数字索引，不能用索引名
        data7_1 = df.iloc[0:7]  # 前7行
        # 2 单独一个函数 判断是不是符合 7 星落长空模型
        isyes = isAn7start_model_pro(data7_1, stock_code)
        if (isyes == '1'):
            liststocks.append(stock_code)
            print "几个了---------------------------------------:" + str(len(liststocks))

    except Exception:
        # print "Exception"
        ss = ""
        # print " "





'''
#2 单独一个函数 判断是不是符合 7 星落长空模型
'''
def isAn7start_model_pro(dataframe_df,stockcode):
    open = dataframe_df.ix[0][5]
    close= dataframe_df.ix[0][2]
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
                                if(pct_chg_1<0):#阴
                                    #符合 七星落长空
                                    print stockcode+"--------------------符合 七星落长空----------------"
                                    return 1

    elif(len(dataframe_df)==6):#3-2-1
        pct_chg_6 = dataframe_df.ix[0][5] -dataframe_df.ix[0][2] # 收盘-开盘
        if(pct_chg_6<0):#阴
            pct_chg_5 = dataframe_df.ix[1][5] -dataframe_df.ix[1][2] # 收盘-开盘

            if(pct_chg_5>0):#阳
                pct_chg_4 = dataframe_df.ix[2][5] -dataframe_df.ix[2][2] # 收盘-开盘
                if(pct_chg_4>0):#阳
                    pct_chg_3 = dataframe_df.ix[3][5] -dataframe_df.ix[3][2] # 收盘-开盘
                    if(pct_chg_3<0):#阴
                        pct_chg_2 = dataframe_df.ix[4][5]- dataframe_df.ix[4][2] # 收盘-开盘
                        if(pct_chg_2<0):#阴
                            pct_chg_1 = dataframe_df.ix[5][5] -dataframe_df.ix[5][2] # 收盘-开盘
                            if(pct_chg_1<0):#阴
                                # 符合 6星落长空  观察明天数据
                                print stockcode+"--------------------符合 6星落长空  观察明天数据----------------"
                                return 1

    elif(len(dataframe_df)==5):#3-2-
        pct_chg_5 = dataframe_df.ix[0][5] -dataframe_df.ix[0][2] # 收盘-开盘
        if (pct_chg_5 > 0):  # 阳
            pct_chg_4 = dataframe_df.ix[1][5] -dataframe_df.ix[1][2] # 收盘-开盘
            if (pct_chg_4 > 0):  # 阳
                pct_chg_3 = dataframe_df.ix[2][5] -dataframe_df.ix[2][2]  # 收盘-开盘
                if(pct_chg_3<0): #阴
                    pct_chg_2 = dataframe_df.ix[3][5]-dataframe_df.ix[3][2]  # 收盘-开盘
                if(pct_chg_2<0): #阴

                    pct_chg_1 = dataframe_df.ix[4][5] -dataframe_df.ix[4][2] # 收盘-开盘
                if(pct_chg_1<0): #阴
                    #符合 5星落长空  观察明天后天数据
                    print stockcode+ "--------------------符合 5星落长空  观察明天后天数据----------------"
                    return 1

    return 0

def test1():
    # print monidata[0:5]

    isyes = isAn7start_model_pro(monidata[0:6])
    print isyes

if __name__ == '__main__':
    # data_show_050002_wucelue() #无策略
    # anstock_isAn7start_model("000002")
    getallstockdata_is7start()
    # anstock_isAn7start_model('002899.SZ')
    # anstock_isAn7start_model(monidata)
    # test1()