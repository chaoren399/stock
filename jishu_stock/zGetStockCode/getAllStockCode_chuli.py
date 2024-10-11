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

https://tushare.pro/document/2?doc_id=25

把 ST 的 300 的 688 的 处理后 

不包含 ST  和 300 开头的创业板 688开头的科创板股票
北交所: 430047.BJ

根据tscode 获取  基本面指标  实时获取

https://tushare.pro/document/2?doc_id=32

'''


def getallstock_list_chuli():
    # 1 首先 加载 基本面的数据

    df_jibemian = pro.daily_basic(ts_code='', trade_date=today,
                                  fields='ts_code,trade_date,close,turnover_rate,volume_ratio,pe,pb,circ_mv')

    df_jibemian = df_jibemian.set_index(['ts_code'])

    print '得到 不包含 ST  和 300 开头的创业板 688开头的科创板股票 的 股票池'
    # print '得到 不包含 ST  和 688开头的科创板股票 的 股票池'

    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    tamp = []
    for index, row in data.iterrows():
        name = row['name']
        code = row['ts_code']
        # code = '830799.BJ'
        list_date = row['list_date']  # 上市日期

        code_300 = code[0:3]  # 用来排除 300,688

        BJ_houzhui = code[len(code) - 3:len(code)]
        # print code_300

        key1 = 0
        # if (code == '688278.SH'):
        #     print "688278"
        if (
                'ST' not in name and code_300 != '300' and code_300 != '688' and BJ_houzhui != '.BJ'):  # 不包含 ST  和 300 开头的创业板 688开头的科创板股票
                # 'ST' not in name  and code_300 != '688' and BJ_houzhui != '.BJ'):  # 不包含 ST  和 300 开头的创业板 688开头的科创板股票
            if (list_date < '20200101'):  # 排除所有新上市的公司
                key1 = 1;

            if (key1 == 1):
                try:
                    jibenmin_row = df_jibemian.loc[code]
                    stock_close_price = jibenmin_row['close']
                    stock_liutongshizhi = jibenmin_row['circ_mv']
                    # if(stock_liutongshizhi < 1000000 ): #过滤流通市值 100 亿以下的
                    if (stock_liutongshizhi < 2000000):  # 过滤流通市值 100 亿以下的
                        if (stock_close_price >= 3 and stock_close_price < 20):
                            print  code
                            # if(code=='000677.SZ'):
                            #     print code
                            #     print stock_close_price
                            tamp.append(row)
                except:
                    '''  get_stock_jibenmian(code) is  null= 002408.SZ 公司停牌 '''

                    print  'get_stock_jibenmian(code) is  null= ' + code

    tamp = pd.DataFrame(tamp, columns=['ts_code', 'symbol', 'name', 'area', 'industry', 'list_date'])
    tamp = tamp.reset_index(drop=True)
    tamp.to_csv("allstockcode_No_ST.csv")
    print "allstockcode_No_ST.csv"

    print  str(len(tamp))


if __name__ == '__main__':
    today = getDayNumberYMD()
    today = '20220323'  # 节假日或者周五 是没有数据的

    getallstock_list_chuli()


