#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from jishu_stock.agetdata.test_ziji_model.XiaoV.huice.XiaoV_huice import get_all_XiaoV

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    # 日线 操作
    localpath1 = '/jishu_stock/stockdata/data1/'
    today = starttime.strftime('%Y%m%d')
    # 先更新数据
    get_all_XiaoV(localpath1)