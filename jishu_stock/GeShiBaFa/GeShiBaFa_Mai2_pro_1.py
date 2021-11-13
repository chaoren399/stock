#!/usr/bin/python
# -*- coding: utf8 -*-
import pandas as pd

from jishu_stock.Tool_jishu_stock import isInQiangShi_gupiaochi, get_Stock_Name
from stock.settings import BASE_DIR

'''
https://www.cnblogs.com/chaoren399/p/15231305.html

https://xueqiu.com/3476656801/202373674

葛式八法 买 2

2021年09月10日 通过 学员朋友的选股测试, 我发现 鱼跃龙门 很好用,
而且 G8M2 也比较实用,

所以我要取 5 个数组 最新的 2 个数据, 是由大到小,

然后后 3 个是 由小到大的就可以. 判断出那个阳线拐点位置就可以.




2021年09月05日  又想到的  1周测试一词

我要找的是 拐点, 那个拐点 就是向上突破的 阳线.  我只要 找到 下降的那一半就可以对吧. 
所以, 我获取最新数据后,  截取 2-3 个 以前的数据,来判断是不是就可以了.


思路 2021年09月04日 

MA10 - MA60 的值放到数组中
只要判断  最老的是最小值, 最新的是最大值

方法: 
把数组 分为 2 个数组  for 循环来依次分割
然后第一个数组 是由大到小排列 , 第二个数组是有小达到排序

'''

def getallstockdata_isG8_Mai2_Pro_fromLocal():
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

            df=df.iloc[0:5]  # 只找最近 1 个月的
            #1 m 是 上涨的部分 之选 2-4 周
            #2 n 是下降部分  选择 4-10
            # df=df.iloc[2:8]  # 只找最近 1 个月的


            is_G8_Mai2_model_pro_Pro_1(df, stock_code)
            count = count + 1

'''
方法: 

判断 2 个  数组 是由大到小排列  和由小到大排序

'''

def is_G8_Mai2_model_pro_Pro_1(data, stock_code):
    if(len(data)==5):
        week10_60s=[]
        for index, row in data.iterrows():
            Week10_60 = row['Week10-60']
            WeekMa60=row['WeekMa60']
            #收盘价 必须 大于 WeekMa60
            close_price = row['close']
            if(close_price < WeekMa60 ):
                return

            if(Week10_60 < 0): # 快速 必须大于 慢速
                return
            week10_60s.append(Week10_60)

        week10_60_1=week10_60s[0:2]
        week10_60_2=week10_60s[2:5]
        # print week10_60s
        # info = stock_code + "-------------------G8买2 pro-1"
        # print info

        if(is_big_to_small(week10_60_1)==1 and is_small_to_big(week10_60_2)==1):

                info = stock_code + "-------------------G8买2 pro-1"

                path = BASE_DIR + '/jishu_stock/zJieGuo/G8/9/' + 'G8M2-Pro-' + datetime.datetime.now().strftime(
                    '%Y-%m-%d') + '.txt'
                if (isInQiangShi_gupiaochi(stock_code)):
                    info = info + '--强势股票--'
                info = info + '--' + get_Stock_Name(stock_code)
                print info
                with open(path, "a") as f:
                    f.write(info + '' + "\n")
                return

            # print week10_60s


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


def test_one_stock_is_GeShi_8fa():
    # stock_code='000001.SZ'
    # stock_code='603993.SH'
    # stock_code='000002.SZ'
    # stock_code='000301.SZ'
    stock_code='002318.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    # print df
    # df = df.iloc[6:11]  # 测试  上个月的数据 6 月份
    df = df.iloc[6:11]  # 测试  上个月的数据 6 月份
    is_G8_Mai2_model_pro_Pro(df, stock_code)



if __name__ == '__main__':
    import datetime
    starttime = datetime.datetime.now()

    getallstockdata_isG8_Mai2_Pro_fromLocal()
    # test_one_stock_is_GeShi_8fa()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds
