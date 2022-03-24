#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import exceptions

import tushare as ts
import pandas as pd
from time import *
from jishu_stock.Tool_jishu_stock import *
from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
from jishu_stock.bChanKe.Tool_HuanShouLv import get_HuanshouLv
from jishu_stock.bChanKe.Tool_LiuTongShiZhi import get_oneStock_liutongshizhi
from jishu_stock.z_tool.PyDateTool import getDayNumberYMD, get_date_Befor_Ater_Days
from stock.settings import BASE_DIR
from jishu_stock.z_tool.ShiTiDaXiao import *
from jishu_stock.z_tool.isXiongShiMoQi import  hasXiongShiMoQi

from jishu_stock.z_tool.isZhangTingBan import isZhangTingBan
import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
得到下周 所有符合  10 周 的 数据, 下周来观察.

NextWeek_ChiCangLiang
'''
chengongs=[]
modelname='下周持仓量'

def get_all_NextWeek_ChiCangLiang(localpath1):
    info1=  '--下周持仓量 start--   '
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

        isAn_ChiCangLiang_BiaoZhun_dandu( stock_code,today)




'''
单独过滤 换手率
'''

def isAn_ChiCangLiang_BiaoZhun_dandu( stockcode,enddate):
    # 2. 获取周线   我是希望通过 ts 在线获取, 这样比较方便,
    import tushare as ts
    pro = ts.pro_api()
    # stockcode='000032.SZ'

    # enddate= '20220217'
    data = pro.weekly(ts_code=stockcode, start_date='20180101', end_date=enddate,
                      fields='ts_code,trade_date,open,high,low,close,vol,amount')

    data = data.iloc[0:100]  # 1 年有 50 周

    bacinfo = []

    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if (len_data >= 10):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        # data1 = data[len_data -1- 10:len_data-1]
        data1 = data[len_data - 10:len_data]   # 搞清楚 周线数据是否包含本周的, 在线获取的不包含本周
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        riqi1 = data1.ix[9]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        # 设置两个 key
        key_1 = 0;  # 周数大于 6 的 开关

        # 换手率 的开始日期 要加上 5 天
        start_date = get_date_Befor_Ater_Days(riqi, -5)
        end_date = riqi1
        turnover_rate_sum = get_HuanshouLv(stockcode, start_date, end_date)

        if (turnover_rate_sum < 110):



            # 如果是周五就非常麻烦, 下周一下午,看看  能不能获取本周的数据. 如果不能,单独处理周五的数据.

            '''
            思路: 周线获取 10 个数据 ,x1,x2,x3....,  然后 找到 这 10 个数据的最大值与最小值 max0, min0 .
    
            从最小值开始遍历到 最大值 步进为 0.01 ,   
            例如,a1 ,  在 x1, 内, count= count +1
            a1 在 x2 内, count= count +1  ...  如果 count >=7 ,满足条件 退出 . 否则继续循环. 
            预计 空间为: 10 元里边有, 10*100 =1000 词循环.  OK
            '''


            if(1 ): #减少遍历的时间

                #1-找到 10 个数据的最大值 max0 最小值 min0
                max0=0
                min0=0
                for index, row in data1.iterrows():
                    high = row['high']
                    low = row['low']
                    if(index==0):
                        max0= high
                        min0= low
                        riqi=row['trade_date']
                    if(high > max0):
                        max0=high
                    if(low < min0):
                        min0=low

                    if(index==9):
                        riqi1 = row['trade_date']
                #遍历 max0 min0
                import numpy as np
                list = np.arange(min0, max0, 0.01)


                zhongjianzhi_dayin = 0
                count_max=0 # 统计 10 周内最多的的周数
                zhongjianzhi_max=0 # 统计 10 周内最多的的周数 对应的中间值
                for item in list:
                    zhongjianzhi = round(item,2)
                    count = 0  # 计数 满足 大于 7 的个数
                    # 遍历 10 个数据
                    for index, row in data1.iterrows():
                        high = row['high']
                        low = row['low']
                        if(zhongjianzhi >=low  and zhongjianzhi <= high):
                            count=count+1
                            if(count > count_max):
                                count_max =count
                                zhongjianzhi_max=zhongjianzhi
                            if (count >= 6):  # 6个满足 神1 中路股份**600818.SH
                                key_1 = 1


            if (key_1 == 1 ):

                if (1):
                    info = ''
                    info = info + '10周持仓量_周线' +'开始=' +str(riqi) +'-结束='+str(riqi1)
                    info = info + '--中间值='+str(zhongjianzhi_max)
                    info = info + '--周数='+str(count_max)

                    info = info + '--换手率,'+str(round(turnover_rate_sum,1))+'--'

                    liutongshizhi = get_oneStock_liutongshizhi(stockcode)
                    info = info + '流通市值,' + liutongshizhi

                    # info = info + stockcode+ '--' + get_Stock_Name(stockcode)
                    # print  info

                    path = BASE_DIR + '/jishu_stock/sJieGuo/JiaGeZhongShu/' + datetime.datetime.now().strftime(
                        '%Y-%m-%d') + '.txt'

                    jiagezhongshu_writeLog_to_txt_path_getcodename(info, path, stockcode)

                    path = '10周持仓量.txt'
                    writeLog_to_txt_path_getcodename(info, path, stockcode)






if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_NextWeek_ChiCangLiang(localpath1)


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"