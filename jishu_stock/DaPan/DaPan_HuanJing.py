#!/usr/bin/python
# -*- coding: utf8 -*-
import tushare as ts
import sys

from jishu_stock.Tool_jishu_stock import print1
from jishu_stock.bChanKe.Tool_Token import token_init

reload(sys)
sys.setdefaultencoding('utf8')
from jishu_stock.z_tool.PyDateTool import getDayNumberYMD


'''
判断 大盘当前的环境 - 仓位的量化管理

1. 120 日均线
2. 20 日均线
3, 成交量
 4 天 站上 120VOL  强势
 4 天内 有 2-3 天 站上 120 vol  一般
 4 天内最多只有 1 天站上 120vol 弱势

 满仓 70+
 半仓仓位: 50%
 轻仓仓位: 30%
 试仓仓位: 10
 空仓仓位: 0

'''

def get_DaPan_HuanJing(enddate):


    # print today
    # 上证指数 000001.SH
    data = ts.pro_bar(ts_code='000001.SH', adj='qfq',asset='I', start_date='20180101', end_date=enddate,
                    ma=[ 20, 120]
                    )
    data = data.iloc[0:4]  # 前4行
    data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    data = data.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。


    # print data

    key_1 = 0;  # 是否站上 120日 均线
    key_2 = 0;  # 是否站上 20日 均线
    key_3_1 = 0;  # 4 天成交量 都在 120vol 以上
    key_3_2 = 0;  # 4 天内有 2-3 天 成交量 在 120vol 以上
    key_3_3 = 0;  # 4 天内 最多只有 1 天 成交量 在 120vol 以上

    count=0
    for index,row in data.iterrows():
        vol = row['vol']
        mavol120= row['ma_v_120']
        if(vol > mavol120):
            count=count+1
        if(index==3):
            day4_close = row['close']
            if(day4_close > row['ma120']):
                key_4=4
            if(day4_close > row['ma20']):
                key_2=3

    if(count <=1):
        key_3_3=0
    elif(count <=3):
        key_3_2=1
    elif (count==4):
        key_3_1=3

    if(0):
        print1(key_1)
        print1(key_2)
        print1(key_3_1)
        print1(key_3_2)
        print1(key_3_3)

    zongfen = key_1 + key_2+ key_3_1 +key_3_2+key_3_3

    # print1(zongfen)
    info=''
    if(zongfen<=1):
        info = info + '空仓:'+str(zongfen)+'分--'+'仓位 0%'
    elif(zongfen==3):
        info = info + '试仓:' + str(zongfen)+'分--'+'仓位 10%'
    elif(zongfen<=6 and zongfen > 3):
        info = info + '轻仓:' + str(zongfen) +'分--'+'仓位 30%'
    elif(zongfen<=6 and zongfen > 3):
        info = info + '半仓:' + str(zongfen)+'分--'+'仓位 40-50%'
    elif(zongfen > 7):
        info = info + '满仓:' + str(zongfen)+'分--'+'仓位 70+%'


    juti_info = ''
    if(key_1 ==1):
        juti_info = juti_info+ '指数 站上 120日 均线 '
    if(key_2==1):
        juti_info = juti_info + '指数 站上 站上 20日 均线 '
    if(key_3_1==1):
        juti_info = juti_info + '指数 4 天成交量 都在 120vol 以上 '
    if(key_3_2==1):
        juti_info = juti_info + '指数 4 天内有 2-3 天 成交量 在 120vol 以上 '
    if(key_3_3==1):
        juti_info = juti_info + '指数 4 天内 最多只有 1 天 成交量 在 120vol 以上 '

    info = info + juti_info

    print info
    return info



if __name__ == '__main__':

    today = getDayNumberYMD()
    get_DaPan_HuanJing(today)