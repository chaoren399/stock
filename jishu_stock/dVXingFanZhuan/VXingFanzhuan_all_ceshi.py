#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR


'''
找到涨停板

1. 判断当天是不是 涨停板
2. 根据条件 , 是不是近 3 天 最低值附近出现的涨停盘, 急速下跌
'''

def getallstockdata_isV_fromLocal(localpath1):
    print  'V 型 反转 start'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    # path = BASE_DIR + '/jishu_stock/stockdata/xiadiecodes.csv'
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
            continue
            # 1 得到 第一个 7 交易日数据
            # iloc只能用数字索引，不能用索引名
        data7_1 = df.iloc[0:1]  # 是不是 涨停盘
        # data7_1 = df.iloc[3:4]  # 是不是 涨停盘
        # data7_1 = data7_1.reset_index(drop=True)  # 重新建立索引 ,
        # print data7_1
        # 2 单独一个函数 判断是不是符合 V型反转
        isyes = isAnV_model(data7_1, stock_code)




def isAnV_model(data,stock_code):

    '''
    60  00 开头的 10%

    30 68 开头的 20%

    '''
    # print  stock_code[0:2]

    # data = data.reset_index(drop=True)  # 重新建立索引 ,
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
        # print row['trade_date']
        # print row['pct_chg']

        if(pct_chg > zhangfuMax):  # 涨停板
            riqi  = str(row['trade_date'])
            # print stock_code + "  " + str(pct_chg) + "--------- 涨停板---------" +str(riqi)
            # 得到涨停板后 获取 这只股票之前的 20 天数据
            # 计算最低价, 如果最低价 的日期 与 涨停板的日期 相减 < 3 那么 ,就可以看看了.
            isXiaDieZhangting(stock_code=stock_code, date=riqi)
            return 1;
        count = count + 1
    return 0;
'''
 # 得到涨停板后 获取 这只股票之前的 20 天数据
# 计算最低价, 如果最低价 的日期 与 涨停板的日期 相减 < 3 那么 ,就可以看看了.
'''
def isXiaDieZhangting(stock_code,date):

    if(len(stock_code)==0 ):
        print  " stock_code is  null"
        return 1
    if(len(date) == 0):
        print " date is null"
    # print "laile "
    cur_day = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    # cur_day = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    # the_date = datetime.datetime(y, m, d)
    result_date = cur_day + datetime.timedelta(days=-30)
    # result_date = result_date.strftime('%Y-%m-%d')
    result_date = result_date.strftime('%Y%m%d')
    pro = ts.pro_api()
    df = pro.daily(ts_code=stock_code, start_date=result_date, end_date=date)
    # df.to_csv("V.csv")
    # print df
    # 计算最小值
    min=0;
    date1=date
    for index, row in df.iterrows():
        # 获取 每天的最低值
        if (index==0):
            min = row['low']
            # print '------sss'+ str(row['low'])
        amin = row['low']
        if( amin < min):
            min = amin
            date1=row['trade_date']
    # print "最小值" + str(min)+ "rq"+ str(date1)
    # 循环结束, 得到最小值所在的日期 比较 日期大小
    cur_day = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    # print cur_day
    min_day = datetime.datetime(int(date1[0:4]), int(date1[4:6]), int(date1[6:8]))
    # print min_day

    # print((cur_day-min_day).days)  # 1
    if ((cur_day-min_day).days < 6):
        info =  stock_code + "  " + "--------- V型反转---------" + str(date)
        print info
        path = BASE_DIR + '/jishu_stock/JieGuo/' + datetime.datetime.now().strftime(
            '%Y-%m-%d') + '.txt'
        with open(path, "a") as f:
            f.write(info + '' + "\n")

    #     print("ok1")



if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # getallstockdata_isShenLongBaiWei('20210701', '20210805')
    # anstock_isShenLongBaiWei_model('000539.SZ','20210701', '20210805')
    localpath1 = '/jishu_stock/stockdata/data1/'
    getallstockdata_isV_fromLocal(localpath1)
    # getDemoData()    # 实战单只 股票的是否满足 V 型反转
    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds