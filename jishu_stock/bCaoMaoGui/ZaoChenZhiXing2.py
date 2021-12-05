#!/usr/bin/python
# -*- coding: utf8 -*-

from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
from threading import Thread
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
早晨之星2
十字星下影线比实体大 1.5 倍
主要改进十字星, 条件就是下影线 长度是 实体的一倍

https://www.yuque.com/chaoren399/eozlgk/zsigty/

1、典型的见底上涨信号，由三根K线组成
2、第一根是较大的阴线，表明市场在下跌
3、第二根是十字星(阴阳皆可)，表明要变盘
4、第三根是无长上影线的较大阳线，确认变盘
5、阳线至少要收复第一-根阴线的2/3以上


ZaoChenZhiXing

'''

chengongs=[]
modelname='早晨之星2'


def get_all_ZaoChenZhiXing2_duoxiancheng(localpath1):
    info1=  '--早晨之星2start--   '
    writeLog_to_txt_nocode(info1)

    stock_codes= get_all_codes_from_tool()
    len_codes= len(stock_codes)

    a = stock_codes[0:len_codes / 2]
    b = stock_codes[len_codes / 2:len_codes]


    t1 = Thread(target=huice_duozhi_stock, args=(a,))  # 定义线程t1，线程任务为调用task1函数，task1函数的参数是6
    t2 = Thread(target=huice_duozhi_stock,args=(b,))  # 定义线程t2，线程任务为调用task2函数，task2函数无参数
    t1.start()  # 开始运行t1线程
    t2.start()  # 开始运行t2线程
    #join()只有在你需要等待线程完成时候才是有用的。
    t1.join()
    t2.join()

def get_all_ZaoChenZhiXing2(localpath1):
    info1=  '--早晨之星2start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ZaoChenZhiXing2_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ZaoChenZhiXing2_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-3:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        # print1(data1)

        # 设置两个 key
        key_1=0; #1 第一天是实体比较大阴线
        key_2=0; #2 第 2 跟是十字星, 阴阳无所谓
        key_3=0; #3  第 3 天是无长上影线的较大阳线 .
        key_4=0; #4 第 3 天是无长上影线
        key_5=0; #5 阳线至少要收复第一根阴线的2/3以上

        key_6=0; #6 发现 第 2 天十字星 的开盘和收盘都低于第 1 天阴线的 收盘价

        count=0
        day1_yinxian_shiti=0
        day2_shizixing_shiti=0
        day3_yangxian_shiti=0
        day1_open=0
        day1_close=0
        day1_high=0
        day1_low=0
        sanfenzhi2_yinxian=0
        day3_yangxian_close=0
        day3_yangxian_high=0
        day3_yangxian_open=0
        day3_shangyingxian_shiti_beishu=0
        day2_shizixing_open=0
        day2_shizixing_close=0
        day3_riqi=0

        shizixing_xiayingxian=0
        shizixing_shiti=0
        shizixing_xiayingxian_shiti_beishu=0

        for index,row in data1.iterrows():
            if(index==0 and isYinXian(row)==1):
                count=count+1
                day1_yinxian_shiti=getShiTiDaXiao(row)
                day1_open= row['open']
                day1_close= row['close']
                day1_high=row['high']
                day1_low=row['low']

            if(index==1 ): #十字星
                count=count+1
                day2_shizixing_shiti=getShiTiDaXiao(row)
                day2_shizixing_open=row['open']
                day2_shizixing_close=row['close']
                day2_shizixing_low=row['low']
                if(isYinXian(row)==1):#阴线十字星
                    shizixing_xiayingxian = day2_shizixing_close - day2_shizixing_low
                    shizixing_shiti = day2_shizixing_open - day2_shizixing_close +0.000001

                else: #阳线十字星
                    shizixing_xiayingxian= day2_shizixing_open-day2_shizixing_low
                    shizixing_shiti= day2_shizixing_close-day2_shizixing_open + 0.000001
                shizixing_xiayingxian_shiti_beishu = shizixing_xiayingxian / shizixing_shiti


            if(index==2and isYangXian(row)==1):
                count=count+1
                day3_yangxian_shiti=getShiTiDaXiao(row)
                day3_yangxian_close=row['close']
                day3_yangxian_high=row['high']
                day3_yangxian_open=row['open']
                day3_riqi=row['trade_date']

        if(count==3):
            # 1第一天是实体比较大阴线
            if(day1_yinxian_shiti > 1.9):  #案例中最小的 1.99  5.62 2.69 3.73
                key_1=1
            # 2 第 2 跟是十字星, 阴阳无所谓

            # 或者像华微电子  下影线 比实体大 2 倍以上
            # day2_shizixing_open_close=day2_shizixing_open -day2_shizixing_close
            # day2_shizixing_xiayingxian = day2_shizixing_close - day2_shizixing_low

            # if(day2_shizixing_shiti <0.6):
            if(shizixing_xiayingxian_shiti_beishu > 1.5):
                key_2=1


            # 3  第 3 天是无长上影线的较大阳线 .
            if(day3_yangxian_shiti > 1.6):
                key_3=1

            # 4 第 3 天是无长上影线
            #思路: 上影线的大小 / 实体的大小
            day3_shangyingxian= day3_yangxian_high - day3_yangxian_close
            day3_shiti= day3_yangxian_close - day3_yangxian_open + 0.000001

            day3_shangyingxian_shiti_beishu=day3_shangyingxian /day3_shiti
            if(day3_shangyingxian_shiti_beishu < 0.5 ): # 是不是长上影线
            # if(day3_shangyingxian_shiti_beishu < 1.2 ): # 是不是长上影线
                key_4=1

            #5 阳线至少要收复第一根阴线的2/3以上
            sanfenzhi2_yinxian=(day1_open+day1_close) /2  #
            # sanfenzhi2_yinxian=(day1_high+day1_low) /2 # 价格中枢

            if(day3_yangxian_close > sanfenzhi2_yinxian) :
                key_5=1

            # 6 发现 第 2 天十字星 的开盘和收盘都低于第 1 天阴线的 收盘价

            # if(day2_shizixing_open < day1_close and day2_shizixing_close < day1_close):
            if(day2_shizixing_open < day1_close or day2_shizixing_close < day1_close):
            # if(day2_shizixing_low < day1_low ):
                key_6=1
        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(key_6)
        # print1(day2_shizixing_shiti)
        # print1(shizixing_xiayingxian)
        # print1(shizixing_shiti)
        # print1(shizixing_xiayingxian_shiti_beishu)
        # # print1(sanfenzhi2_yinxian)
        # print1(day3_yangxian_shiti)
        # print1(day3_shangyingxian_shiti_beishu)
        # print1(sanfenzhi2_yinxian)
        # # print1(day1_yinxian_shiti)


        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1 and key_6==1) :
        # if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1 ) :
            info = ''
            info=info+'阴线实体='+str(day1_yinxian_shiti)

            info = info + "--早晨之星2  成功了"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '早晨之星2.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            # get_shouyi(stockcode, day3_riqi, day2_shizixing_low)
            chenggong_code={'stockcode':stockcode,'mairuriqi':day3_riqi,'zhiyingdian':day2_shizixing_low}
            # print1(day2_shizixing_low)
            chengongs.append(chenggong_code)


'''
测试老师的案例
'''
def test_isAn_ZaoChenZhiXing2_laoshi():
    # 案例 1  002475 立讯精密
    df1 = ts.pro_bar(ts_code='002475.SZ',adj='qfq', start_date='20190206', end_date='20191010')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1,'002475.SZ')

    # 案例 2 002156 通富微电
    df1 = ts.pro_bar(ts_code='002156.SZ', adj='qfq', start_date='20190206', end_date='20191022')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '002156.SZ')

    # 案例 3  万达信息  300168

    df1 = ts.pro_bar(ts_code='300168.SZ', adj='qfq', start_date='20190206', end_date='20191104')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '300168.SZ')
    # 案例 4  605006  山东玻纤
    df1 = ts.pro_bar(ts_code='605006.SH', adj='qfq', start_date='20190206', end_date='20201103')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '605006.SH')
    # 案例 5 雅克科技**002409.SZ
    df1 = ts.pro_bar(ts_code='002409.SZ', adj='qfq', start_date='20190206', end_date='20191224')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '002409.SZ')
    print  "总共 5 个成功案例"

'''
老师举例 符合模型,但是实体比较大的案例
'''
def test_shizixing_da():

    # 案例 6 688111 华微电子 十字星实体比较大
    df1 = ts.pro_bar(ts_code='600360.SH', adj='qfq', start_date='20190206', end_date='20200429')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '600360.SH')

    # 案例 7 688111 金山办公 十字星实体比较大
    df1 = ts.pro_bar(ts_code='688111.SH', adj='qfq', start_date='20190206', end_date='20200706')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '688111.SH')

    # 案例8  300034 案例22：钢研高纳  # 十字星实体 0.7 比较大了

    df1 = ts.pro_bar(ts_code='300034.SZ', adj='qfq', start_date='20190206', end_date='20201103')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '300034.SZ')

    # 案例 9华微电子

    df1 = ts.pro_bar(ts_code='600360.SH', adj='qfq', start_date='20190206', end_date='20200429 ')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '600360.SH')



'''
测试老师 的反面案例, 就是不像模型的, 验证程序的健壮性
'''
def test_fanmian_anli():
    # 600360


    # 案例 7 反面案例 ,测试程序 300724
    df1 = ts.pro_bar(ts_code='300724.SZ', adj='qfq', start_date='20190206', end_date='20200821 ')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '300724.SZ')

    #20200414  688111  金山
    df1 = ts.pro_bar(ts_code='688111.SH', adj='qfq', start_date='20190206', end_date='20200414 ')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1, '688111.SH')

'''
测试自己的案例  盾安环境
'''
def test_isAn_ZaoChenZhiXing2_ziji():


    # #盾安环境 002011
    # df1 = ts.pro_bar(ts_code='002011.SZ', adj='qfq', start_date='20210206', end_date='20211014')
    # data7_1 = df1.iloc[0:30]  # 前7行
    # isAn_ZaoChenZhiXing2_model(data7_1, '002011.SZ')

    # 案例 1  002475 立讯精密
    # df1 = ts.pro_bar(ts_code='002475.SZ',adj='qfq', start_date='20190206', end_date='20191010')
    # data7_1 = df1.iloc[0:30]  # 前7行
    # isAn_ZaoChenZhiXing2_model(data7_1,'002475.SZ')

    #000869.SZ

    df1 = ts.pro_bar(ts_code='000869.SZ',adj='qfq', start_date='20190206', end_date='20211029')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing2_model(data7_1,'000869.SZ')


'''
回测 8 月份的数据
'''
def test_Befor_data():
    stock_codes= get_all_codes_from_tool()
    len_codes= len(stock_codes)

    a = stock_codes[0:len_codes / 2]
    b = stock_codes[len_codes / 2:len_codes]


    t1 = Thread(target=huice_duozhi_stock, args=(a,))  # 定义线程t1，线程任务为调用task1函数，task1函数的参数是6
    t2 = Thread(target=huice_duozhi_stock,args=(b,))  # 定义线程t2，线程任务为调用task2函数，task2函数无参数
    t1.start()  # 开始运行t1线程
    t2.start()  # 开始运行t2线程
    #join()只有在你需要等待线程完成时候才是有用的。
    t1.join()
    t2.join()


    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)

'''
回测 多只 股票数据
'''
def  huice_duozhi_stock(stock_codes):
    for index, item in enumerate(stock_codes):
        # print index, item
        huice_one_stock(item)

'''
回测一只股票的函数
'''
def huice_one_stock(stock_code):
    stock_code = stock_code
    stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    data7_4 = df.iloc[22:32]  # 前10个交易日
    # data7_4 = df.iloc[22:22+22+6]  # 前10个交易日
    # data7_4 = df.iloc[22:22+250+6]  # 去年 1 年的
    # data7_4 = df.iloc[10:22]  # 前10个交易日
    len_1 = len(data7_4)
    for i in range(0, len_1 - 6 + 1):
        # print "i" + str(i )+ "j"+str(i+3)
        isAn_ZaoChenZhiXing2_model(data7_4[i:i + 6], stock_code)


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_ZaoChenZhiXing2(localpath1)
    # test_isAn_ZaoChenZhiXing2_laoshi()
    # test_shizixing_da()
    # test_fanmian_anli()

    test_Befor_data()
    # test_isAn_ZaoChenZhiXing2_ziji()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print round((endtime - starttime).seconds / 60 ,2)