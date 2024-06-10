#!/usr/bin/python
# -*- coding: utf8 -*-

from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
早晨之星
十字星实体 小于 0.6
https://www.yuque.com/chaoren399/eozlgk/zsigty/

1、典型的见底上涨信号，由三根K线组成
2、第一根是较大的阴线，表明市场在下跌
3、第二根是十字星(阴阳皆可)，表明要变盘
4、第三根是无长上影线的较大阳线，确认变盘
5、阳线至少要收复第一-根阴线的2/3以上


ZaoChenZhiXing

'''
infolists=[]
chengongs=[]
modelname='早晨之星'
def get_all_ZaoChenZhiXing(localpath1):
    info1=  '--早晨之星start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ZaoChenZhiXing_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ZaoChenZhiXing_model(data,stockcode):
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
        day3_riqi = data1.ix[0]['trade_date']  # 阳线的日期
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
        day2_shizixing_low=0

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

            if(day2_shizixing_shiti <0.6):
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
                key_4=1

            #5 阳线至少要收复第一根阴线的2/3以上
            sanfenzhi2_yinxian=(day1_open+day1_close) /2  #
            # sanfenzhi2_yinxian=(day1_high+day1_low) /2 # 价格中枢

            if(day3_yangxian_close > sanfenzhi2_yinxian) :
                key_5=1

            # 6 发现 第 2 天十字星 的开盘和收盘都低于第 1 天阴线的 收盘价

            if(day2_shizixing_open < day1_close and day2_shizixing_close < day1_close):
                key_6=1
        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(key_6)
        # print1(day2_shizixing_shiti)
        # print1(sanfenzhi2_yinxian)
        # print1(day3_yangxian_close)
        # print1(day3_shangyingxian_shiti_beishu)
        # print1(day1_yinxian_shiti)


        if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 and key_5==1 and key_6==1) :
            info = ''
            info=info+'阴线实体='+str(day1_yinxian_shiti)

            info = info + "--早晨之星  成功了"  + str(riqi)
            # print info
            writeLog_to_txt(info, stockcode)
            path = '早晨之星.txt'
            writeLog_to_txt_path_getcodename(info, path, stockcode)

            #回测专用
            chenggong_code={'stockcode':stockcode,'mairuriqi':day3_riqi,'zhisundian':day2_shizixing_low}
            chengongs.append(chenggong_code)




'''
测试老师的案例
'''
def test_isAn_ZaoChenZhiXing_laoshi():
    # 案例 1  002475 立讯精密
    df1 = ts.pro_bar(ts_code='002475.SZ',adj='qfq', start_date='20190206', end_date='20191010')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1,'002475.SZ')

    # 案例 2 002156 通富微电
    df1 = ts.pro_bar(ts_code='002156.SZ', adj='qfq', start_date='20190206', end_date='20191022')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '002156.SZ')

    # 案例 3  万达信息  300168

    df1 = ts.pro_bar(ts_code='300168.SZ', adj='qfq', start_date='20190206', end_date='20191104')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '300168.SZ')
    # 案例 4  605006  山东玻纤
    df1 = ts.pro_bar(ts_code='605006.SH', adj='qfq', start_date='20190206', end_date='20201103')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '605006.SH')
    # 案例 5 雅克科技**002409.SZ
    df1 = ts.pro_bar(ts_code='002409.SZ', adj='qfq', start_date='20190206', end_date='20191224')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '002409.SZ')
    print  "总共 5 个成功案例"

'''
老师举例 符合模型,但是实体比较大的案例
'''
def test_shizixing_da():

    # 案例 6 688111 华微电子 十字星实体比较大
    df1 = ts.pro_bar(ts_code='600360.SH', adj='qfq', start_date='20190206', end_date='20200429')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '600360.SH')

    # 案例 6 688111 金山办公 十字星实体比较大
    df1 = ts.pro_bar(ts_code='688111.SH', adj='qfq', start_date='20190206', end_date='20200706')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '688111.SH')

    # 案例7  300034 案例22：钢研高纳  # 十字星实体 0.7 比较大了

    df1 = ts.pro_bar(ts_code='300034.SZ', adj='qfq', start_date='20190206', end_date='20201103')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '300034.SZ')




'''
测试老师 的反面案例, 就是不像模型的, 验证程序的健壮性
'''
def test_fanmian_anli():
    # 600360
    # 案例 6
    df1 = ts.pro_bar(ts_code='600360.SH', adj='qfq', start_date='20190206', end_date='20200429 ')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '600360.SH')

    # 案例 7 反面案例 ,测试程序 300724
    df1 = ts.pro_bar(ts_code='300724.SZ', adj='qfq', start_date='20190206', end_date='20200821 ')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '300724.SZ')

    #20200414  688111
    df1 = ts.pro_bar(ts_code='688111.SH', adj='qfq', start_date='20190206', end_date='20200414 ')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '688111.SH')

'''
测试自己的案例  雅克科技
'''
def test_isAn_ZaoChenZhiXing_ziji():


    #盾安环境 002011
    df1 = ts.pro_bar(ts_code='002011.SZ', adj='qfq', start_date='20210206', end_date='20211014')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ZaoChenZhiXing_model(data7_1, '002011.SZ')


'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
        data7_4 = df.iloc[22:42]  # 前10个交易日
        data7_4 = df.iloc[22:22+6+22]  # 1 个月
        # data7_4 = df.iloc[22:22+6+120]  # 半年
        # data7_4 = df.iloc[22:22+6+250]  # 去年 1 年的
        len_1=len(data7_4)
        for i in range(0, len_1 - 6 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ZaoChenZhiXing_model(data7_4[i:i + 6], stock_code)
    jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)


if __name__ == '__main__':
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # get_all_ZaoChenZhiXing(localpath1)
    # test_isAn_ZaoChenZhiXing_laoshi()
    # test_fanmian_anli()
    # test_shizixing_da()
    test_Befor_data()
    # test_isAn_ZaoChenZhiXing_ziji()
