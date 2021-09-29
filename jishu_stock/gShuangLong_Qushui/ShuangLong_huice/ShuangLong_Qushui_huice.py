#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt
from stock.settings import BASE_DIR
'''
双龙取水
思路: 判断 2 跟 k 线是不是满足 涨停板, 一个是放量, 另一个是缩量

回测 , 看看成功率, 只要第 3 天 是阳线就算成功

原理: 庄家的空间洗盘

自己总结 
1-之前 有 跳空的要注意
2-横盘的不要
3- 放量不明显的不要


'''

count_2tian_manzu =0
count_3tian_manzu= 0

def getallstockdata_is_ShuangLong_Qushui_FromLocal(localpath1):
    print "双龙取水  start "
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/xiadiecodes.csv'

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

        # data7_1 = df.iloc[0:2]  #
        # data7_1 = df.iloc[2:4]  #
        # data7_1 = df.iloc[3:5]  #
        # data7_1 = df.iloc[0:22]  #
        data7_1 = df.iloc[23:55]  #
        len1= len(data7_1)

        for i in range(0, len1 - 3 + 1):
            isAn_2ZhangtingBan_model(data7_1[i:i + 3], stock_code)



'''
判断 2 跟 k 线是不是满足 涨停板, 一个是放量, 另一个是缩量


               60  00 开头的 10%  30 68 开头的 20%
    
               
'''
def isAn_2ZhangtingBan_model(data,stock_code):
    data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    data = data.reset_index(drop=True)  # 重新建立索引 ,
    # print data

    # print data

    if(len(data) ==3):
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data
        qianzhui_code = stock_code[0:2]
        zhangfuMax = 9  # 涨幅 是不是大于 这个
        if (qianzhui_code == '00' or qianzhui_code == '60'):  #   60  00 开头的 10%  30 68 开头的 20%
            zhangfuMax = 9.1
        elif (qianzhui_code == "30" or qianzhui_code == '68'):
            zhangfuMax = 19

        count=0
        # count_all_no_di3tian=0
        global count_2tian_manzu
        global count_3tian_manzu
        vol1=0
        vol2=0
        riqi1 = data.ix[0]['trade_date']  # 最新的日期在前
        riqi2 = data.ix[1]['trade_date']

        # 跳开 是 第2 天的开盘价 大于 第一天的收盘价
        day2_open =0
        day1_close=0

        for index, row in data.iterrows():
            pct_chg = row['pct_chg']


            if(index==0):
                vol1 = row['amount']  # 第一天
                day1_close= row['close']
                if (pct_chg > zhangfuMax):  # 涨停板
                    count = count + 1
            if(index==1):
                vol2 = row['amount'] # 第 2 天
                day2_open=row['open']
                if (pct_chg > zhangfuMax):  # 涨停板
                    count = count + 1
            if(index==2 and count ==2 and  vol1 >  vol2):  # 第 3 天 用 count 判断是不是
                close_price = row['close']
                open_price = row['open']
                if(close_price > open_price): # 阳线
                        # 3天都满足
                    count_3tian_manzu = count_3tian_manzu+1
                    # print '11'



        #跳开 是 第2 天的开盘价 大于 第一天的收盘价

        if( count == 2 and  vol1 >  vol2 and day2_open > day1_close ):
            count_2tian_manzu= count_2tian_manzu+1  # 2 天满足

        # if( count == 2 ):
            info = stock_code + "  --vol1=" + str(vol1) + "  --vol2=" + str(vol2)+ "----- 双龙取水  ---------" + str(riqi1)+'---'+str(riqi2)
            print info
            # writeLog_to_txt(info, stock_code)
            return 1

    return 0



if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # getallstockdata_isShenLongBaiWei('20210701', '20210805')
    # anstock_isShenLongBaiWei_model('000539.SZ','20210701', '20210805')
    localpath1 = '/jishu_stock/stockdata/data1/'
    getallstockdata_is_ShuangLong_Qushui_FromLocal(localpath1)
    # global count_2tian_manzu
    # global count_3tian_manzu
    print 'count_2tian_manzu=' + str(count_2tian_manzu)
    print 'count_3tian_manzu=' + str(count_3tian_manzu)



    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds
