#!/usr/bin/python
# -*- coding: utf8 -*-

from jishu_stock.Tool_jishu_stock import *
from jishu_stock.agetdata.liutongshizhi.LiuTongShiZhi import get_oneStock_LTSZ, LTSZ_IS_Small_100YI
from jishu_stock.bChanKe.HuanShouLv import get_HuanshouLv
from jishu_stock.z_tool.ShiTiDaXiao import *

import pandas as pd
# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

''''
想法: 过滤当天 创新高的个股 市值在 100 亿以下,的小盘股, 然后收阳线涨幅在 6%以上. 
 
然后实盘几个案例. 加深印象.  主要是辅助 找到 持仓量 黑马股-周线
当汽车 出现违规的时候交警才 注意他. 

https://www.yuque.com/chaoren399/eozlgk/vg3ik9 案例:

https://www.yuque.com/chaoren399/eozlgk/crt2n4

23-（2）筹码突破-案例讲解

ChouMaTuPo
'''
chengongs=[]
modelname='筹码突破'
zhouxian_info=''

def get_all_ChouMaTuPo(localpath1):
    info1=  '--筹码突破 start--   '
    writeLog_to_txt_nocode(info1)
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        # print row['ts_code']
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:40]  # 前6行
        # data6_1 = df.iloc[20:32]  # 前6行
        len1 = len(data6_1)
        isAn_ChouMaTuPo_model(data6_1, stock_code)



'''
#2 单独一个函数 判断 6 个数据是不是符合模型
'''
def isAn_ChouMaTuPo_model(data,stockcode):
    if (data is None or data.empty):
        print '--df.empty--' + str(stockcode)
        return 0
    len_data = len(data)
    if (len_data == 0):
        print str(stockcode) + '--data --is null'
    if(len_data >= 6):
        data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
        data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

        data1= data[len_data-1:len_data]
        data1 = data1.reset_index(drop=True)  # 重新建立索引 ,
        riqi = data1.ix[0]['trade_date']  # 阳线的日期
        mairuriqi = 0
        zhisundian = 0
        # print1(data1)

        data2= data[len_data-20:len_data-1]
        data2 = data2.reset_index(drop=True)  # 重新建立索引 ,

        # 设置两个 key
        key_1=0; # 当天 收阳线  涨幅 6% 以上 的个股
        key_6 = 0 ; ## 判断周线是不是 符合 庄家持仓量 的标准.

        day1_close=0
        for index ,row in data1.iterrows():
            pct_chg = row['pct_chg']
            day1_close=row['close']
            if(index==0 and isYangXian(row)==1 and pct_chg >=6): # 6%的阳线
                key_1=1

        # print1(key_1)

        if(key_1==1 ):

            # 判断周线是不是 符合 庄家持仓量 的标准.
            if(is_ChiCangliang_zhouxian(stockcode,riqi)==1):
                key_6=1
            # print key_6
            if(key_6==1):
                info = ''

                info = info + "--筹码突破--"  + str(riqi)
                info = info +"--"+ zhouxian_info
                # info = info+ 'sssss'
                # print info
                writeLog_to_txt(info, stockcode)
                path = modelname + '.txt'
                writeLog_to_txt_path_getcodename(info, path, stockcode)

                chenggong_code={'stockcode':stockcode,'mairuriqi':mairuriqi,'zhisundian':zhisundian}
                # print1(day2_shizixing_low)
                chengongs.append(chenggong_code)

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
            zhongjianzhi_dayin=0
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
                        zhongjianzhi_dayin= zhongjianzhi
                        # print zhongjianzhi
                        # print '---22--'+'count ='+str(count)

                    if(count >=7): # 为了打印日志 区别 大于 7 的 哪些票子.
                        key_3=1
                        zhongjianzhi_dayin = zhongjianzhi
                        break;
                # print '---count='+str(count)
                if(count>=7):  # 终止 外层的循环, 不然 中间值会继续 赋值
                    break

        # print1(key_1)

        if (key_1 == 1 ):

            if (1):
                info = ''
                info = info + "持仓量" +'开始=' +str(riqi) +'-结束='+str(riqi1)
                info = info + '--中间值='+str(zhongjianzhi_dayin)
                if(key_3==1):
                    info = info + '--大于7个'
                    # print info

                # 换手率 的开始日期 要加上 5 天
                start_date = getRiQi_Befor_Ater_Days(riqi, -5)
                end_date = riqi1
                turnover_rate_sum = get_HuanshouLv(stockcode, start_date, end_date)
                if(turnover_rate_sum <120 ) :
                    if (LTSZ_IS_Small_100YI(stockcode) == 1):
                        info = info + '--换手率=' + str(round(turnover_rate_sum, 1)) + '--'
                        ts_ltsz = get_oneStock_LTSZ(stockcode) #得到流通市值
                        info = info + '流通市值='+str(round(ts_ltsz/10000,0)) +'亿'
                        global zhouxian_info
                        zhouxian_info= info
                        return 1
    return 0

'''
测试老师的案例
'''
def test_isAn_ChouMaTuPo_laoshi():
    # 案例 1  案例: 吴通控股 -20190416-300292.SZ  禅 老师讲课案例
    df1 = ts.pro_bar(ts_code='300292.SZ',adj='qfq', start_date='20180416', end_date='20190416')
    data7_1 = df1.iloc[0:30]  # 前7行
    # isAn_ChouMaTuPo_model(data7_1,'300292.SZ')

    # 案例 2 黑牡丹 600510  自己找的案例 中间值=7.55--大于7个----黑牡丹**600510.SH

    df1 = ts.pro_bar(ts_code='600510.SH',adj='qfq', start_date='20180416', end_date='20220208')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ChouMaTuPo_model(data7_1,'600510.SH')

    # 案例 3
    test_isAn_ChouMaTuPo_ziji_shen3_chenggong()

'''

通过禅老师的分析,我好像打通了任督二脉, 自己之前做得过的神 3 测试一下 
胜率是不是能提高很多
'''
def test_isAn_ChouMaTuPo_ziji_shen3_chenggong():
    #满足筹码峰 日线 周线 条件 神 3 成功案例

    # 案例 1 浙江交科 20220207 002061 中间值=6.96--浙江交科**002061.SZ
    df1 = ts.pro_bar(ts_code='002061.SZ',adj='qfq', start_date='20180416', end_date='20220207')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ChouMaTuPo_model(data7_1,'002061.SZ')

    # 案例 2 成都燃气 20220208 603053 中间值=10.26--大于7个----成都燃气**603053.SH
    df1 = ts.pro_bar(ts_code='603053.SH',adj='qfq', start_date='20180416', end_date='20220208')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ChouMaTuPo_model(data7_1,'603053.SH')

    # 案例 3 华海药业# 600521   中间值=20.73--大于7个----华海药业**600521.SH
    df1 = ts.pro_bar(ts_code='600521.SH',adj='qfq', start_date='20180416', end_date='20220218')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ChouMaTuPo_model(data7_1,'600521.SH')

    print '神 1 案例;'

    # 神 1 案例;

    # 案例 1 中路股份  600818
    df1 = ts.pro_bar(ts_code='600818.SH',adj='qfq', start_date='20180416', end_date='20220111')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ChouMaTuPo_model(data7_1,'600818.SH')

    # 案例 1 翔鹭钨业  002842
    df1 = ts.pro_bar(ts_code='002842.SZ',adj='qfq', start_date='20180416', end_date='20220223')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ChouMaTuPo_model(data7_1,'002842.SZ')



'''
  我之前做过的神3
 #不满足 满足筹码峰 日线 周线 条件 神 3 失败案例
'''
def test_isAn_ChouMaTuPo_ziji_shen3_shibai():

    #不满足 满足筹码峰 日线 周线 条件 神 3 失败案例
    #
    # 案例 5 国光股份 002749  筹码突破 日线不满足.  周线不满足 失败
    df1 = ts.pro_bar(ts_code='002749.SZ', adj='qfq', start_date='20180416', end_date='20220218')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ChouMaTuPo_model(data7_1, '002749.SZ')

    # 案例 3 恒久科技  002808 20220216   筹码突破 日线不满足. 周线满足 失败
    df1 = ts.pro_bar(ts_code='002808.SZ',adj='qfq', start_date='20180416', end_date='20220216')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ChouMaTuPo_model(data7_1,'002808.SZ')

    # 案例 4 华阳新材   600281 20220216   筹码突破 日线不满足.  周线不满足 失败
    df1 = ts.pro_bar(ts_code='600281.SH',adj='qfq', start_date='20180416', end_date='20220216')
    data7_1 = df1.iloc[0:30]  # 前7行
    isAn_ChouMaTuPo_model(data7_1,'600281.SH')

'''
测试自己的案例
'''
def test_isAn_ChouMaTuPo_ziji():
    #自己的 案例  --中间值=8.16--换手率100----北方国际**000065.SZ
    df1 = ts.pro_bar(ts_code='000065.SZ',adj='qfq', start_date='20210206', end_date='20220308')
    data7_1 = df1.iloc[0:6]  # 前7行
    # isAn_ChouMaTuPo_model(data7_1,'000065.SZ')

# 改进 统计 10 周内的最大值是多少,
#-中间值=8.23--大于7个--换手率=80.3--流通市值=32.0亿--皖通科技**002331.SZ  神1 5 天改为 4天



'''
回测 8 月份的数据
'''
def test_Befor_data():
    path = BASE_DIR + '/jishu_stock/stockdata/stockcodelist_No_ST.csv'
    data = pd.read_csv(path, dtype={'code': str})
    for index, row in data.iterrows():
        stock_code = row['ts_code']
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        n = 5  # 模型需要最低的数据
        # data7_4 = df.iloc[22:22 + n + 5]  # 前1个月个交易日
        data7_4 = df.iloc[22:22 + n + 22]  # 1 个月
        # data7_4 = df.iloc[22:22 + n + 120]  # 半年
        # data7_4 = df.iloc[22:22+n+250]  # 1年

        len_1 = len(data7_4)
        for i in range(0, len_1 - n + 1):
            # print "i" + str(i )+ "j"+str(i+3)
            isAn_ChouMaTuPo_model(data7_4[i:i + n], stock_code)

    from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
    from jishu_stock.aShengLv.ShengLv import jisuan_all_shouyilv
    wirteList_to_txt(chengongs)
    # chengongs1 = getList_from_txt()
    # jisuan_all_shouyilv(chengongs, modelname, 1.03)
    jisuan_all_shouyilv(chengongs, modelname, 1.05)
    # jisuan_all_shouyilv(chengongs, modelname, 1.07)
    jisuan_all_shouyilv(chengongs, modelname, 1.10)
    jisuan_all_shouyilv(chengongs, modelname, 1.15)


if __name__ == '__main__':
    from  time import  *
    starttime = time()


    localpath1 = '/jishu_stock/stockdata/data1/'
    get_all_ChouMaTuPo(localpath1)
    # test_isAn_ChouMaTuPo_laoshi()
    # test_isAn_ChouMaTuPo_ziji()



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"