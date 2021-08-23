#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.bQiXingLuoChangKong.QiXingluochangkong1 import getallstockdata_is7start_FromLocal
from jishu_stock.bQiXingLuoChangKong.QiXingluochangkong2 import getallstockdata_is7start2_FromLocal
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei import getallstockdata_isShenLongBaiWei_fromLocal
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei3 import getallstockdata_isShenLongBaiWei3_fromLocal
from jishu_stock.aKangLongyouHui.kanglongyouhui import getallstockdata_isKangLong_fromLocal
from jishu_stock.dVXingFanZhuan.VXingFanzhuan_all import getallstockdata_isV_fromLocal
from jishu_stock.eRiJunXianZuhe.RiJunXianZuhe import get_5_13_34_RiJunXian
from jishu_stock.getAllStockData import getAllStockData


def yijianyunxing():

    # 日线 操作

    localpath1 = '/jishu_stock/stockdata/data1/'

    today = starttime.strftime('%Y%m%d')

    getAllStockData(start_date='20200701', end_date=today, localpath=localpath1)

    #亢龙有悔
    getallstockdata_isKangLong_fromLocal(localpath1)
    #2 七星落长空 1
    getallstockdata_is7start_FromLocal(localpath1=localpath1)
    # 七星落长空 2
    getallstockdata_is7start2_FromLocal(localpath1)
    # 3 神龙摆尾
    getallstockdata_isShenLongBaiWei_fromLocal(localpath1)
    # 神龙摆尾3
    getallstockdata_isShenLongBaiWei3_fromLocal(localpath1)
    # V型 反转
    getallstockdata_isV_fromLocal(localpath1)

    # 5-13-34 均线组合
    get_5_13_34_RiJunXian(localpath1)

if __name__ == '__main__':

    starttime = datetime.datetime.now()


    yijianyunxing()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print str((endtime - starttime).seconds/60) + "分钟"