#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, isInQiangShi_gupiaochi, get_Stock_Name, writeLog_to_txt_nocode
from jishu_stock.fGeShiBaFa.Get_Week_K_data import getAllWeekKdata
from stock.settings import BASE_DIR

'''
葛式八法 买 2

思路 2021年09月04日 

MA10 - MA60 的值放到数组中
只要判断  最老的是最小值, 最新的是最大值

方法: 
把数组 分为 2 个数组  for 循环来依次分割
然后第一个数组 是由大到小排列 , 第二个数组是有小达到排序

'''

def getallstockdata_isG8_Mai2_fromLocal():
    print '------start 葛式八法---'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    if(len(data)>0):

        # print len(data)
        # print '1111111'
        for index, row in data.iterrows():
            stock_code = row['ts_code']
            stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                continue

            df=df.iloc[0:12]  # 只找最近 1 个月的

            # 再找到 慢速 60 周均线明显 上涨的,
            # is_G8_Mai2_model(df, stock_code)
            is_G8_Mai2_model_pro(df, stock_code)
            count = count + 1
            # print count

'''
方法: 
把数组 分为 2 个数组  for 循环来依次分割
然后第一个数组 是由大到小排列 , 第二个数组是有小达到排序

'''

def is_G8_Mai2_model_pro(data, stock_code):
    week10_60s = []
    if (len(data) > 0):
        for index, row in data.iterrows():
            # Week60_10 = abs(row['Week60-10'])
            Week10_60 = row['Week10-60']
            if(Week10_60 < 0):
                return
            week10_60s.append(Week10_60)
            # print Week10_60
        #1 . week10_60s 分割 成 2 个数组
        data_len = len(data)

        #2 判断 第一个数组 是不是 由大到小


        for i in range(2, data_len-1):  # 这样写的目的是 数组必须是 2 个数值以上,这样才有意义
            week10_60s_1=week10_60s[0:i]
            week10_60s_2=week10_60s[i:]
            # print week10_60s_1
            # print week10_60s_2

            if(is_big_to_small(week10_60s_1) ==1 and is_small_to_big(week10_60s_2)==1 ):
                # print 'week10_60s='+str(week10_60s)
                # print 'week10_60s_1='+str(week10_60s_1)
                # print 'week10_60s_2='+str(week10_60s_2)
                info = stock_code + "-------------------G8买2"

                path = BASE_DIR + '/jishu_stock/JieGuo/G8/9/' +'G8M2-'+ datetime.datetime.now().strftime(
                    '%Y-%m-%d') +'.txt'
                if (isInQiangShi_gupiaochi(stock_code)):
                    info = info + '--强势股票--'
                info = info + '--' + get_Stock_Name(stock_code)
                print info
                with open(path, "a") as f:
                    f.write(info + '' + "\n")
                return



'''
数组 是由大到小排列  返回 1  ,否则 0 
'''
def is_big_to_small(data):
    len_data = len(data)
    if(len_data > 0):
        isBigToSmall_flag=1
        for i in range(0, len_data - 1):
            # week10_60s[i:i+1]
            if (data[i] < data[i + 1]):
                isBigToSmall_flag = 0

        if(isBigToSmall_flag == 1):
            return 1
    return 0


'''
数组 是由小到大排列  返回 1  ,否则 0 
'''
def is_small_to_big(data):
    len_data = len(data)
    if(len_data > 0):
        is_small_to_big_flag=1
        for i in range(0, len_data - 1):
            # week10_60s[i:i+1]
            if (data[i] > data[i + 1]):
                is_small_to_big_flag = 0

        if(is_small_to_big_flag == 1):
            return 1
    return 0





def is_G8_Mai2_model(data, stock_code):
    # df_week['Week10-60'] #增加了 这一列
    week10_60s=[]
    if(len(data) > 0):
        for index, row in data.iterrows():
            # Week60_10 = abs(row['Week60-10'])
            Week10_60=row['Week10-60']
            week10_60s.append(Week10_60)
        # print week10_60s
        tmp=0
        data_len= len(data)

        isG8mai2=0;
        for i in range(0, data_len - 1 ):
            # week10_60s[i:i+1]
            if(week10_60s[i] < week10_60s[i+1]):
                isG8mai2=1;
                return 0

        if(isG8mai2==0):
            # print "葛式八法 买 2"
            info =  stock_code + "-------------------葛式八法 买 2"
            # print  info
            writeLog_to_txt(info, stock_code)





def test_one_stock_is_GeShi_8fa():
    # stock_code='000001.SZ'
    # stock_code='603993.SH'
    # stock_code='000002.SZ'
    stock_code='000301.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    # print df
    df = df.iloc[0:11]  # 测试  上个月的数据 6 月份
    is_G8_Mai2_model_pro(df, stock_code)



if __name__ == '__main__':
    import datetime
    starttime = datetime.datetime.now()

    getallstockdata_isG8_Mai2_fromLocal()
    # test_one_stock_is_GeShi_8fa()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds
