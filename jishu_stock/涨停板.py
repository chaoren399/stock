#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR


'''


 找到 当天的涨停板  


'''



def getallstockdata_isZhangTingBan_fromLocal(localpath1):
    # path = BASE_DIR + '/jishu_stock/bQiXingLuoChangKong/data/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/xiadiecodes.csv'
    # print "ssss"
    # print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        # localpath1 ='/jishu_stock/stockdata/data1/'
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        # df =  pd.read_csv(stockdata_path, dtype={'code': str})
        df = pd.read_csv(stockdata_path, index_col=0)
        # print df
        if (df.empty):
            return
            # 1 得到 第一个 7 交易日数据
            # iloc只能用数字索引，不能用索引名
        # data7_1 = df.iloc[0:1]  # 前10个交易日
        data7_1 = df.iloc[2:3]  # 前10个交易日

        # 2 单独一个函数 判断是不是符合
        isyes = isAn_ZhangtingBan_model(data7_1, stock_code)
        if (isyes == '1'):
            # liststocks.append(stock_code)
            print "几个了---------------------------------------:"

def isAn_ZhangtingBan_model(data,stock_code):

    '''
    60  00 开头的 10%

    30 68 开头的 20%

    '''
    # print  stock_code[0:2]

    data = data.reset_index(drop=True)  # 重新建立索引 ,
    # print data
    qianzhui_code= stock_code[0:2]
    zhangfuMax = 9 # 涨幅 是不是大于 这个
    if(qianzhui_code =='00' or qianzhui_code =='60'):
        zhangfuMax=9.1
    elif(qianzhui_code=="30" or qianzhui_code=='68'):
        zhangfuMax=19
    count =0;


    for index, row in data.iterrows():

        # print index
        pct_chg = row['pct_chg']
        riqi= row['trade_date']

        if(pct_chg > zhangfuMax):  # 涨停板
            print stock_code + "  " + str(pct_chg) + "--------- 涨停板  ---------"+str(riqi)

            return 1;
        count = count + 1

    return 0;

if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # getallstockdata_isShenLongBaiWei('20210701', '20210805')
    # anstock_isShenLongBaiWei_model('000539.SZ','20210701', '20210805')
    localpath1 = '/jishu_stock/stockdata/data1/'
    getallstockdata_isZhangTingBan_fromLocal(localpath1)

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds