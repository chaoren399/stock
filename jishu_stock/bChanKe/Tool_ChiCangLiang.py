#!/usr/bin/python
# -*- coding: utf8 -*-

from jishu_stock.bChanKe.Tool_HuanShouLv import get_HuanshouLv
from jishu_stock.bChanKe.Tool_LiuTongShiZhi import get_oneStock_liutongshizhi

from jishu_stock.z_tool.PyDateTool import getDayNumberYMD, get_date_Befor_Ater_Days

'''
单独的 函数抽出来  判断 周线的数据是不是满足  持仓量的标准.

获取周线数据, 并判断是不是 符合10 周 一条线的标准


要求:  10 周内 有 7 周 可以用同一个价格买到 才可以叫做 主力控盘力度强


思路: 周线获取 10 个数据 ,x1,x2,x3....,  然后 找到 这 10 个数据的最大值与最小值 max0, min0 .

从最小值开始遍历到 最大值 步进为 0.01 ,   
例如,a1 ,  在 x1, 内, count= count +1
a1 在 x2 内, count= count +1  ...  如果 count >=7 ,满足条件 退出 . 否则继续循环. 
预计 空间为: 10 元里边有, 10*100 =1000 词循环.  OK


'''
def isAn_ChiCangLiang_BiaoZhun( stockcode,enddate):
    import time
    time.sleep(0.05)  # //睡觉
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
        riqi1 = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        # 设置两个 key
        key_1 = 0;  # 周数大于 6 的 开关



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
                        # if (count >= 6):  # 6个满足 神1 中路股份**600818.SH
                        if (count >= 7):  # 严格按照老师的条件 7 周 不然每天出来很多票
                            key_1 = 1


        if (key_1 == 1 ):

            if (1):
                info = ''
                info = info + "-持仓量"  +str(riqi) +'-'+str(riqi1)
                info = info + '-中间值'+str(zhongjianzhi_max)
                info = info + '--'+str(count_max) +'周'


                #换手率 的开始日期 要加上 5 天
                start_date=  get_date_Befor_Ater_Days(riqi, -5)
                end_date= riqi1
                turnover_rate_sum= get_HuanshouLv(stockcode,start_date,end_date)
                info = info + '-换手率,'+str(round(turnover_rate_sum,1))+'-'

                liutongshizhi = get_oneStock_liutongshizhi(stockcode)
                info = info + '流通市值,'+liutongshizhi

                # info = info + stockcode+ '--' + get_Stock_Name(stockcode)
                # global zhouxian_info
                # zhouxian_info= info
                # print  info


                bacinfo.append(key_1)
                bacinfo.append(info)

                return bacinfo
    return bacinfo

def test():
    stockcode = '002848.SZ' #--中间值=8.93--大于7个----换手率=111.5--002848.SZ--高斯贝尔
    today = getDayNumberYMD()
    bacinfo=isAn_ChiCangLiang_BiaoZhun(stockcode, today)
    print bacinfo[1]

if __name__ == '__main__':
    test()