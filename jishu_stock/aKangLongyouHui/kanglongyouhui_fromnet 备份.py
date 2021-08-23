#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR

def getallstockdata_isKangLong(start_date,end_date):
    path = BASE_DIR + '/jishu_stock/bQiXingLuoChangKong/data/stockcodelist_No_ST.csv'
    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        name = row['name']
        if ('ST' not in name):
            anstock_isAnKanglongyouhui_model(row['ts_code'],start_date,end_date)
            count=count+1
        # print "第"+str(count)+"个"
        # print code

'''
亢龙有悔
'''
def anstock_isAnKanglongyouhui_model(stock_code,start_date,end_date):

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
        data7_1 = df.iloc[0:7]  # 前7行
        # print data7_1
        # 2 单独一个函数 判断是不是符合 7 星落长空模型
        isyes = isAnKanglongyouhui_model_pro(data7_1, stock_code)
        if (isyes == '1'):
            # liststocks.append(stock_code)
            print "几个了---------------------------------------:"

    except Exception:
        # print "Exception"
        ss = ""
        # print " "


'''

'''
def getallstockdata_isKangLong_fromLocal(start_date,end_date):
    path = BASE_DIR + '/jishu_stock/bQiXingLuoChangKong/data/stockcodelist_No_ST.csv'
    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        name = row['name']
        if ('ST' not in name):
            stockdata_path = BASE_DIR + '/jishu_stock/stockdata/data2/' + stock_code + ".csv"
            # df =  pd.read_csv(stockdata_path, dtype={'code': str})
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                return
                # 1 得到 第一个 7 交易日数据
                # iloc只能用数字索引，不能用索引名
            data7_1 = df.iloc[0:10]  # 前7行
            # print data7_1
            # 2 单独一个函数 判断是不是符合 上缺口
            isyes = isAnKanglongyouhui_model_pro(data7_1, stock_code)
            if (isyes == '1'):
                # liststocks.append(stock_code)
                print "几个了---------------------------------------:"

def isAnKanglongyouhui_model_pro(dataframe_df,stockcode):
    # print dataframe_df[1:4]
    # open = dataframe_df.ix[0][5]
    # close = dataframe_df.ix[0][2]

    len1 = len(dataframe_df)
    # print len1
    for i in range(0,len1-3+1):
        # print "i" + str(i )+ "j"+str(i+3)
        # print dataframe_df[i:i+3]
        # isKanglongyouhui_3Days_data(dataframe_df[0:3])
        isKanglongyouhui_3Days_data(dataframe_df[i:i+3],stockcode)
        # isKanglongyouhui_3Days_data(dataframe_df[1:4])
        # isKanglongyouhui_3Days_data(dataframe_df[3:6]) # 真是的






''''
3 天的数据是不是满足 亢龙有悔的模型
'''
def  isKanglongyouhui_3Days_data(data3days,stockcode):
    data3days = data3days.reset_index(drop=True)  # 重新建立索引 ,
    # print data3days
    # print "122222"
    # print  data3days.ix[0][2]

    if len(data3days) > 0:

        #第一天 阴线
        day1open = data3days.ix[2][2]
        day1close = data3days.ix[2][5]
        day1riqi = data3days.ix[2][1]
        day1pct_chg = data3days.ix[2][8]
        day1low= data3days.ix[2][4]
        # print day1riqi
        # print day1close
        # print day1open
        day1yinxian= day1close -  day1open


        # print day1yinxian

        # 第 2 天阴线

        day2open = data3days.ix[1][2]
        day2close = data3days.ix[1][5]
        day2pct_chg = data3days.ix[1][8]
        day2yinxian = day2close - day2open
        # print day2yinxian

        #第 3天 阳线

        day3open = data3days.ix[0][2]
        day3close = data3days.ix[0][5]
        day3pct_chg = data3days.ix[0][8]

        # print day3pct_chg
        day3yinxian = day3close - day3open
        # print day3yinxian


        if(day1yinxian < 0 and day2yinxian <0 and day3yinxian>0):
            if(day2pct_chg < day1pct_chg  ): # 第一天小阴线  通过涨幅判断 是不是大阴线 比小阴线大
                if(day3open < day2close and day3close  < day2open): # 阳线的开盘 低于 第 2 天阴线的收盘价 &  阳线 收盘价 小于第 2 天阴线的开盘
                    if(day1low > day2open ): # 跳空 第一天小阴线的 收盘价 必须要高于 第 2 天大阴线的开盘价
                        if(day3pct_chg > 2): #阳线越小好


                            # 实体部分对比 开盘价 - 收盘价 的差值
                            day1shiti= day1open -day1close
                            day2shiti = day2open - day2close
                            day3shiti = day3close - day3open
                            if( day2shiti / day1shiti > 1 and day2shiti / day3shiti > 1):

                                print "yinyin yang "+stockcode +"-------------------符合亢龙有悔"
                                print day1low
                                return 1


    return 0;



if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # anstock_isAnKanglongyouhui_model("300020.SZ",'20210701', '20210802')
    getallstockdata_isKangLong('20210701', '20210803')
    # getallstockdata_isKangLong_fromLocal('20210701', '20210803')
    # getallstockdata_isKangLong()

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds

    '''
    追求的 比较符合的 趋势
    '''