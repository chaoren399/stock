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

原理: 庄家的空间洗盘
'''

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
        # data7_1 = df.iloc[16:38]  # 7 月份的
        data7_1 = df.iloc[0:2]  # 6 月份的
        # data7_1 = df.iloc[1:8]  # 前7行
        # 2 单独一个函数 判断是不是符合 7 星落长空模型
        isAn_ShuangLong_Qushui_model_pro(data7_1, stock_code)  # 七星 1
        # isAn7start2_model_pro(data7_1, stock_code) # 七星 2


def isAn_ShuangLong_Qushui_model_pro(dataframe_df,stockcode):
    len1 = len(dataframe_df)
    # print len1
    for i in range(0,len1-2+1):
        # print "i" + str(i )+ "j"+str(i+3)
        # print dataframe_df[i:i+3]
        # isKanglongyouhui_3Days_data(dataframe_df[0:3])
        isAn_2ZhangtingBan_model(dataframe_df[i:i+2],stockcode)

'''
判断 2 跟 k 线是不是满足 涨停板, 一个是放量, 另一个是缩量


               60  00 开头的 10%  30 68 开头的 20%
    
               
'''
def isAn_2ZhangtingBan_model(data,stock_code):
    data = data.reset_index(drop=True)  # 重新建立索引 ,
    print data

    if(len(data) ==2):
        data = data.reset_index(drop=True)  # 重新建立索引 ,
        # print data
        qianzhui_code = stock_code[0:2]
        zhangfuMax = 9  # 涨幅 是不是大于 这个
        if (qianzhui_code == '00' or qianzhui_code == '60'):  #   60  00 开头的 10%  30 68 开头的 20%
            zhangfuMax = 9.1
        elif (qianzhui_code == "30" or qianzhui_code == '68'):
            zhangfuMax = 19

        count =0
        vol1=0
        vol2=0
        riqi1 = data.ix[0]['trade_date']  # 最新的日期在前
        riqi2 = data.ix[1]['trade_date']

        for index, row in data.iterrows():
            pct_chg = row['pct_chg']
            if (pct_chg > zhangfuMax):  # 涨停板
                count= count+1
            if(index==0):
                vol2 = row['amount']
            if(index==1):
                vol1 = row['amount']


        if( count == 2 and  vol1 >  vol2):
        # if( count == 2 ):
            info = stock_code + "  --vol1=" + str(vol1) + "  --vol2=" + str(vol2)+ "----- 双龙取水  ---------" + str(riqi1)+'---'+str(riqi2)
            # print info
            writeLog_to_txt(info, stock_code)
            return 1

    return 0



if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # getallstockdata_isShenLongBaiWei('20210701', '20210805')
    # anstock_isShenLongBaiWei_model('000539.SZ','20210701', '20210805')
    localpath1 = '/jishu_stock/stockdata/data1/'
    getallstockdata_is_ShuangLong_Qushui_FromLocal(localpath1)

    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds
