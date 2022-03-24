#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from jishu_stock.Tool_jishu_stock import get_Stock_Name, print1, getRiQi_Befor_Ater_Days
from jishu_stock.bChanKe.Tool_HuanShouLv import get_HuanshouLv
from jishu_stock.z_tool.PyDateTool import getMonthNumber, getDayNumberYMD
from stock.settings import BASE_DIR
import pandas as pd
import tushare as ts
import time
'''
根据股票代码   判断 最近 10 周是不是符合 持仓量的标准.  过滤每天的 CSV文件


GetToday_ChiCangLiang_Week


'''

def GetToday_ChiCangLiang_Week():
    # 1.首先获取当天符合模型的代码
    yuefen = str(getMonthNumber())
    today= getDayNumberYMD()
    path1 = BASE_DIR + '/jishu_stock/sJieGuo/' + yuefen + '月/' + datetime.datetime.now().strftime(
        '%Y-%m-%d') + '.csv'

    df = pd.read_csv(path1, sep=',', header=None, engine='python')
    df.columns = ['modecode', 'modename','info']
    df = df.sort_values('modecode', ascending=True)
    # modename =
    for index,row in df.iterrows():
        info= row['info'] #--小树股票池--有钱君股票池**603259.SH'
        ss = info.split('**')
        # list.append(ss[1].rstrip('\n'))
        # print ss[1]
        time.sleep(0.3)  # //睡觉

        if(len(ss)==2):
            stockcode =ss[1]
            is_ChiCangliang_zhouxian(stockcode,today)



'''
获取周线数据, 并判断是不是 符合10 周 一条线的标准
'''
def is_ChiCangliang_zhouxian(stockcode,riqi):

    #2. 获取周线   我是希望通过 ts 在线获取, 这样比较方便,
    pro = ts.pro_api()
    # stockcode='000032.SZ'
    starttime = datetime.datetime.now()
    today = starttime.strftime('%Y%m%d')
    # riqi= '20220217'
    data = pro.weekly(ts_code=stockcode,start_date='20180101', end_date=riqi,
                     fields='ts_code,trade_date,open,high,low,close,vol,amount')

    data7_1 = data.iloc[0:100]  # 1 年有 50 周
    if(isAn_ChiCangLiang_ZhouXian_model_1(data7_1, stockcode)==1):
        return 1
    return 0

'''
单独的 判断 周线的数据是不是满足

'''
def isAn_ChiCangLiang_ZhouXian_model_1(data, stockcode):
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
        data1 = data[len_data - 10:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        riqi1 = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        data2 = data[len_data - 1:len_data]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1 = 0;  # 当天 收阳线  涨幅 6% 以上 的个股

        key_3 = 0; # 为了打印日志 区别 大于 7 的 哪些票子.

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

            zhongjianzhi=0
            zhongjianzhi_dayin = 0
            for item in list:
                zhongjianzhi = round(item,2)
                count = 0  # 计数 满足 大于 7 的个数
                # 遍历 10 个数据
                for index, row in data1.iterrows():
                    high = row['high']
                    low = row['low']
                    if(zhongjianzhi >=low  and zhongjianzhi <= high):
                        count=count+1
                    if(count>=6): #6个满足 神1 中路股份**600818.SH
                        key_1=1
                        zhongjianzhi_dayin = zhongjianzhi
                        # print zhongjianzhi
                        # print '---22--'+'count ='+str(count)

                    if(count >=7): # 为了打印日志 区别 大于 7 的 哪些票子.
                        key_3=1
                        zhongjianzhi_dayin = zhongjianzhi
                        break;
                # print '---count='+str(count)
                if(count>=7):  # 终止 外层的循环, 不然 中间值会继续 赋值 ,之前是 6,改成大于 7 比较合适, 否则 有些值到了 6 打印的会不显示
                    break



        # print1(key_1)

        if (key_1 == 1 ):

            if (1):
                info = ''
                info = info + "--持仓量_周线" +'开始=' +str(riqi) +'-结束='+str(riqi1)
                info = info + '--中间值='+str(zhongjianzhi_dayin)
                if(key_3==1):
                    info = info + '--大于7个--'
                    # print info

                #换手率 的开始日期 要加上 5 天
                start_date=  getRiQi_Befor_Ater_Days(riqi, -5)
                end_date= riqi1
                turnover_rate_sum= get_HuanshouLv(stockcode,start_date,end_date)
                info = info + '--换手率='+str(round(turnover_rate_sum,1))+'--'
                info = info + stockcode+ '--' + get_Stock_Name(stockcode)
                global zhouxian_info
                zhouxian_info= info
                print  info

                return 1
    return 0


def  get_onestock_isChiCangLiang():

    stockcode= '603229.SH' #--持仓量_周线开始=20211224-结束=20220304--中间值=34.3--大于7个----换手率100--603229.SH--奥翔药业
    stockcode= '603900.SH'
    stockcode= '000065.SZ' #-中间值=8.16--换手率100----北方国际**000065.SZ
    stockcode = '603969.SH'
    stockcode = '603969.SH' # -银龙股份--强势股票**603969.SH
    stockcode = '600814.SH' #- 神 1 -中间值=6.8--换手率=64.6--600814.SH--杭州解百
    stockcode = '600037.SH' #- 神 1 -中间值=8.25--大于7个----换手率=76.6--600037.SH--歌华有线
    stockcode = '002848.SZ' #
    today = getDayNumberYMD()
    is_ChiCangliang_zhouxian(stockcode, today)



if __name__ == '__main__':
    starttime = datetime.datetime.now()

    # GetToday_ChiCangLiang_Week()
    get_onestock_isChiCangLiang()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print str((endtime - starttime).seconds/60) + "分钟"