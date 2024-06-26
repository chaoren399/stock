#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import pandas as pd
import tushare as ts

from jishu_stock.RiQi_Zhuanhuan import Y_D_M_To_YMD
from jishu_stock.Tool_jishu_stock import isInQiangShi_gupiaochi, get_Stock_Name
from stock.settings import BASE_DIR

'''
葛式八法 买 1  回测 程序  

间隔 60 天 的收益 10% 的成功率


第一步 : 用  Get_Week_K_data.py 来 得到 周K 线
第二步:   计算 10 周K 线 和 60 周K 线, 葛式八法 需要的
第三步: 找到 葛式八法的点位  ,,Week60-10 差值 只要小于 0.1 说明很接近了.  

G2 其实我们找到 最近 2 个数据的差值大小. 

改进一下  , 先不判断 趋势,先确定点位 2021年08月31日  还没改, 改完后 删除

trade_date,open,close,high,low,WeekMa10,WeekMa60,Week60-10
2021-03-28,20.55,21.14,21.65,20.4,22.452999999999992,16.50683333333334,-5.946166666666652



'''

count_isG8=0
count_isDayu10_baifen=0
def getallstockdata_is_GeShi_8fa():
    print '------start 葛式八法---'
    # path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST-1.csv'
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    if(len(data)>0):

        # print len(data)
        # print '1111111'
        for index, row in data.iterrows():
            stock_code = row['ts_code']
            stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
            df = pd.read_csv(stockdata_path, index_col=0)
            # print df
            if (df.empty):
                continue

            # df=df.iloc[0:6]  # 把前 2 周的数据保留, 我只要找到 合适得买点   前3行 最近 3 周的数据
            # df=df.iloc[4:8]  # 测试  上个月的数据 7 月份
            df=df.iloc[8:12]  # 测试  上个月的数据 6 月份
            # df=df.iloc[12:18]  # 测试  上个月的数据  5月份

            # 再找到 慢速 60 周均线明显 上涨的,
            isAn_GEShi8_model(df, stock_code)
            count = count + 1
            # print count
    print 'count_isG8='+str(count_isG8 )
    print 'count_isDayu10_baifen='+str(count_isDayu10_baifen )
    print 'count_isG8/count_isDayu10_baifen='+str(count_isG8/count_isDayu10_baifen )

def isAn_GEShi8_model(data,stock_code):
    global count_isG8
    global count_isDayu10_baifen

    if(len(data) > 3):
        # 传给我 1 个月数据  我
        # 把前 2 周的数据拿出来, 作为 判断 60日均线的依据
        data1 = data.iloc[0:1]
        week60LastK = data1.ix[0]['WeekMa60']
        # print  data1
        # print '------'

        data = data.iloc[2:10]  # 真正的 相交的点是从第 2 个开始的
        data = data.reset_index()  # 重新建立索引 ,
        # print data
        riqi =data.ix[0]['trade_date']
        #1 选出 最小值
        mini =abs(data.ix[0]['Week60-10'])
        for index, row in data.iterrows():
            Week60_10 = abs(row['Week60-10'])
            if(Week60_10<mini):
                mini = Week60_10
                riqi = row['trade_date']
        #2 判断日期是近一个月

        from datetime import datetime, timedelta
        today = datetime.now().strftime('%Y-%m-%d')

        today = datetime(int(today[0:4]), int(today[5:7]), int(today[8:10]))
        today_30 = today + timedelta(days=-30)
        today_30= str(today_30)
        # print today_30
        next_day = datetime(int(today_30[0:4]), int(today_30[5:7]), int(today_30[8:10]))
        # cur_day = datetime(2021, 04, 18)

        cur_day= datetime(int(riqi[0:4]),int(riqi[5:7]), int(riqi[8:10]))


        # 3 判断 慢线是上涨趋势  起码近 2 个月,也就是 前 8 个数据
        # 快线 也是 上涨趋势,

        Week60_last = data.ix[0]['WeekMa60'] #week60LastK

        WeekMa60_max = data.ix[0]['WeekMa60']
        isBigThanWeekMa60 =1

        WeekMa10_max = data.ix[0]['WeekMa10']
        isBigThanWeekMa10 = 1

        data_10 = data[0:20]
        for index, row in data_10.iterrows():
            # print index

            if(row['WeekMa60'] > WeekMa60_max):
                isBigThanWeekMa60=0
            if(row['WeekMa10'] > WeekMa10_max):
                isBigThanWeekMa10=0


        #  Week60-10 差值 只要小于 0.1 说明很接近了.
        # if(mini < 0.1 and (cur_day - next_day).days < 30  and (cur_day - next_day).days > 0 and
        # isBigThanWeekMa60 ==1 and isBigThanWeekMa10==1):
        if(mini < 0.1 and isBigThanWeekMa60 ==1 and isBigThanWeekMa10==1):

            if(week60LastK- Week60_last > 0.1) : # 60日 周线明显上涨的 可以调节 0.01 的大小来控制 60 线的上涨趋势
                count_isG8 = count_isG8 +1
                info = stock_code  + "--------- 葛式八法--------" + str(riqi)+ "---mini--"+str(mini)
                path = BASE_DIR + '/jishu_stock/zJieGuo/G8/9/' + datetime.now().strftime(
                    '%Y-%m-%d') + '-G8.txt'
                if (isInQiangShi_gupiaochi(stock_code)):
                    info = info + '--强势股票--'
                info = info + '--' + get_Stock_Name(stock_code)
                print info
                with open(path, "a") as f:
                    f.write(info + '' + "\n")
                # 统计 正确率

                isdayu10_Bafifen=  getZhengquelv_with_code_date(stock_code,riqi) #间隔 60 天
                if(isdayu10_Bafifen ==1):
                    count_isDayu10_baifen= count_isDayu10_baifen+1


''''

先获取 G8 买 1 的 日期,以后的数据, 然后 找到 大于开盘价 1.1 倍的 数据

间隔 60 天
'''
def getZhengquelv_with_code_date(stock_code,start_date):
    start_date=Y_D_M_To_YMD(start_date)
    end_date=getRiQi_Ater_Days(start_date,70)  # 间隔 60 天
    df = ts.pro_bar(ts_code=stock_code, start_date=start_date, end_date=end_date)
    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从新到旧 排序
    df = df.reset_index(drop=True)  # 重新建立索引 ,
    # print df
    if(len(df) >0):
        high_price = df.ix[0]['open'] * 1.1  # 10% 的收益率
        for index1, row1 in df.iterrows():
            if (row1['high'] > high_price):
                high_price_riqi = row1['trade_date']
                return 1

    return 0


'''
2021-05-16
'''
def getRiQi_Ater_Days(date,numdays):
    day1riqi = str(date)
    # print day1riqi
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    result_date = cur_day + datetime.timedelta(days=numdays)
    try:
        result_date = result_date.strftime('%Y%m%d')
    except Exception as e:
        print e


    return result_date
def test_one_stock_is_GeShi_8fa():
    stock_code='000001.SZ'
    stockdata_path = BASE_DIR + '/jishu_stock/z_stockdata/WEEK_DATA_K/' + stock_code + '_Week' + ".csv"
    df = pd.read_csv(stockdata_path, index_col=0)
    # print df

    isAn_GEShi8_model(df, stock_code)

if __name__ == '__main__':

    localpath1 = '/jishu_stock/z_stockdata/data1/'
    # getAllWeekKdata(localpath1)  #更新数据的时候可以打开 可以每周更新一次

    getallstockdata_is_GeShi_8fa()
    # test_one_stock_is_GeShi_8fa()
