#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, writeLog_to_txt_path_getcodename
from stock.settings import BASE_DIR
'''
双龙取水
思路: 判断 2 跟 k 线是不是满足 涨停板, 一个是放量, 另一个是缩量

原理: 庄家的空间洗盘

自己总结 
1-之前 有 跳空的要注意
2-横盘的不要
3- 放量不明显的不要

2021年09月01日 经过回测, 失败的概率很高 , 7月份 成功率只有 0.2
'''

def getallstockdata_is_ShuangLong_Qushui_FromLocal(localpath1):
    info1= "双龙取水  start "
    writeLog_to_txt_nocode(info1)
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


        data7_1 = df.iloc[0:2]  #
        # data7_1 = df.iloc[2:4]  #
        # data7_1 = df.iloc[3:5]  #
        # data7_1 = df.iloc[:5]  #

        isAn_2ZhangtingBan_model(data7_1, stock_code)
        # len1= len(data7_1)
        #
        # for i in range(0, len1 - 2 + 1):
        #     isAn_2ZhangtingBan_model(data7_1[i:i + 2], stock_code)



'''
判断 2 跟 k 线是不是满足 涨停板, 一个是放量, 另一个是缩量


               60  00 开头的 10%  30 68 开头的 20%
    
               
'''
def isAn_2ZhangtingBan_model(data,stock_code):
    data = data.reset_index(drop=True)  # 重新建立索引 ,
    # print data

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
            info =  "  --vol1=" + str(vol1) + "  --vol2=" + str(vol2)+ "----- 双龙取水  ---------" + str(riqi1)+'---'+str(riqi2)
            # print info
            writeLog_to_txt(info, stock_code)

            path = '双龙取水.txt'
            writeLog_to_txt_path_getcodename(info, path, stock_code)
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
