#!/usr/bin/python
# -*- coding: utf8 -*-
import pandas as pd
import tushare as ts

from stock.settings import BASE_DIR



'''
上缺口
'''
def getallstockdata_isQuekou_fromLocal(start_date,end_date):

    path = BASE_DIR + '/jishu_stock/bQiXingLuoChangKong/data/stockcodelist_No_ST.csv'


    print path

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code= row['ts_code']
        # stock_code= '000539.SZ'
        name = row['name']
        if ('ST' not in name):

            stockdata_path = BASE_DIR + '/jishu_stock/stockdata/data2/'+ stock_code + ".csv"
            # df =  pd.read_csv(stockdata_path, dtype={'code': str})
            df =  pd.read_csv(stockdata_path,index_col=0)
            # print df
            if (df.empty):
                return
                # 1 得到 第一个 7 交易日数据
                # iloc只能用数字索引，不能用索引名
            data7_1 = df.iloc[0:10]  # 前7行
            # print data7_1
            # 2 单独一个函数 判断是不是符合 上缺口
            isyes = isAnQuekou_model(data7_1, stock_code)
            if (isyes == '1'):
                # liststocks.append(stock_code)
                print "几个了---------------------------------------:"






'''
缺口 网络访问 数据,  已经不使用了
'''
def anstock_isAnQueKou_model(stock_code,start_date,end_date):

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    pro = ts.pro_api()
    # stock_code='600887.SH'
    # print 'stockcode'+stock_code
    # df = pro.daily(ts_code='000002.SZ', start_date='20210701', end_date='2021726')
    try:
        df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
        # df = pro.daily(ts_code=stock_code, start_date='20210701', end_date='20210802')
        if(df.empty):
            return
        # 1 得到 第一个 7 交易日数据
        # iloc只能用数字索引，不能用索引名
        data7_1 = df.iloc[0:10]  # 前7行
        # print data7_1
        # 2 单独一个函数 判断是不是符合 7 星落长空模型
        isyes = isAnQuekou_model(data7_1, stock_code)
        if (isyes == '1'):
            # liststocks.append(stock_code)
            print "几个了---------------------------------------:"

    except Exception:
        # print "Exception"
        print Exception.__name__



def isAnQuekou_model(dataframe_df,stockcode):
    # print dataframe_df[1:4]
    # open = dataframe_df.ix[0][5]
    # close = dataframe_df.ix[0][2]
    # 对数据处理,  5 日内填补 缺口, 所以要 从第 5 天开始 处理 4 天的吧

    dataframe_df = dataframe_df.iloc[5:10]  # 前7行
    # print "dd "
    # print dataframe_df

    len1 = len(dataframe_df)
    # print len1
    for i in range(0,len1-2+1):
        # print "i" + str(i )+ "j"+str(i+3)
        # print dataframe_df[i:i+3]
        # isKanglongyouhui_3Days_data(dataframe_df[0:3])
        isQueKou_2Days_data(dataframe_df[i:i+2],stockcode)
        # isQueKou_2Days_data(dataframe_df[1:3],stockcode)
        # isKanglongyouhui_3Days_data(dataframe_df[3:6]) # 真是的

''''
2天的数据是不是满足 上缺口

第一天的最高价 小于 第二天的最低价
'''
def  isQueKou_2Days_data(data2days,stockcode):
    data2days = data2days.reset_index(drop=True)  # 重新建立索引 ,
    # print data2days

    # print "122222"
    # print  data3days.ix[0][2]

    if len(data2days) > 0:
        day1High= data2days.ix[1][3] #第一天的最高价
        day2low = data2days.ix[0][4] #第二天的最低价

        day2riqi = data2days.ix[0][1]
        # print day2riqi

        quekou = day2low - day1High

        if(quekou > 1):
            print stockcode + "  " + "--------- 上缺口---------"+str(day2riqi)
            print day1High
            print day2low





if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()


    # anstock_isAnQueKou_model('000539.SZ','20210701', '20210805')
    getallstockdata_isQuekou_fromLocal('20210701', '20210805')  #本地获取数据

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds