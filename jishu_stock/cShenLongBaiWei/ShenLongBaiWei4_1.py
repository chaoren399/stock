#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, writeLog_to_txt_nocode, getRiQi_Befor_Ater_Days, print1, \
    writeLog_to_txt_path_getcodename
from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.aShengLv.huice.ShengLv_10_5 import jisuan_all_shouyilv_10_5
from stock.settings import BASE_DIR


'''
神龙摆尾 4_1  ,成交量 改为 vol 之前的都是 amount 搞错了

https://www.yuque.com/chaoren399/eozlgk/fkbnbi

下跌横盘缓慢上涨
涨幅5%左右的放量中阳线 且成为近期高点
之后横盘或下跌调整10个交易日以内
之后再次放量阳线
创之前阳线的新高且成交量更大


思路:

, 先确定 2 个数组:  10 : 10 

找到 最后一个是 近期的最大值,
然后往循环找 9 个值, 判断有没有 大于 5% 的值

如果有大于%5 的, 判断 后边的 10+X的收盘价是不是 都小于这个 5%的收盘价.
如果不是,继续往下循环, 再找 大于 5% 值,继续判断.

'''

chengongs=[]
modelname='神4_1'
def get_all_ShenLongBaiWei4_1(localpath1):
    info1= "神龙摆尾4_1  下跌横盘缓慢上涨 66 且 3 个月内最大值  start "
    writeLog_to_txt_nocode(info1)

    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    # print "ssss"
    # print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']

        if (1):

            stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
            # df =  pd.read_csv(stockdata_path, dtype={'code': str})
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                return
                # 1 得到 第一个 7 交易日数据
                # iloc只能用数字索引，不能用索引名
            data7_1 = df.iloc[0:20]  # 前10个交易日
            # data7_1 = df.iloc[40:60]  # 前10个交易日
            # data7_1 = df.iloc[1:21]  # 前10个交易日
            # data7_1 = data7_1.reset_index(drop=True)  # 重新建立索引 ,
            # print data7_1
            # 2 单独一个函数 判断是不是符合  神龙摆尾
            isyes = isAn_ShenLongBaiwei4_1_model_pro(data7_1, stock_code)



def  isAn_ShenLongBaiwei4_1_model_pro(dataframe_df,stock_code):

    #这次数据是最新日期为 0 倒序排列的

    len_df= len(dataframe_df)
    if(len_df>10):
        dataframe_df = dataframe_df.reset_index(drop=True)  # 重新建立索引 ,
        maxclose = dataframe_df.ix[0]['close']

        day1_amount=dataframe_df.ix[0]['vol']
        day1_open=dataframe_df.ix[0]['open']
        day1_close=dataframe_df.ix[0]['close']

        day1_pct_chg=dataframe_df.ix[0]['pct_chg'] # 第一天的 涨幅
        riqi_0 =dataframe_df.ix[0]['trade_date']
        mairuriqi=riqi_0
        zhisundian=0
        # riqi ='20210901'
        key_0=0 #  第一天的 涨幅 不能是 涨停板
        key_1 = 1#  确定 条件 最新一天的值是不是放量, 并且是最近的最大值.
        key_2 = 0  #  5%阳线 前一天的成交量  确定条件 5% 放量
        key_3 = 0  # 第 2 个放量 要比第一个 5%中阳线 要大 ,且控制在 10 个交易日内

        key_4=0 # 5%阳线收盘价 是近期的最大值 需要一个单独的函数处理:


        # 第一步:  排除 涨停板(实测过程中, 涨停板 失败概率很大)
        if(day1_pct_chg < 9.8 and  day1_open <  day1_close):
            key_0=1

        # 第 二步: 第一次循环 确定 条件 最新一天的值是不是放量, 并且是最近的最大值.

        for index, row in dataframe_df.iterrows():
            if(index >0):
                zhisundian = row['low']
                if(row['close'] > maxclose or row['open'] > maxclose): # 有效突破
                    key_1=0
                    # print row['trade_date']

                    return

            if(index==1):

                if( row['vol'] > day1_amount):
                    key_1=0


                    return

        #第三步  第 2 次循环 确定条件 5% 放量  需要 2 个 key , key_2 ,key_3




        data1 = dataframe_df[1:len_df]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        count=0
        # print data1
        close_price=0
        for index1, row1 in data1.iterrows():
            count= count+1
            # if (count > 1 and count <9):  # 然后往循环找 9 个值, 判断有没有 大于 5% 的值
            if (count >= 4 and count <=9):  # 然后往循环找 9 个值, 判断有没有 大于 5% 的值
                pct_chg = row1['pct_chg']
                # zhisundian = row1['open']

                if (pct_chg >= 3.9 and pct_chg < 7.5):  # 5% 左右
                    riqi=row1['trade_date']
                    close_price=row1['close']
                    key_3 = 0  # 因为有 2 次或者多次 满足5% 的时候 , 有的会混乱
                    key_2 = 0
                    #前一天的 amount
                    data1_day2_amount= data1.ix[count]['vol']
                    if(row1['vol'] < day1_amount): #  第 2 个放量 要比第一个 5%中阳线 要大
                        key_3=1

                        # print row1['amount']
                        # print day1_amount
                        # print data1_day2_amount
                        # print riqi

                    if(data1_day2_amount < row1['vol']): #前一天的成交量 小
                        key_2=1
                        # print row1['trade_date']



        # key3=0
        # riqi_0 - riqi >3
        # print key_2
        # print1(key_0)
        # print1(key_1)
        # print1(key_2)
        # print1(key_3)
        # print1(key_4)

        if(key_0==1 and key_1==1 and key_2==1 and key_3==1):

            #第 4 步: 判断 5% 阳线是不是近期最大值 非常关键:

            if(is_max_in_20days(stock_code, riqi, close_price) ==1):
                key_4 =1

            if(key_4==1):

                info = "--------- 神4_1---------" + str(riqi)+'--'+str(riqi_0)

                # 统一 info管理 一个函数,每次都要执行, 并且信息 返回后,要添加到 info中,
                # 方便后期修改,这样一改,所有的都可以执行了.
                from jishu_stock.z_tool.InfoTool import manage_info
                manage_info = manage_info(info, stock_code, riqi, '')
                info = info + manage_info

                # print  info
                writeLog_to_txt(info, stock_code)

                path = '神4_1.txt'
                writeLog_to_txt_path_getcodename(info, path, stock_code)

                chenggong_code = {'stockcode': stock_code, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
                chengongs.append(chenggong_code)

'''
判断 前 66 天 的最高价 是不是 低于 某个值
'''
def  is_max_in_20days(stock_code,riqi,close_price):

    start_date= getRiQi_Befor_Ater_Days(riqi,-66)#近 20 天 是最大值
    end_date=getRiQi_Befor_Ater_Days(riqi,-1) # %5 前一天的日期
    # print1 (riqi)
    # print1 (stock_code)
    # print1 (close_price)

    df = ts.pro_bar(ts_code=stock_code, start_date=start_date, end_date=end_date)
    # print df

    for index,row in df.iterrows():
        high = row['close']
        if(high > close_price):
            return 0
    return 1

    # print df

def test_is_max_in_20days():
    stock_code= '000722.SZ'
    riqi='20210910'
    close_price=7.67
    print is_max_in_20days(stock_code, riqi, close_price)

def test_isAn_ShenLongBaiwei4_1_model_form_ts():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    df1 = ts.pro_bar(ts_code='600114.SH', start_date='20210617', end_date='20210720')
    data7_1 = df1.iloc[0:20]  # 前10个交易日
    isAn_ShenLongBaiwei4_1_model_pro(data7_1, '600114.SH')

    df2 = ts.pro_bar(ts_code='000504.SZ', start_date='20210317', end_date='20210510')
    data7_2 = df2.iloc[0:20]  # 前10个交易日
    isAn_ShenLongBaiwei4_1_model_pro(data7_2, '000504.SZ')

    df3 = ts.pro_bar(ts_code='600054.SH', start_date='20210117', end_date='20210218')
    data7_3 = df3.iloc[0:20]  # 前10个交易日
    isAn_ShenLongBaiwei4_1_model_pro(data7_3, '600054.SH')

    df4 = ts.pro_bar(ts_code='600085.SH', start_date='20210417', end_date='20210514')
    data7_4 = df4.iloc[0:20]  # 前10个交易日
    isAn_ShenLongBaiwei4_1_model_pro(data7_4, '600085.SH')





def test_isAn_ShenLongBaiwei4_1_model():
    localpath1 = '/jishu_stock/stockdata/data1/'
    # stock_code ='000520.SZ'
    # stock_code ='002247.SZ'
    stock_code ='000519.SZ'
    # stock_code ='000001.SZ'
    stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
    # stockdata_path = BASE_DIR + localpath1 + '000520.SZ' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    # print df

    data7_1 = df.iloc[0:20]  # 前10个交易日
    isAn_ShenLongBaiwei4_1_model_pro(data7_1,stock_code)



def test_ziji():
    #002275  三元股份 ,君正集团

    df4 = ts.pro_bar(ts_code='600429.SH', start_date='20210417', end_date='20220207')
    data7_4 = df4.iloc[0:20]  # 前10个交易日
    isAn_ShenLongBaiwei4_1_model_pro(data7_4, '600429.SH')
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


        data7_4 = df.iloc[22:42]  # 前10个交易日
        # data7_4 = df.iloc[22:22+20+5]  # 前10个交易日
        data7_4 = df.iloc[22:22+20+22]  # 1 个月
        # data7_4 = df.iloc[22:22+20+120]  #半年

        len_1=len(data7_4)

        for i in range(0, len_1 - 20 + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ShenLongBaiwei4_1_model_pro(data7_4[i:i + 20], stock_code)

    wirteList_to_txt(chengongs)

    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    # jisuan_all_shouyilv(chengongs, modelname, 1.15)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    # jisuan_all_shouyilv(chengongs, modelname, 1.30)

    jisuan_all_shouyilv_10_5(chengongs, modelname, 1.10, 0.95)
    jisuan_all_shouyilv_10_5(chengongs, modelname, 1.20, 0.90)


'''
测试一只股票 历史数据 符合神 4 的 位置
'''
def test_onestock_olddata():
    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()
    stock_code = '002486.SZ'
    df = ts.pro_bar(ts_code=stock_code, start_date='20200617', end_date='20220129')

    stock_code = '601216.SH'
    df = ts.pro_bar(ts_code=stock_code, start_date='20200530', end_date='20200830')
    print  df.iloc[0:2]


    data7_4 = df.iloc[0:52]  # 前10个交易日
    # data7_4 = df.iloc[22:22+20+5]  # 前10个交易日
    # data7_4 = df.iloc[22:22 + 20 + 22]  # 1 个月
    # data7_4 = df.iloc[22:22+20+120]  #半年

    len_1 = len(data7_4)

    for i in range(0, len_1 - 20 + 1):
        # print "i" + str(i )+ "j"+str(i+3)
        isAn_ShenLongBaiwei4_1_model_pro(data7_4[i:i + 20], stock_code)

if __name__ == '__main__':
    from  time import  *
    starttime = time()

    # getallstockdata_isShenLongBaiWei('20210701', '20210805')
    # anstock_isShenLongBaiWei_model('000539.SZ','20210701', '20210805')
    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_ShenLongBaiWei4_1(localpath1)
    # test_isAn_ShenLongBaiwei4_1_model_form_ts()
    # test_isAn_ShenLongBaiwei4_1_model()
    # test_is_max_in_20days()
    # test_Befor_data()
    # test_onestock_olddata()
    # test_ziji()
    # jisuan_all_shouyilv(chengongs, modelname, 1.05)

    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"
