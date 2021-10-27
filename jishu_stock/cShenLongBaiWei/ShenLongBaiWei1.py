#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, \
    writeLog_to_txt_path_getcodename
from jishu_stock.z_tool.PyDateTool import get_date1_date2_days
from stock.settings import BASE_DIR


'''
神龙摆尾

1# 找到 涨停板
'''


def getall_ShenLongBaiWei1(localpath1):
    info1= "神龙摆尾  首先要看是不是 下跌后横盘  横盘后出现的第一个涨停板 start "
    writeLog_to_txt_nocode(info1)
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
        data7_1 = df.iloc[0:40]  # 前10个交易日
        # data7_1 = df.iloc[1:41]  # 前10个交易日
        # data7_1 = df.iloc[2:42]  # 前10个交易日
        # data7_1 = df.iloc[3:43]  # 前10个交易日
        # data7_1 = df.iloc[4:44]  # 前10个交易日


        # 2 单独一个函数 判断是不是符合  神龙摆尾
        isyes = isAnShenLongBaiwei_model(data7_1, stock_code)

def isAnShenLongBaiwei_model(data,stock_code):

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

        if(index==0): # 最新的一天, 阳线突破实体
            day1open = row['open']
            day1close= row['close']
            day1riqi = row['trade_date']
            if( day1close - day1open >0 ): #如果是阳线
                # print "阳线 继续"
                continue
            else: break
        if (index == 1):  #
            day1_1open = row['open']
            day1_1close = row['close']
            day1_1riqi = row['trade_date']
        if (index == 2):  #
            day1_2open = row['open']
            day1_2close = row['close']
        if (index == 3):  #
            day1_3open = row['open']
            day1_3close = row['close']
        if (index == 4):  #
            day1_4open = row['open']
            day1_4close = row['close']
        if (index == 5):  #
            day1_5open = row['open']
            day1_5close = row['close']


        # print index
        pct_chg = row['pct_chg']


        #1 找到涨停板, 还有 突破涨停板的最后一天, 判断 之间的天数是不是大于 7 天,
        #2 找到 最后一天相邻的 5 个交易日,判断是不是在箱体内

        if(pct_chg > zhangfuMax):  # 涨停板
            day2riqi = row['trade_date']
            # 涨幅 10%的那一个行
            day2DayangxianClose = row['close']
            day2Dayangxianopen = row['open']

            if(day1close > day2DayangxianClose and  day1open >day2Dayangxianopen and day1open < day2DayangxianClose):
                # print1(day1riqi)
                # print1(day2riqi)
                # print1(stock_code)
                # print get_date1_date2_days(day2riqi,day1riqi)


                # if( (int(day1riqi) - int(day2riqi)) > 7): #1 找到涨停板, 还有 突破涨停板的最后一天, 判断 之间的天数是不是大于 7 天,
                if( get_date1_date2_days(day2riqi,day1riqi) > 7): #1 找到涨停板, 还有 突破涨停板的最后一天, 判断 之间的天数是不是大于 7 天,

                    # 2 找到 最后一天相邻的 5 个交易日,判断是不是在箱体内
                    if(day1_1open < day2DayangxianClose and day1_1open > day2Dayangxianopen
                    and day1_1close < day2DayangxianClose and day1_1close > day2Dayangxianopen):


                        if(day1_2open < day2DayangxianClose and day1_2open > day2Dayangxianopen
                        and day1_2close < day2DayangxianClose and day1_2close > day2Dayangxianopen):
                            if(day1_3open < day2DayangxianClose and day1_3open > day2Dayangxianopen
                            and day1_3close < day2DayangxianClose and day1_3close > day2Dayangxianopen):
                                if(day1_4open < day2DayangxianClose and day1_4open > day2Dayangxianopen
                                and day1_4close < day2DayangxianClose and day1_4close > day2Dayangxianopen):
                                    if(day1_5open < day2DayangxianClose and day1_5open > day2Dayangxianopen
                                    and day1_5close < day2DayangxianClose and day1_5close > day2Dayangxianopen):



                                        info =  str(pct_chg) + "--------- 神1---------" + str(day2riqi) + " 突破阳线日期"+str(day1riqi)
                                        # print info
                                        writeLog_to_txt(info,stock_code)

                                        path = '神 1.txt'
                                        writeLog_to_txt_path_getcodename(info, path, stockcode)

                                        return 1;
        count = count + 1

    return 0;


'''
测试后 老师的 案例 基本都通过
'''
def test_isAnShenLongBaiwei_model():

    # 测试案例 1 渤海租赁
    df1 = ts.pro_bar(ts_code='000415.SZ', start_date='20190403', end_date='20210723')
    data7_1 = df1.iloc[0:40]  # 前4行
    isAnShenLongBaiwei_model(data7_1, '000415.SZ')
    # 测试案例 2 大立科技
    df2 = ts.pro_bar(ts_code='002214.SZ', start_date='20190403', end_date='20210723')
    data7_2 = df2.iloc[0:40]  # 前4行
    isAnShenLongBaiwei_model(data7_2, '002214.SZ')

    # 测试案例 3 飞亚达
    df3 = ts.pro_bar(ts_code='000026.SZ', start_date='20190403', end_date='20200616')
    data7_3 = df3.iloc[0:40]  # 前4行
    # print1(data7_3)
    # isAn_JiuSiYiSheng_2_model(data7_3, '688008.SH')
    isAnShenLongBaiwei_model(data7_3, '000026.SZ')

    # 测试案例 4 首航高科
    df4 = ts.pro_bar(ts_code='002665.SZ', start_date='20190403', end_date='20210902')
    data7_4 = df4.iloc[0:40]  # 前4行
    isAnShenLongBaiwei_model(data7_4, '002665.SZ')

    # 复杂盘面  1 000038深大通

    df5 = ts.pro_bar(ts_code='000038.SZ', start_date='20190403', end_date='20200403')
    data7_5 = df5.iloc[0:40]  # 前4行
    # print1(data7_5)
    isAnShenLongBaiwei_model(data7_5, '000038.SZ')


    # 复杂盘面  2  000400 许继电气, 20191118 以后买入 但是 有一个破了箱体 所以程序跑不出来,
    # 然后但是 如果我每天测试一次, 就可以 在 2019 1113 可以检测出来,所以程序非常好

    df6 = ts.pro_bar(ts_code='000400.SZ', start_date='20190403', end_date='20191113')
    data7_6 = df6.iloc[0:40]  # 前4行
    # print1(data7_6)
    isAnShenLongBaiwei_model(data7_6, '000400.SZ')





'''
学员选出的案例 
测试后 学员的 案例 基本都通过

但是有 2 个褔蓉科技,佛燃能源,是不符合模型的
'''
def test_xueyuan():
    # 学员选出来的 002665 首航高科 完美符合模型
    df_x1 = ts.pro_bar(ts_code='002665.SZ', start_date='20190403', end_date='20210902')
    df_x1 = df_x1.iloc[0:40]  # 前4行
    # print1(df_x1)
    isAnShenLongBaiwei_model(df_x1, '002665.SZ')


    # 学员选出来的 褔蓉科技 603327  ,
    #测试数据失败,原因箱体内
    # df_x2 = ts.pro_bar(ts_code='603327.SH', start_date='20190403', end_date='20210831')
    # df_x2 = df_x2.iloc[0:40]  # 前4行
    # # print1(df_x2)
    # isAnShenLongBaiwei_model(df_x2, '603327.SH')


    # 学员选出来的 002911佛燃能源
    #测试数据失败,原因箱体内
    # df_x3 = ts.pro_bar(ts_code='002911.SZ', start_date='20190403', end_date='20210907')
    # df_x3 = df_x3.iloc[0:40]  # 前4行
    # print1(df_x3)
    # isAnShenLongBaiwei_model(df_x3, '002911.SZ')

    df_x3 = ts.pro_bar(ts_code='603520.SH', start_date='20190403', end_date='20211013')
    df_x3 = df_x3.iloc[0:40]  # 前4行
    print1(df_x3)
    isAnShenLongBaiwei_model(df_x3, '603520.SH')

'''
回测 6月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'

    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)


        data6_1 = df.iloc[0:40]  # 前10个交易日
        data6_1 = df.iloc[44:84]  # 前10个交易日 7 月份
        data6_1 = df.iloc[44:90]  # 前10个交易日 7 月份

        len_1=len(data6_1)

        for i in range(0, len_1 - 40 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAnShenLongBaiwei_model(data6_1[i:i + 40], stock_code)
if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # getallstockdata_isShenLongBaiWei('20210701', '20210805')
    # anstock_isShenLongBaiWei_model('000539.SZ','20210701', '20210805')
    localpath1 = '/jishu_stock/stockdata/data1/'
    # getall_ShenLongBaiWei1(localpath1)
    # test_Befor_data() # 找到 7 月份的数据
    # test_isAnShenLongBaiwei_model() # 老师案例
    test_xueyuan() # 学员案例




