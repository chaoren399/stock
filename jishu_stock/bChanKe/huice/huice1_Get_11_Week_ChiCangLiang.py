# !/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.bChanKe.Tool_HuanShouLv import get_HuanshouLv
from jishu_stock.z_tool.PyDateTool import getDayNumberYMD, get_date_Befor_Ater_Days
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import hasXiongShiMoQi

from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
import pandas as pd

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''

找到 11 周的数据, 最后一周 放量的大阳线
下周观察, 也就是我们做的 周线, 不看日线. 这样可以吧




Next_11_Week_ChiCangLiang
'''
chengongs = []
modelname = '11周突破'


def get_all_Next_11_Week_ChiCangLiang(localpath1):
    info1 = '--11周突破 start--   '
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
        # isAn_ChouMaTuPo_model(data6_1, stock_code)

        today = getDayNumberYMD()

        isAn_ChiCangLiang_BiaoZhun_11_week(stock_code, today)


'''
单独过滤 换手率
'''


def isAn_ChiCangLiang_BiaoZhun_11_week(data, stockcode):


    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if (len_data >= 11):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1 = data[len_data -1- 10:len_data-1]
        # data1 = data[len_data - 10:len_data]  # 搞清楚 周线数据是否包含本周的, 在线获取的不包含本周
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        riqi1 = data1.ix[9]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        data2= data[len_data -1:len_data]   # 最新一周的数据
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # print1(data2)

        # 设置两个 key
        key_1 = 0;  # 周数大于 6 的 开关

        key_2=1; # 第 11 周的开盘价 大于 前 10 周的收盘价和开盘价
        key_3=0; # 第 11周是阳线
        key_4=1; # 第 11周是成交量放量

        # 单独判断 第 11 周的阳线, 是否放量等
        week_11_close = data2.ix[0]['close']
        week_11_vol = data2.ix[0]['vol']
        mairuriqi = data2.ix[0]['trade_date']

        if (isYangXian(data2.ix[0]) == 1):
            key_3 = 1

        for index, row in data1.iterrows():
            week_close = row['close']
            week_open = row['open']
            week_vol = row['vol']
            if (week_close > week_11_close or week_open > week_11_close):
                key_2 = 0
            if (week_vol > week_11_vol):
                key_4 = 0



        if(key_2==1 and key_3==1): # 把这步放到前边,可以减少下边的循环次数,节约时间

            # 换手率 的开始日期 要加上 5 天
            start_date = get_date_Befor_Ater_Days(riqi, -5)
            end_date = riqi1
            turnover_rate_sum = get_HuanshouLv(stockcode, start_date, end_date)

            # if (turnover_rate_sum < 110):
            if (turnover_rate_sum < 500):

                # 如果是周五就非常麻烦, 下周一下午,看看  能不能获取本周的数据. 如果不能,单独处理周五的数据.

                '''
                思路: 周线获取 10 个数据 ,x1,x2,x3....,  然后 找到 这 10 个数据的最大值与最小值 max0, min0 .
    
                从最小值开始遍历到 最大值 步进为 0.01 ,   
                例如,a1 ,  在 x1, 内, count= count +1
                a1 在 x2 内, count= count +1  ...  如果 count >=7 ,满足条件 退出 . 否则继续循环. 
                预计 空间为: 10 元里边有, 10*100 =1000 词循环.  OK
                '''

                if (1):  # 减少遍历的时间

                    # 1-找到 10 个数据的最大值 max0 最小值 min0
                    max0 = 0
                    min0 = 0
                    for index, row in data1.iterrows():
                        high = row['high']
                        low = row['low']
                        if (index == 0):
                            max0 = high
                            min0 = low
                            riqi = row['trade_date']
                        if (high > max0):
                            max0 = high
                        if (low < min0):
                            min0 = low

                        if (index == 9):
                            riqi1 = row['trade_date']
                    # 遍历 max0 min0
                    import numpy as np
                    list = np.arange(min0, max0, 0.01)

                    zhongjianzhi_dayin = 0
                    count_max = 0  # 统计 10 周内最多的的周数
                    zhongjianzhi_max = 0  # 统计 10 周内最多的的周数 对应的中间值
                    for item in list:
                        zhongjianzhi = round(item, 2)
                        count = 0  # 计数 满足 大于 7 的个数
                        # 遍历 10 个数据
                        for index, row in data1.iterrows():
                            high = row['high']
                            low = row['low']
                            if (zhongjianzhi >= low and zhongjianzhi <= high):
                                count = count + 1
                                if (count > count_max):
                                    count_max = count
                                    zhongjianzhi_max = zhongjianzhi
                                if (count >= 7):  # 6个满足 神1 中路股份**600818.SH
                                    key_1 = 1

                zhisundian = zhongjianzhi_max
                if(0):
                    print1(key_1)
                    print1(key_2)
                    print1(key_3)
                    print1(key_4)
                    print1(count_max)

                # if (key_1 == 1 and key_2==1 and key_3==1 ):
                if (key_1 == 1 and key_2==1 and key_3==1 and key_4==1):

                    if (1):
                        info = ''
                        info = info + "--11周突破_周线" + '开始=' + str(riqi) + '-结束=' + str(riqi1)
                        info = info + '--中间值=' + str(zhongjianzhi_max)
                        info = info + '--周数=' + str(count_max)

                        info = info + '--换手率=' + str(round(turnover_rate_sum, 1)) + '--'
                        # info = info + stockcode + '--' + get_Stock_Name(stockcode)
                        # print  info

                        path = BASE_DIR + '/jishu_stock/zJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                            '%Y-%m-%d') + '.txt'

                        jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)

                        path = '11周突破.txt'
                        writeLog_to_txt_path_getcodename(info, path, stockcode)

                        # chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian}
                        chenggong_code = {'stockcode': stockcode, 'mairuriqi': mairuriqi, 'zhisundian': zhisundian,'info':info}
                        # print1(day2_shizixing_low)
                        chengongs.append(chenggong_code)

'''
测试 之前做过的神 1 案例
'''
def test_shen1_old():

    # 神 1 案例;

    # 案例8 -中间值=3.93--周数=9--换手率=48.8----冀中能源 -000937.SZ**000937.SZ

    isAn_ChiCangLiang_BiaoZhun_11_week('000937.SZ', '20210806')
    # 案例9  -中间值=8.34--周数=7--换手率=58.0----code_name is null-600058.SH**600058.SH
    isAn_ChiCangLiang_BiaoZhun_11_week('600058.SH', '20210806')
    # 案例10  -中间值=13.14--周数=6--换手率=40.9----国网信通**600131.SH
    isAn_ChiCangLiang_BiaoZhun_11_week('600131.SH', '20210806')

    # 案例11 --中间值=14.66--周数=10--换手率=39.0----北京城乡**600861.SH
    isAn_ChiCangLiang_BiaoZhun_11_week('600861.SH', '20210611')
    # 案例12 --中间值=15.6--周数=10--换手率=80.1----上海亚虹**603159.SH
    isAn_ChiCangLiang_BiaoZhun_11_week('603159.SH', '20210910')








    # 案例8

def test():
    # 案例 1 中路股份  600818
    isAn_ChiCangLiang_BiaoZhun_11_week('600818.SH', '20220114')

    # 案例 2 中间值=20.16--周数=8--换手率=185.1--002935.SZ--天奥电子--天奥电子--强势股票**002935.SZ
    isAn_ChiCangLiang_BiaoZhun_11_week('002935.SZ', '20210910')
    # 案例 3: --中间值=14.1--周数=9--换手率=55.7----code_name is null-600452.SH**600452.SH
    isAn_ChiCangLiang_BiaoZhun_11_week('600452.SH', '20210813')

    # 案例4 中间值=9.11--周数=9--换手率=41.0----沐邦高科**603398.SH
    isAn_ChiCangLiang_BiaoZhun_11_week('603398.SH', '20210827')


    # 案例5  岱美股份 , 持仓量 不符合要求 --中间值=16.88--周数=8--换手率=9.0----code_name is null-603730.SH**603730.SH
    isAn_ChiCangLiang_BiaoZhun_11_week('603730.SH', '20211015')
    # 案例6  -中间值=9.84--周数=6--换手率=55.1----神力股份**603819.SH
    isAn_ChiCangLiang_BiaoZhun_11_week('603819.SH', '20211022')
    # 案例7  -中间值=4.83--周数=6--换手率=58.2----泸天化**000912.SZ
    isAn_ChiCangLiang_BiaoZhun_11_week('000912.SZ', '20210827')


'''
回测 8 月份的数据
'''
def test_Befor_data():


    # 2. 获取周线   我是希望通过 ts 在线获取, 这样比较方便,
    import tushare as ts
    pro = ts.pro_api()
    # stockcode='000032.SZ'

    # enddate= '20220217'
    enddate=getDayNumberYMD()



    # path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST-1.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        # stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        # df = pd.read_csv(stockdata_path, index_col=0)

        data = pro.weekly(ts_code=stock_code, start_date='20180101', end_date=enddate,
                          fields='ts_code,trade_date,open,high,low,close,vol,amount')

        df = data.iloc[0:100]  # 1 年有 50 周


        n = 11  # 模型需要最低的数据
        # data7_4 = df.iloc[22:22 + n + 5]  # 前1个月个交易日
        data7_4 = df.iloc[22:22 + n + 22]  # 1 个月
        # data7_4 = df.iloc[22:22 + n + 120]  # 半年
        # data7_4 = df.iloc[22:22+n+250]  # 1年

        len_1 = len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ChiCangLiang_BiaoZhun_11_week(data7_4[i:i + n], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.HuiCeTool import getList_from_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    # jisuan_all_shouyilv(chengongs, modelname, 1.03)
    # jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.20)
    jisuan_all_shouyilv(chengongs, modelname, 1.30)

# 冀中能源 市值 大于 100 亿 ,没有在 股票池中 可以扩大到 150 亿

#--11周突破_周线开始=20211224-结束=20220304--中间值=3.63--周数=9--换手率=29.6----合兴包装**002228.SZ
if __name__ == '__main__':
    from time import *

    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    # get_all_Next_11_Week_ChiCangLiang(localpath1)
    # test_shen1_old()
    test_Befor_data()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"