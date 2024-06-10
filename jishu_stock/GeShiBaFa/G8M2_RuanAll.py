#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from jishu_stock.GeShiBaFa.G8M2_XiaYingXian_Yang import  get_all_G8M2_XiaYingXian_YangXian
from jishu_stock.GeShiBaFa.G8M2_XiaYingXian_YinXian import get_all_G8M2_XiaYingXian_YinXian
from jishu_stock.GeShiBaFa.Get_Week_K_data_From_Ts import getAllWeekKdata


'''
G8M2 一键运行
'''

def G8M2_yijianyunxing():
    # 日线 操作
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    today = starttime.strftime('%Y%m%d')
    #先更新数据
    getAllWeekKdata(localpath1)

    #1 阳线 下影线 下穿 60 周均线
    get_all_G8M2_XiaYingXian_YangXian()
    #2阴线下影线 穿越 60 周均线
    get_all_G8M2_XiaYingXian_YinXian()


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    G8M2_yijianyunxing()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print str((endtime - starttime).seconds/60) + "分钟"