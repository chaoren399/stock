#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.Tool_jishu_stock import writeLog_to_txt, isShangZhang_QuShi, writeLog_to_txt_nocode, \
    getRiQi_Befor_Ater_Days, print1, is_big_to_small

from stock.settings import BASE_DIR

'''

亢龙有悔 N字型上涨趋势


亢龙有悔 ,用在个股上 必须 是 上涨 趋势 , 如何 判断上涨趋势呢?

先把最近7 天的 数据拿到 最小值MIN7,  然后对比最近 30 天的数据做对比, 只要 min7  是最大的说明 这是一个上涨趋势
'''

count_sucess_2=0
count_kanglong=0
count_sucess_ma34=0
count_sucess_2_ma34=0

def getallstockdata_isKangLong_fromLocal(localpath1):
    info1="亢龙有悔 start "
    writeLog_to_txt_nocode(info1 )
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
                print "stock_code-----empty"
                break
                # 1 得到 第一个 7 交易日数据
                # iloc只能用数字索引，不能用索引名
            # data7_1 = df.iloc[0:3]  # 前7行
            data7_1 = df.iloc[10:32]  # 前7行
            # data7_1 = df.iloc[32:52]  # 前7行
            # data7_1 = df.iloc[52:74]  # 前7行
            # print data7_1


            len1 = len(data7_1)
            # print len1
            for i in range(0, len1 - 3 + 1):

                isAnKanglongyouhui_model_pro(data7_1[i:i + 3], stock_code)
    # print1(count_kanglong)
    # print1(count_sucess_2)
    print1(count_sucess_ma34)
    print1(count_sucess_2_ma34)
    print float(count_sucess_2_ma34)/float(count_sucess_ma34)


def isAnKanglongyouhui_model_pro(dataframe_df,stockcode):
    len1 = len(dataframe_df)
    # print len1
    for i in range(0,len1-3+1):
        # print "i" + str(i )+ "j"+str(i+3)
        # print dataframe_df[i:i+3]
        # isKanglongyouhui_3Days_data(dataframe_df[0:3])
        isKanglongyouhui_3Days_data(dataframe_df[i:i+3],stockcode)
        # isKanglongyouhui_3Days_data(dataframe_df[1:4])
        # isKanglongyouhui_3Days_data(dataframe_df[3:6]) # 真是的






''''
3 天的数据是不是满足 亢龙有悔的模型
'''
def  isKanglongyouhui_3Days_data(data3days,stockcode):
    data3days = data3days.reset_index(drop=True)  # 重新建立索引 ,
    # print data3days
    # print "122222"
    # print  data3days.ix[0][2]
    global count_kanglong
    global count_sucess_2
    global count_sucess_ma34
    global count_sucess_2_ma34

    if len(data3days) ==3 :

        #第一天 阴线
        day1open = data3days.ix[2]['open']
        day1close = data3days.ix[2]['close']
        day1riqi = data3days.ix[2]['trade_date']
        day1pct_chg = data3days.ix[2]['pct_chg']
        day1low= data3days.ix[2]['low']
        day1yinxian= day1close -  day1open

        # 第 2 天阴线

        day2open = data3days.ix[1]['open']
        day2close = data3days.ix[1]['close']
        day2pct_chg = data3days.ix[1]['trade_date']
        day2yinxian = day2close - day2open
        # print day2yinxian

        #第 3天 阳线

        day3open = data3days.ix[0]['open']
        day3close = data3days.ix[0]['close']
        day3pct_chg = data3days.ix[0]['trade_date']

        # print day3pct_chg
        day3yinxian = day3close - day3open
        # print day3yinxian
        riqi = data3days.ix[0][1]


        if(day1yinxian < 0 and day2yinxian <0 and day3yinxian>0):  # 阴 阴 阳
            if (day1yinxian > day2yinxian):  # 第一天小阴线  通过涨幅判断 是不是大阴线 比小阴线大  注意负值
                if (day3open < day2close and day3close < day2open and day3close > day2close):  # 阳线的开盘 低于 第 2 天阴线的收盘价 &  阳线 收盘价 小于第 2 天阴线的开盘
                    if (day1low > day2open):  # 跳空 第一天小阴线的 收盘价 必须要高于 第 2 天大阴线的开盘价
                        if(isShangZhang_QuShi(data3days) ==1 ):

                         #    info ="huice _阴阴阳--"+stockcode +"-----符合亢龙有悔--"+str(riqi)
                         #    info =stockcode +","+str(riqi)


                            count_kanglong=count_kanglong+1
                            info1=''
                            key1= is_sucess(stockcode,riqi)
                            if( key1 ==1):
                                count_sucess_2= count_sucess_2 + 1
                                info1='-大于 3%-'

                            info2=''
                            key2=ma34_is_shangzhang(stockcode,riqi)
                            if(key2==1):
                                info2='-ma34_is_shangzhang-'
                                # print 'ma34_is_shangzhang ---'
                                count_sucess_ma34=count_sucess_ma34+1

                            if(key1==1 and key2==1):
                                count_sucess_2_ma34 = count_sucess_2_ma34+1

                            info = "huice _阴阴阳--" + stockcode + "-----符合亢龙有悔--" + str(riqi) + info1+info2
                            print info
                            return 1


    return 0;

'''
计算赚了多少 

在后一天以开盘价买入, 如果 收益 3%  果断卖出, 如果没有大于 3% 的,那么就在第 10 天止损卖出.

这样计算一下, 能赚多少钱.
'''
def jisuan_zhuanleDuoShao(stockcode,start_date):
    return


def is_sucess(stockcode,start_date):

    start_date = getRiQi_Befor_Ater_Days(start_date, 1)
    end_date = getRiQi_Befor_Ater_Days(start_date, 20)
    # print start_date
    df = ts.pro_bar(ts_code=stockcode, start_date=start_date, end_date=end_date)
    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序
    df = df.reset_index(drop=True)  # 重新建立索引 ,
    df = df[0:5]
    # print df[0:5]
    # print stockcode
    if(len(df) > 0):

        day1_open= df.ix[0]['open']
        for index1, row1 in df.iterrows():
            day_close=row1['high']
            if(day_close >= day1_open*1.03):
                # print 'success'
                return 1
    return 0

def ma34_is_shangzhang (stockcode,start_date):

    start_date_7 = getRiQi_Befor_Ater_Days(start_date, -700)
    # print1(start_date_7)
    enddate= start_date

    df = ts.pro_bar(ts_code=stockcode, start_date=str(start_date_7), end_date=str(enddate), ma=[5, 13, 34])
    df= df [0:7]

    # print df
    if(len(df)>0):
        data1=[]
        for index, row in df.iterrows():
            data1.append(row['ma34'])


        if(is_big_to_small(data1)==1):
            return 1
    return 0



def test_ma34_is_shangzhang():

    # print  ma34_is_shangzhang('603185.SH','20210810')
    print  ma34_is_shangzhang('000503.SZ','20210831')

def test_isKanglongyouhui_3Days_data():
    stockcode= '000503.SZ'
    df = ts.pro_bar(ts_code=stockcode, start_date='20210827', end_date='20210831')
    isKanglongyouhui_3Days_data(df,stockcode)
    print1(count_kanglong)
    print1(count_sucess_2)

if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # anstock_isAnKanglongyouhui_model("300020.SZ",'20210701', '20210802')
    localpath1 = '/jishu_stock/stockdata/data1/'
    getallstockdata_isKangLong_fromLocal(localpath1)

    # test_isKanglongyouhui_3Days_data()
    # test_ma34_is_shangzhang()
    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds

    '''
    追求的 比较符合的 趋势
    '''