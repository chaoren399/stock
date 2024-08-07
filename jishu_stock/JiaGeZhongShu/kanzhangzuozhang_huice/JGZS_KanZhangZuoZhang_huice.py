#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions


from jishu_stock.JiaGeZhongShu.jiagezhognshu_Get_Week_K_data import getAll_jiagezhongshu_WeekKdata
from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, print1, isYinXian, isYangXian, \
    jiagezhongshu_writeLog_to_txt_path_getcodename, writeLog_to_txt_path_getcodename,writeLog_to_txt_path
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.z_tool.email import webhook
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
import pandas as pd
from pandasCSVTools  import exced_csv_kanzhangjiegou
from jishu_stock.z_tool.PyDateTool import covert_date
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
创建日期: 2021年10月29日
更新日期:
价格中枢-看涨做涨
https://www.yuque.com/chaoren399/eozlgk/nzv2b4/


上涨初期或中期
实体较大有上下影线的阳线
实体的1/2恰好是中枢价
收盘价在中枢价之上
上下影线都不长且等长
第2周高开高走低开不能做
后期发力上攻
大阳线最低价止损

JGZS_KanZhangZuoZhang
'''

chengongs=[]
modelname='价格中枢-看涨做涨'

yangxianriqi=''


pathin = ''
pathout = ''
def get_all_JGZS_KanZhangZuoZhang(localpath1):
    info1=  '--上涨初期 价格中枢-看涨做涨 start-- '
    webhook.sendData( info1)
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST_tmp.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():

        stock_code = row['ts_code']

        # stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"

        try:
            df = pd.read_csv(stockdata_path, index_col=0)
            if (df.empty):
                continue

            df = df.reset_index(drop=False)  # 重新建立索引 ,
            data6_1 = df.iloc[0:8]  # 前6行
            # data6_1 = df.iloc[20:32]  # 前6行
            len1 = len(data6_1)
            isAn_JGZS_KanZhangZuoZhang_model(data6_1, stock_code)
        except:
            print  'stock_code is null = ' + str(stock_code)


'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_JGZS_KanZhangZuoZhang_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    global yangxianriqi
    global pathin
    global pathout

    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)
        riqi = data1.ix[1]['trade_date']  # 阳线的日期
        # yangxianriqi=riqi

        if(yangxianriqi == ''):

            yangxianriqi = covert_date(str(int(riqi)))  # %Y-%m-%d
            pathin = BASE_DIR + '/jishu_stock/JiaGeZhongShu/kanzhangzuozhang_huice/huicedata/2023/' + yangxianriqi + '.csv'
            pathout = BASE_DIR + '/jishu_stock/JiaGeZhongShu/kanzhangzuozhang_huice/huicedata/shouyi/' + yangxianriqi + '-shouyi.csv'



        # 设置两个 key

        key_1=0;  #1实体的1/2恰好是中枢价
        key_2=0; # 2收盘价 在中枢价之上
        key_3=0; # 3上下影线 都不会很长, 且等长 ,

        key_4=0; # 4 第 2 周 高开高走

        key_5=0; #第一周实体较大, 我这里大于 1 来测试一下
        key_6=0; #上下影线都不长, 比实体要小


        week1_zhongshujiage=0
        week1_shiti_yiban=0
        week1_close=0
        week1_xiayingxian=0
        week1_shangyingxian=0
        week2_open=0
        week1_shiti=0
        week1_open=0
        count=0
        for index, row in data1.iterrows():
            if(index==0 and isYangXian(row)==1):
                count=count+1
                week1_zhongshujiage=round((row['high']+row['low'])/2,2)
                week1_shiti_yiban=round((row['open']+row['close'])/2,2)
                week1_close=row['close']
                week1_open=row['open']
                week1_xiayingxian=row['open']-row['low']
                week1_shangyingxian=row['high']-row['close']
                week1_shiti=getShiTiDaXiao(row)
                zhisundian=row['low']



            if(index==1 and isYangXian(row)==1):
                count=count+1
                week2_open=row['open']
                mairuriqi=row['trade_date']


         # 0第一周第 2 周都是 阳线
        if(count ==2):
            #1实体的1/2恰好是中枢价
            week1_zhongshu_shitiyiban=abs(week1_zhongshujiage-week1_shiti_yiban)
            if(week1_zhongshu_shitiyiban < 0.1): # 案例 值 0.01,0.04,0.05,0.01
                key_1=1
            #2收盘价 在中枢价之上
            if(week1_close > week1_zhongshujiage):
                key_2=1
            #3 上下影线 都不会很长, 且等长 ,

            week1_xiayingxian= week1_xiayingxian+0.0001
            shangyingxian_xiayingxian= round(week1_shangyingxian /week1_xiayingxian ,2) # 上影线-下影线的绝对值
            if(  shangyingxian_xiayingxian< 1.51 and shangyingxian_xiayingxian > 0.5):
                key_3=1

            #4  第 2 周 刚开高走 的阳线.  周四买入也可以.
            gaokai = week2_open - week1_close
            # print1(gaokai)
            # if(  gaokai> -0.05 ):  # 案例中 最小的是一个是 - 0.01
            if(  gaokai >= - 0.02):  # 案例中 最小的是一个是 - 0.01
                key_4=1

            # 5 第一周实体较大, 我这里大于 1 来测试一下
            if (week1_shiti > 1):
                key_5 = 1

            # 6 上下影线都不长, 比实体要小

            tmp_week1 = week1_close - week1_open  # 这里的实体长度是纯 价格 因为下边一步 相除后就抵消了.
            week1_shangyingxian = week1_shangyingxian + 0.001  # 为了防止除数为 0
            # print1()
            shiti_yingxian_jibei = round(tmp_week1 / week1_shangyingxian, 2)
            if (shiti_yingxian_jibei > 2):  # 实体的长度 大于 上影线的长度
                key_6 = 1



        #
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)
        # print1(key_5)
        # print1(key_6)
        # print1(shiti_yingxian_jibei)
        # print1(shangyingxian_xiayingxian)


        # if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 ):
        if(key_1==1 and  key_2 ==1 and key_3==1  and key_4==1 and key_5==1 and key_6==1 ):
        #     print1(shangyingxian_xiayingxian)
            if (0):
                info = ''
                info = info + "--价格中枢看涨做涨--" + str(riqi)
                info=info+'价格中枢-实体一半=' +str(week1_zhongshu_shitiyiban)
                info=info+'--上影线是下的几倍=' +str(shangyingxian_xiayingxian)
                info=info+'--阳线实体=' +str(week1_shiti)
                info=info+'--实体是影线的几倍=' +str(shiti_yingxian_jibei)
                path = BASE_DIR + '/jishu_stock/zJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                    '%Y-%m-%d') + '.txt'
                jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)
                path = '价格中枢看涨做涨.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)
                chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
                chengongs.append(chenggong_code)

            from jishu_stock.aShengLv.HuiCeTool import get_oneweekOpenClosePrice_twoweekClose
                # print int(riqi)
            huice_info = get_oneweekOpenClosePrice_twoweekClose(stockcode, str(int(riqi)))
            # print huice_info
            # print '++++++++++++++================'

            writeLog_to_txt_path(huice_info, pathin);


def to_csv():
    global yangxianriqi
    global pathout
    global  pathin

    exced_csv_kanzhangjiegou(pathin,pathout,str(yangxianriqi))




'''
#2 单独一个函数 判断 6 个数据是不是符合模型 范围更大点


'''
def isAn_JGZS_KanZhangZuoZhang_model_pro(data,stockcode):
    # print stockcode
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 2):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,

        data1= data[len_data-2:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        # print data1
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)
        riqi = data1.ix[1]['trade_date']  # 阳线的日期




        # 设置两个 key

        key_1=0;  #1实体的1/2恰好是中枢价
        key_2=0; # 2收盘价 在中枢价之上
        key_3=0; # 3上下影线 都不会很长, 且等长 ,

        key_4=0; # 4 第 2 周 高开高走

        key_5=0; #第一周实体较大, 我这里大于 1 来测试一下
        key_6=0; #上下影线都不长, 比实体要小


        week1_zhongshujiage=0
        week1_shiti_yiban=0
        week1_close=0
        week1_xiayingxian=0
        week1_shangyingxian=0
        week2_open=0
        week1_shiti=0
        week1_open=0
        count=0
        for index, row in data1.iterrows():
            if(index==0 and isYangXian(row)==1):
                count=count+1
                week1_zhongshujiage=round((row['high']+row['low'])/2,2)
                week1_shiti_yiban=round((row['open']+row['close'])/2,2)
                # print int(row['trade_date'])
                # print '---------------'
                week1_close=row['close']
                week1_open=row['open']
                week1_xiayingxian=row['open']-row['low']
                week1_shangyingxian=row['high']-row['close']
                week1_shiti=getShiTiDaXiao(row)
                zhisundian=row['low']



            if(index==1 and isYangXian(row)==1):
                count=count+1
                week2_open=row['open']
                mairuriqi=row['trade_date']


         # 0第一周第 2 周都是 阳线
        if(count ==2):
            #1实体的1/2恰好是中枢价
            week1_zhongshu_shitiyiban=abs(week1_zhongshujiage-week1_shiti_yiban)
            if(week1_zhongshu_shitiyiban < 0.1): # 案例 值 0.01,0.04,0.05,0.01
                key_1=1
            #2收盘价 在中枢价之上
            if(week1_close > week1_zhongshujiage):
                key_2=1
            #3 上下影线 都不会很长, 且等长 ,

            week1_xiayingxian= week1_xiayingxian+0.0001
            shangyingxian_xiayingxian= round(week1_shangyingxian /week1_xiayingxian ,2) # 上影线-下影线的绝对值
            # print shangyingxian_xiayingxian
            if(  shangyingxian_xiayingxian< 2.51 and shangyingxian_xiayingxian > 0.5):
                key_3=1

            #4  第 2 周 刚开高走 的阳线.  周四买入也可以.
            gaokai = week2_open - week1_close
            # print1(gaokai)
            # if(  gaokai> -0.05 ):  # 案例中 最小的是一个是 - 0.01
            if(  gaokai >= - 0.02):  # 案例中 最小的是一个是 - 0.01
                key_4=1

            # 5 第一周实体较大, 我这里大于 1 来测试一下
            if (week1_shiti > 1):
                key_5 = 1

            # 6 上下影线都不长, 比实体要小

            tmp_week1 = week1_close - week1_open  # 这里的实体长度是纯 价格 因为下边一步 相除后就抵消了.
            week1_shangyingxian = week1_shangyingxian + 0.001  # 为了防止除数为 0
            # print1()
            shiti_yingxian_jibei = round(tmp_week1 / week1_shangyingxian, 2)
            if (shiti_yingxian_jibei > 2):  # 实体的长度 大于 上影线的长度
                key_6 = 1



        #
        if(0):
        # if(1):

            print1(key_1)
            print1(key_2)
            print1(key_3)
            print1(key_4)
            print1(key_5)
            print1(key_6)

        # print1(shiti_yingxian_jibei)
        # print1(shangyingxian_xiayingxian)


        # if(key_1==1 and  key_2 ==1 and key_3==1 and key_4==1 ):
        # if(key_1==1 and  key_2 ==1 and key_3==1  and key_4==1 and key_5==1 and key_6==1 ):
        # if(key_1==1 and  key_2 ==1 and key_3==1  and key_4==1 and key_5==1 ):
        if(key_1==1 and  key_2 ==1 and key_4==1 and key_5==1 ):

        #     print1(shangyingxian_xiayingxian)
            if(0):
                info = ''
                info = info + "--价格中枢看涨做涨--" + str(riqi)
                info=info+'价格中枢-实体一半=' +str(week1_zhongshu_shitiyiban)
                info=info+'--上影线是下的几倍=' +str(shangyingxian_xiayingxian)
                info=info+'--阳线实体=' +str(week1_shiti)
                info=info+'--实体是影线的几倍=' +str(shiti_yingxian_jibei)

                path = BASE_DIR + '/jishu_stock/zJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                    '%Y-%m-%d') + '.txt'
                # print stockcode
                jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)

                path = '价格中枢看涨做涨.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)

                chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
                chengongs.append(chenggong_code)

            from jishu_stock.aShengLv.HuiCeTool import get_oneweekOpenClosePrice_twoweekClose
            # print int(riqi)
            get_oneweekOpenClosePrice_twoweekClose(stockcode,str(int(riqi)))



'''
测试老师的案例
'''
def test_isAn_JGZS_KanZhangZuoZhang_laoshi():
    # 案例 1
    df = ts.pro_bar(ts_code='300157.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20200807')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_JGZS_KanZhangZuoZhang_model(data7_1, '300157.SZ')

    # 案例 2  得到的数据不对
    df = ts.pro_bar(ts_code='600089.SH', adj='qfq', freq='W', start_date='20170101', end_date='20201225')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_JGZS_KanZhangZuoZhang_model(data7_1, '600089.SH')

    # 案例 3 000155
    df = ts.pro_bar(ts_code='000155.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20201225')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_JGZS_KanZhangZuoZhang_model(data7_1, '000155.SZ')

    # 案例 4
    df = ts.pro_bar(ts_code='000409.SZ', adj='qfq', freq='W', start_date='20170101', end_date='20210226')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    isAn_JGZS_KanZhangZuoZhang_model(data7_1, '000409.SZ')



'''
测试自己的案例
'''
def test_isAn_JGZS_KanZhangZuoZhang_ziji():
    #自己的 案例
    #价格中枢-实体一半=0.04---上影线是下的几倍=1.33---阳线实体=7.26---实体看涨做涨--2021-10-31--维力医疗**603309.SH
    # df1 = ts.pro_bar(ts_code='603309.SZ',adj='qfq', start_date='20210206', end_date='20211008')
    stock_code = '000812.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    df = df.reset_index(drop=False)  # 重新建立索引 ,
    data7_1 = df.iloc[0:8]  # 前7行
    # isAn_JGZS_KanZhangZuoZhang_model(data7_1,'000812.SZ')


    # 案例 4  000426 xingyeyinxi
    stock_code = '000426.SZ'
    # df = ts.pro_bar(ts_code=tock_code, adj='qfq', freq='W', start_date='20170101', end_date='2024023')
    df = ts.pro_bar(ts_code=stock_code, adj='qfq', freq='W', start_date='20170101', end_date='20240315')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    # print data7_1
    # isAn_JGZS_KanZhangZuoZhang_model_pro(data7_1, stock_code)


    # 案例 4  gansu nengyuan
    stock_code = '000791.SZ'
    df = ts.pro_bar(ts_code= stock_code, adj='qfq', freq='W', start_date='20170101', end_date='20250526')
    data7_1 = df.iloc[0:100]  # 1 年有 50 周
    # isAn_JGZS_KanZhangZuoZhang_model_pro(data7_1, stock_code)

    #feiyada
    stock_code = '000026.SZ'
    df = ts.pro_bar(ts_code= stock_code, adj='qfq', freq='W', start_date='20231105', end_date='20240526')
    data1=df
    data1 = data1.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
    df = data1

    data7_1 = df.iloc[0:8]  # 1 年有 50 周
    print data7_1
    isAn_JGZS_KanZhangZuoZhang_model(data7_1, stock_code)


'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        # stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)
            # print df
        if (df.empty):
            continue

        df = df.reset_index(drop=False)  # 重新建立索引 ,
        data7_4 = df.iloc[8:10]  # 1 年有 52 周
        data7_4 = df.iloc[8:8+2+4]  # 上个与的

        len_1=len(data7_4)
        for i in range(0, len_1 - 2 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_JGZS_KanZhangZuoZhang_model(data7_4[i:i + 2], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)


'''

回测 2024-05 月份的数据
'''
def test_Befor_5_data():
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST_tmp.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/jiagezhongshu/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        # print stockdata_path
        # stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
        try:
            df = pd.read_csv(stockdata_path, index_col=0)
                # print df
            if (df.empty):
                continue

            df = df.reset_index(drop=False)  # 重新建立索引 ,
            data7_4 = df.iloc[8:10]  # 1 年有 52 周
            data7_4 = df.iloc[8:8+2+4]  # 上个与的
            data7_4 = df.iloc[1:8+1]  # 上个与的
            data7_4 = df.iloc[1:8+50]  # 上个与的
            n=12
            # n=19 CHUN JIE
            # n=0
            isAn_JGZS_KanZhangZuoZhang_model(data7_4[n:n+ 2], stock_code)
            #
            # for n in range(24,2,-1):
            #     isAn_JGZS_KanZhangZuoZhang_model(data7_4[n:n + 2], stock_code)
        except:
            print  'stock_code is null = ' + str(stock_code)



def huice_shouyi():
    test_Befor_5_data()
    to_csv()

if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/z_stockdata/data1/'


    # get_all_JGZS_KanZhangZuoZhang(localpath1)
    # test_isAn_JGZS_KanZhangZuoZhang_laoshi() #测试老师的案例
    # test_isAn_JGZS_KanZhangZuoZhang_ziji()
    # test_Befor_data()
    # jisuan_all_shouyilv(chengongs, modelname, 1.03)
    huice_shouyi()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"