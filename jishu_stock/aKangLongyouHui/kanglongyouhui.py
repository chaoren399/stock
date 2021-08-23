#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, isShangZhang_QuShi

from stock.settings import BASE_DIR

'''

亢龙有悔 N字型上涨趋势


亢龙有悔 ,用在个股上 必须 是 上涨 趋势 , 如何 判断上涨趋势呢?

先把最近7 天的 数据拿到 最小值MIN7,  然后对比最近 30 天的数据做对比, 只要 min7  是最大的说明 这是一个上涨趋势
'''
def getallstockdata_isKangLong_fromLocal(localpath1):
    print "亢龙有悔 start "
    # path = BASE_DIR + '/jishu_stock/bQiXingLuoChangKong/data/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # print "ssss"
    # print path
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
            data7_1 = df.iloc[0:3]  # 前7行
            # print data7_1
            # 2 单独一个函数 判断是不是符合 上缺口
            isyes = isAnKanglongyouhui_model_pro(data7_1, stock_code)
            if (isyes == '1'):
                # liststocks.append(stock_code)
                print "几个了---------------------------------------:"

def isAnKanglongyouhui_model_pro(dataframe_df,stockcode):
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

    if len(data3days) ==3 :

        #第一天 阴线
        day1open = data3days.ix[2]['open']
        day1close = data3days.ix[2]['close']
        day1riqi = data3days.ix[2]['trade_date']
        day1pct_chg = data3days.ix[2]['pct_chg']
        day1low= data3days.ix[2]['low']
        day1yinxian= day1close -  day1open

        # 第 2 天阴线

        day2open = data3days.ix[1]['open']
        day2close = data3days.ix[1]['close']
        day2pct_chg = data3days.ix[1]['trade_date']
        day2yinxian = day2close - day2open
        # print day2yinxian

        #第 3天 阳线

        day3open = data3days.ix[0]['open']
        day3close = data3days.ix[0]['close']
        day3pct_chg = data3days.ix[0]['trade_date']

        # print day3pct_chg
        day3yinxian = day3close - day3open
        # print day3yinxian
        riqi = data3days.ix[0][1]


        if(day1yinxian < 0 and day2yinxian <0 and day3yinxian>0):  # 阴 阴 阳
            if (day1yinxian > day2yinxian):  # 第一天小阴线  通过涨幅判断 是不是大阴线 比小阴线大  注意负值
                if (day3open < day2close and day3close < day2open and day3close > day2close):  # 阳线的开盘 低于 第 2 天阴线的收盘价 &  阳线 收盘价 小于第 2 天阴线的开盘
                    if (day1low > day2open):  # 跳空 第一天小阴线的 收盘价 必须要高于 第 2 天大阴线的开盘价
                        if(isShangZhang_QuShi(data3days) ==1 ):
                            # print day1yinxian
                            # print day2yinxian
                         # 上涨趋势,  最近的最小值 大于 近 30 天的最小值
                            info =  "yinyin yang "+stockcode +"-------------------符合亢龙有悔"+str(riqi)
                            print  info
                            writeLog_to_txt(info)
                            return 1


    return 0;



if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # anstock_isAnKanglongyouhui_model("300020.SZ",'20210701', '20210802')
    localpath1 = '/jishu_stock/stockdata/data1/'
    getallstockdata_isKangLong_fromLocal(localpath1)
    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds

    '''
    追求的 比较符合的 趋势
    '''