#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, \
    writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from stock.settings import BASE_DIR
import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

'''
找到涨停板

1. 判断当天是不是 涨停板
2. 根据条件 , 是不是近 3 天 最低值附近出现的涨停盘, 急速下跌

https://www.yuque.com/chaoren399/eozlgk/kcmgi6

思路:
1.得到涨停板后 获取 这只股票之前的 90 天数据 (这个数据可以更改)
2. 计算最低价, 如果最低价 的日期 与 涨停板的日期 相减 < 3 那么 ,就可以看看了.
            

'''
chengongs=[]
modelname='V型反转'
zhisundian=0 #这里的变量是个意外, 因为程序是最早写, 没有按照 模板来
def getallstockdata_isV_fromLocal(localpath1):
    info1=  'V型反转start'
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'

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

    if (data is None or data.empty):
        print '--df.empty--' + str(stock_code)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stock_code) + '--data --is null'
    if(len_data >=1):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1 = data[len_data - 1:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,

    qianzhui_code= stock_code[0:2]
    zhangfuMax = 9 # 涨幅 是不是大于 这个
    if(qianzhui_code =='00' or qianzhui_code =='60'):
        zhangfuMax=9.1
    elif(qianzhui_code=="30" or qianzhui_code=='68'):
        zhangfuMax=19
    count =0;


    for index, row in data1.iterrows():

        # print index
        pct_chg = row['pct_chg']
        # print row['trade_date']
        # print row['pct_chg']

        if(pct_chg > zhangfuMax):  # 涨停板
            riqi  = str(row['trade_date'])
            zhisundian= row['low']
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
参数 date  : 涨停板日期
'''
def isXiaDieZhangting(stock_code,date):

    if(len(stock_code)==0 ):
        print  " stock_code is  null"
        return 1
    if(len(date) == 0):
        print " date is null"
    # print "laile "
    cur_day = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))

    result_date = cur_day + datetime.timedelta(days=-90)
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
        info =  " V型反转--" + str(date)
        # print info
        # 统一 info管理 一个函数,每次都要执行, 并且信息 返回后,要添加到 info中,
        # 方便后期修改,这样一改,所有的都可以执行了.
        from jishu_stock.z_tool.InfoTool import manage_info
        manage_info = manage_info(info, stock_code, date, '')
        info = info + manage_info


        writeLog_to_txt(info, stock_code)

        path = 'V型反转.txt'
        writeLog_to_txt_path_getcodename(info, path, stock_code)

        chenggong_code = {'stockcode': stock_code, 'mairuriqi': date, 'zhisundian': zhisundian}
        chengongs.append(chenggong_code)


'''
测试老师用的案例
'''
def test_V_anli_laoshi():
    # print1(tt)

    #1  002028 思源电气
    df = ts.pro_bar(ts_code='002028.SZ', adj='qfq', start_date='20200104', end_date='20210112')
    data7_1 = df.iloc[0:1]  # 是不是 涨停盘
    # 单独一个函数 判断是不是符合 V型反转
    isAnV_model(data7_1, '002028.SZ')

    #2  600216 浙江医药
    df = ts.pro_bar(ts_code='600216.SH', adj='qfq', start_date='20200104', end_date='20210209')
    data7_1 = df.iloc[0:1]  # 是不是 涨停盘
    # 单独一个函数 判断是不是符合 V型反转
    isAnV_model(data7_1, '600216.SH')


    #3  002017 东信和平
    df = ts.pro_bar(ts_code='002017.SZ', adj='qfq', start_date='20200104', end_date='20201229')
    data7_1 = df.iloc[0:1]  # 是不是 涨停盘
    # 单独一个函数 判断是不是符合 V型反转
    isAnV_model(data7_1, '002017.SZ')


    #4  000608 阳光股份

    df = ts.pro_bar(ts_code='000608.SZ', adj='qfq', start_date='20200104', end_date='20210115')
    data7_1 = df.iloc[0:1]  # 是不是 涨停盘
    # 单独一个函数 判断是不是符合 V型反转
    isAnV_model(data7_1, '000608.SZ')

    #5  000545 金浦钛业

    df = ts.pro_bar(ts_code='000545.SZ', adj='qfq', start_date='20200104', end_date='20210209')
    data7_1 = df.iloc[0:1]  # 是不是 涨停盘
    # 单独一个函数 判断是不是符合 V型反转
    isAnV_model(data7_1, '000545.SZ')

    #我自己做的 石基信息 002153

    df = ts.pro_bar(ts_code='002153.SZ', adj='qfq', start_date='20200104', end_date='20210903')
    data7_1 = df.iloc[0:1]  # 是不是 涨停盘
    # 单独一个函数 判断是不是符合 V型反转
    isAnV_model(data7_1, '002153.SZ')

    jisuan_all_shouyilv(chengongs, modelname, 1.03)


def test_V_anli_ziji():
    # df = ts.pro_bar(ts_code='002093.SZ', adj='qfq', start_date='20200101', end_date='20210819')
    # df = ts.pro_bar(ts_code='000889.SZ',adj='qfq', start_date='20200101', end_date='20211009')

    # df = ts.pro_bar(ts_code='000889.SZ', start_date='20200101', end_date='20211009')
    df = ts.pro_bar(ts_code='002612.SZ', start_date='20200101', end_date='20211008') # V型反转有问题, 没有计算出来

    data7_1 = df.iloc[0:1]  # 是不是 涨停盘
    # print data7_1
    # 单独一个函数 判断是不是符合 V型反转
    isAnV_model(data7_1, '002612.SZ')

'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:4]  # 前4行
        data6_1 = df.iloc[0:1]  # 前4行
        data6_1 = df.iloc[22:44]  # 前4行
        # data6_1 = df.iloc[22:22+20+22]  # 1 个月
        data6_1 = df.iloc[22:22+20+120]  #半年

        len_1=len(data6_1)

        for i in range(0, len_1 - 1 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAnV_model(data6_1[i:i + 1], stock_code)

    jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)

if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    # getallstockdata_isV_fromLocal(localpath1)

    # test_V_anli_laoshi()
    test_Befor_data()
    # test_V_anli_ziji()

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"