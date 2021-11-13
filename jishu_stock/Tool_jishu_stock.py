#!/usr/bin/python
# -*- coding: utf8 -*-
import collections
import datetime
import time

from stock.settings import BASE_DIR
import pandas as pd
import tushare as ts

'''
time.sleep(0.03)  # //睡觉
'''

'''
给信息 还有路径 写入文件
'''

'''
测试程序案例
'''
'''
def test_getallstockdata_isLongZhan_YuYe():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    pro = ts.pro_api()
    stock_code='000158.SZ'
    # print 'stockcode'+stock_code
    df = pro.daily(ts_code='000158.SZ', start_date='20210401', end_date='20210422')
    data= df[0: 3]
    # print data
    isAn_LongZhanYuYe_model(data, stock_code)

'''


'''
判断一行是不是 阴线, 返回 1 是阴线, 返回0 是阳线
isYangXian(row)是有缺陷的,比如 开盘价=收盘价的时候 也判断为阴线

'''
def isYinXian(row):
    # print row['open']
    # print row['close']
    # print len(row)
    if(len(row) > 0):
        # print'-----'
        if(row['open'] > row['close']):
            # print row['open']
            return 1
        # if(row['open'] == row['close']):
        #     return 2 # 不阴不阳
    return 0


'''
判断一行是不是 阳线, 返回 1 是阳线, 返回0 是阴线
'''
def isYangXian(row):
    # print row['open']
    # print row['close']
    # print len(row)
    if(len(row) > 0):
        # print'-----'
        if(row['open'] < row['close']):
            # print row['open']
            return 1
        # if(row['open'] == row['close']):
        #     return 2 # 不阴不阳
    return 0


import inspect
import re

def print1(name):
    x=name
    frame = inspect.currentframe().f_back
    s = inspect.getframeinfo(frame).code_context[0]
    r = re.search(r"\((.*)\)", s).group(1)
    print("{} = {}".format(r,x))

'''
数组 是由小到大排列  返回 1  ,否则 0 
'''
def is_small_to_big(data):
    len_data = len(data)
    if(len_data > 0):
        is_small_to_big_flag=1
        for i in range(0, len_data - 1):  #思路, 只要有个一 数据 大于后边数据 那么就不满足 由小到大排序
            # week10_60s[i:i+1]
            if (data[i] > data[i + 1]):
                is_small_to_big_flag = 0

        if(is_small_to_big_flag == 1):
            return 1
    return 0


'''
数组 data[]是由大到小排列  返回 1  ,否则 0 
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
价格中枢用到 专用

可以指定路径, 并且 得到股票名字的 

'''

def jiagezhongshu_writeLog_to_txt_path_getcodename(info ,path,code):
    info = info + '--' + get_Stock_Name(code)

    if (isInQiangShi_gupiaochi(code) == 1):
        info = info + '--强势股票'

    if (is_XiaoShu_gupiaochi(code) == 1):
        info = info + '--小树股票池'
    if (is_YouQianJun_gupiaochi(code) == 1):
        info = info + '--有钱君股票池'

    info = info + '**' + str(code)
    print info

    with open(path, "a") as f:
        f.write(info + '' + "\n")



'''
用来对每一个模型 做积累统计, 这样后期方便回测
可以指定路径, 并且 得到股票名字的 
'''
def writeLog_to_txt_path_getcodename(info ,path,code):
    info = info + '--' + get_Stock_Name(code)

    if (isInQiangShi_gupiaochi(code) == 1):
        info = info + '--强势股票'

    if (is_XiaoShu_gupiaochi(code) == 1):
        info = info + '--小树股票池'
    if (is_YouQianJun_gupiaochi(code) == 1):
        info = info + '--有钱君股票池'

    info = info + '**' + str(code)
    # print info

    path = BASE_DIR + '/jishu_stock/zJieGuo/huizong/' + path
    with open(path, "a") as f:
        f.write(info + '' + "\n")

def writeLog_to_txt_path(info ,path):
    with open(path, "a") as f:
        f.write(info + '' + "\n")


#  下边的  writeLog_to_txt  writeLog_to_txt_nocode 两个函数用用一路径
path = BASE_DIR + '/jishu_stock/zJieGuo/11月/' + datetime.datetime.now().strftime(
        '%Y-%m-%d') + '.txt'
'''
固定路径的写入 带 code 的, 每个输出都有的
'''
def writeLog_to_txt(info,code):
    # path = BASE_DIR + '/jishu_stock/zJieGuo/10月/' + datetime.datetime.now().strftime(
    #     '%Y-%m-%d') + '.txt'

    info = info + '--' + get_Stock_Name(code)

    if(isInQiangShi_gupiaochi(code)==1):
        info = info +'--强势股票'

    if(is_XiaoShu_gupiaochi(code)==1):
        info = info + '--小树股票池'
    if(is_YouQianJun_gupiaochi(code)==1):
        info = info + '--有钱君股票池'

    info = info +'**'+str(code)

    # info= info+'--'+get_Stock_Name(code)
    print info

    with open(path, "a") as f:
        f.write(info + '' + "\n")

'''
固定路径的写入
'''
def writeLog_to_txt_nocode(info):
    # path = BASE_DIR + '/jishu_stock/zJieGuo/10月/' + datetime.datetime.now().strftime(
    #     '%Y-%m-%d') + '.txt'

    qianzhui ='---------------------------------------'
    info = qianzhui + info + qianzhui
    print info


    with open(path, "a") as f:
        f.write(info + '' + "\n")

'''
通过分析每天的日志,得到 一只股票出现 2 次模型的 个股


通常来讲，我们如果只是迭代文件对象每一行，
并做一些处理，是不需要将文件对象转成列表的，因为文件对象本身可迭代，而且是按行迭代：
'''

def get_2stockcode():
    # ss='-----有钱君-120-250 均线交易法 成功了 ----20210917--药明康德--小树股票池--有钱君股票池**603259.SH'
    # print ss.split('**')
    list=[]
    with open(path, "r") as f:
        for line in f:
            # print line
            ss = line.split('**')
            # print len(ss)
            if(len(ss)>1):  #https://www.cnblogs.com/zyber/p/9578240.html
                list.append(ss[1].rstrip('\n'))
    dic = collections.Counter(list)
    # print dic
    list3='一只股票出现 2 次模型的 个股--'+'\n'
    for key in dic:
        shuliang= dic[key]
        if(shuliang>1):
            # print(key, dic[key])
            # list2.append((key, dic[key]))
            list3=list3+str(key)+'='+str(shuliang) +'\n'

    with open(path, "a") as f:
        f.write(str(list3)+'\n')


'''
从 dataframe 中 找到 每日K 线中最低值 中最小的 那个数值
'''
def  getMin_low_fromDataFrame(data):
    Mindata= data.ix[0]['low']
    for index ,row in data.iterrows():
        if( Mindata > row['low']):  # 近 10 天的最小值
            Mindata = row['low']
    return Mindata
'''
从 dataframe 中 找到 每日K 线中最高值 high 中最大的 那个数值
'''
def getMax_High_fromDataFrame(data):
    maxData = data.ix[0]['high']
    for index , row in data.iterrows():
        if(maxData < row['high']):
            maxData = row['high']
    return maxData

'''
获取 之前 -30 , 1 ,2 3,天之前的日期
'20210813'
'''
def getRiQi_Befor_Ater_Days(date,numdays):
    day1riqi = str(date)
    # print day1riqi
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    result_date = cur_day + datetime.timedelta(days=numdays)
    try:
        result_date = result_date.strftime('%Y%m%d')
    except Exception as e:
        print e


    return result_date

'''
获取 之前 30 天之前的日期
'20210813'
'''
def getRiQi_Befor_30Days(date):
    day1riqi = str(date)
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    result_date = cur_day + datetime.timedelta(days=-30)
    try:
        result_date = result_date.strftime('%Y%m%d')
    except Exception as e:
        print e


    return result_date
'''
获取 之前 60 天之前的日期
'20210813'
'''
def getRiqi_Befor_60Days(date):
    day1riqi = str(date)
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    result_date = cur_day + datetime.timedelta(days=-60)
    try:
        result_date = result_date.strftime('%Y%m%d')
    except Exception as e:
        print e
    return result_date

'''
判断是不是上涨趋势 
因为是要获取网络数据 ,所以 尽量要在 for 循环中加入条件

得到 最近 30 天 数据'low'的最小值,min_7days
得到 60 天 数据的 数据'low'的最小值  min_30days

发现 判断 最小值   要比 判断最大值 更好一些   起码 最近 2 个月是上涨的
'''
def isShangZhang_QuShi(data):
    date_1day = data.ix[0]['trade_date']
    stock_code = data.ix[0]['ts_code']

    data_7days = data.iloc[0:7]
    min_7days = getMin_low_fromDataFrame(data)
    date_30days = getRiQi_Befor_30Days(date_1day)
    date_60days = getRiqi_Befor_60Days(date_1day)
    #得到近期数据

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    pro = ts.pro_api()
    df30 = pro.daily(ts_code=stock_code, start_date=date_30days, end_date=date_1day)
    df60 = pro.daily(ts_code=stock_code, start_date=date_60days, end_date=date_1day)

    min_30days = getMin_low_fromDataFrame(df30)
    min_60days = getMin_low_fromDataFrame(df60)
    if(min_30days > min_60days ):
        # print  '----上涨趋势----'+stock_code
        return 1
    return 0



'''
给出 股票代码 得到 股票的名字
'''
def  get_Stock_Name(code):
    # path = path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path)
    for index, row in data.iterrows():
        if (row['ts_code'] == code):
            return row['name']

    return 'code_name is null-'+str(code)



'''
判断一只股票是不是 在有钱君的股票池中
'''

def is_YouQianJun_gupiaochi(code):
    path= BASE_DIR + '/jishu_stock/stockdata/有钱君股票池.csv'
    data = pd.read_csv(path)

    count = 0
    if (len(data.columns) == 1):  # 只有一列股票代码,没有股票名称
        for index, row in data.iterrows():
            if(row['ts_code'] == code):

                return 1
    return 0


'''
判断一只股票是不是 在小树的股票池中
'''

def is_XiaoShu_gupiaochi(code):
    path = BASE_DIR + '/jishu_stock/stockdata/小树股票池.csv'
    data = pd.read_csv(path)

    count = 0
    if (len(data.columns) == 1):  # 只有一列股票代码,没有股票名称
        for index, row in data.iterrows():
            if(row['ts_code'] == code):

                return 1
    return 0
'''
判断一只股票是不是 在强势股票池中
'''
def isInQiangShi_gupiaochi(code):
    path = BASE_DIR + '/jishu_stock/stockdata/强者恒强股票池.csv'
    data = pd.read_csv(path)

    count = 0
    if (len(data.columns) == 1):  # 只有一列股票代码,没有股票名称
        for index, row in data.iterrows():
            if(row['ts_code'] == code):

                return 1
    return 0

'''
单纯 测试 cronette定时任务是不是启动成功
'''
def dingshi_ceshi():
    print '看看能不能引用到'
    path = '00_测试定时任务.txt'
    info='看看能不能引用到'+str( datetime.datetime.now())
    stockcode='000001.SZ'
    writeLog_to_txt_path_getcodename(info, path, stockcode)


if __name__ == '__main__':
    # isInQiangShi_gupiaochi('603041.SH')
    # print get_Stock_Name('603040.SH')
    # stoc_code_zhuanhuan()
    # get_houzhui_code('000661')
    get_2stockcode()


