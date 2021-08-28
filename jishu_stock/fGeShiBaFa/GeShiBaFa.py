#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import pandas as pd

from jishu_stock.fGeShiBaFa.Get_Week_K_data import getAllWeekKdata
from stock.settings import BASE_DIR

'''
第一步 : 用  Get_Week_K_data.py 来 得到 周K 线
第二步:   计算 10 周K 线 和 60 周K 线, 葛式八法 需要的
第三步: 找到 葛式八法的点位


trade_date,open,close,high,low,WeekMa10,WeekMa60,Week60-10
2021-03-28,20.55,21.14,21.65,20.4,22.452999999999992,16.50683333333334,-5.946166666666652



'''
def getallstockdata_is_GeShi_8fa():
    print '------start 葛式八法---'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    # print len(data)
    # print '1111111'
    for index, row in data.iterrows():
        stock_code = row['ts_code']

        stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        # print df
        if (df.empty):
            continue

        isAn_GEShi8_model(df, stock_code)
        count = count + 1
        # print count


def isAn_GEShi8_model(data,stock_code):
    # data = data.reset_index(drop=True)  # 重新建立索引 ,
    # print data
    data= data.reset_index()
    # print data



    riqi =data.ix[0][0]
    #1 选出 最小值
    mini =abs(data.ix[0]['Week60-10'])
    for index, row in data.iterrows():
        Week60_10 = abs(row['Week60-10'])

        if(Week60_10<mini):
            mini = Week60_10
            riqi = row['trade_date']


    #2 判断日期是近一个月

    from datetime import datetime, timedelta
    today = datetime.now().strftime('%Y-%m-%d')

    today = datetime(int(today[0:4]), int(today[5:7]), int(today[8:10]))

    today_30 = today + timedelta(days=-30)
    today_30= str(today_30)
    # print today_30
    next_day = datetime(int(today_30[0:4]), int(today_30[5:7]), int(today_30[8:10]))
    # cur_day = datetime(2021, 04, 18)

    cur_day= datetime(int(riqi[0:4]),int(riqi[5:7]), int(riqi[8:10]))


    # 3 判断 慢线是上涨趋势  起码近 2 个月,也就是 前 8 个数据
    # 快线 也是 上涨趋势,

    WeekMa60_max = data.ix[0]['WeekMa60']
    isBigThanWeekMa60 =1

    WeekMa10_max = data.ix[0]['WeekMa10']
    isBigThanWeekMa10 = 1

    data_10 = data[0:20]
    for index, row in data_10.iterrows():
        # print index

        if(row['WeekMa60'] > WeekMa60_max):
            isBigThanWeekMa60=0
        if(row['WeekMa10'] > WeekMa10_max):
            isBigThanWeekMa10=0



    if(mini < 0.1 and (cur_day - next_day).days < 30  and (cur_day - next_day).days > 0 and
    isBigThanWeekMa60 ==1 and isBigThanWeekMa10==1):
        info = stock_code  + "--------- 葛式八法--------" + str(riqi)+ "---mini--"+str(mini)
        print info



if __name__ == '__main__':

    # localpath1 = '/jishu_stock/stockdata/data1/'
    # getAllWeekKdata(localpath1)

    getallstockdata_is_GeShi_8fa()
