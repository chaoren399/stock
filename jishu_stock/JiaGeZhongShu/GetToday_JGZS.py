#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian1 import get_all_JGZS_KanZhangYinXian1, \
    isAn_JGZS_KanZhangYinXian1_model
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian2 import get_all_JGZS_KanZhangYinXian2, \
    isAn_JGZS_KanZhangYinXian2_model
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian4 import get_all_JGZS_KanZhangYinXian4, \
    isAn_JGZS_KanZhangYinXian4_model
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangZuoZhang import get_all_JGZS_KanZhangZuoZhang, \
    isAn_JGZS_KanZhangZuoZhang_model
from jishu_stock.JiaGeZhongShu.jiagezhognshu_Get_Week_K_data import getAll_jiagezhongshu_WeekKdata
from jishu_stock.JiaGeZhongShu.jiagezhongshu_KanDieZuoZhang import get_all_jiagezhongshu_KanDieZuoZhang, \
    isAn_KanDieZuoZhang_model
from jishu_stock.z_tool.PyDateTool import getMonthNumber
from stock.settings import BASE_DIR
import pandas as pd
import tushare as ts
import time
'''
根据股票代码 获取 当天是不是价格中枢

1.首先获取当天符合模型的代码
2. 获取周线,
3.判断


GetToday_JGZS
'''

def GetToday_JGZS():
    # 1.首先获取当天符合模型的代码
    yuefen = str(getMonthNumber())
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
            isJGZH(stockcode)


def isJGZH(stockcode):
    #2. 获取周线   我是希望通过 ts 在线获取, 这样比较方便,
    pro = ts.pro_api()
    # stockcode='000032.SZ'
    starttime = datetime.datetime.now()
    today = starttime.strftime('%Y%m%d')

    data = pro.weekly(ts_code=stockcode,start_date='20200101', end_date=today,
                     fields='ts_code,trade_date,open,high,low,close,vol,amount')


    # 1 看跌做涨
    # isAn_KanDieZuoZhang_model(data, stockcode)
    # 2 看涨做涨
    isAn_JGZS_KanZhangZuoZhang_model(data, stockcode)
    # 3  看涨阴线1 上涨初期

    # isAn_JGZS_KanZhangYinXian1_model(data, stockcode)

    # 4 看涨阴线 2 回调位置

    # isAn_JGZS_KanZhangYinXian2_model(data, stockcode)
    # 5 看涨阴线4
    isAn_JGZS_KanZhangYinXian4_model(data, stockcode)


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    GetToday_JGZS()
    # isJGZH('000685.SZ')


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print str((endtime - starttime).seconds/60) + "分钟"