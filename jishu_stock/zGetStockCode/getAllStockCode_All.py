#!/usr/bin/python
# -*- coding: utf8 -*-
import tushare as ts
import sys
import pandas as pd

from jishu_stock.Tool_jishu_stock import print1, getRiQi_Befor_Ater_Days
from jishu_stock.bChanKe.Tool_LiuTongShiZhi import LTSZ_IS_Small_100YI, get_stock_jibenmian, get_LiuTongShiZhi
from jishu_stock.bChanKe.Tool_Token import token_init
from jishu_stock.z_tool.PyDateTool import getDayNumberYMD
from stock.settings import BASE_DIR

reload(sys)

sys.setdefaultencoding('utf8')

token_init()

# 查询当前所有正常上市交易的股票列表
pro = ts.pro_api()

today = getDayNumberYMD()

g_df = ''  # 全局变量
'''

all  codes   cloude st  

https://tushare.pro/document/2?doc_id=25

300 的 688 的  bu 处理后 

不包含 ST  和 300 开头的创业板 688开头的科创板股票
北交所: 430047.BJ

根据tscode 获取  基本面指标  实时获取

https://tushare.pro/document/2?doc_id=32

'''


def getallstock_list():
    # 1 首先 加载 基本面的数据

    df_jibemian = pro.daily_basic(ts_code='', trade_date=today,
                                  fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb,circ_mv')

    df_jibemian = df_jibemian.set_index(['ts_code'])

    print '得到 股票池'

    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    print data
    data.to_csv("allstockcode_all.csv")
    print  "共"+str(len(data))+"只"




if __name__ == '__main__':
    today = getDayNumberYMD()
    today = '20220323'  # 节假日或者周五 是没有数据的

    getallstock_list()


