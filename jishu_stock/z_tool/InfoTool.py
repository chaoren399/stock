#!/usr/bin/python
# -*- coding: utf8 -*-


'''
# info 信息 统一 运行 每次都要执行, 并且信息 返回后,要添加到 info中, 方便后期修改,这样一改,所有的都可以执行了.

'''
def manage_info(info, stockcode,date,yuliu):
    info =''
    # today = getDayNumberYMD()
    from jishu_stock.bChanKe.Tool_ChiCangLiang import isAn_ChiCangLiang_BiaoZhun

    bacinfo = isAn_ChiCangLiang_BiaoZhun(stockcode, date)
    zhouxian_info = ''
    if (len(bacinfo) == 2):
        if (bacinfo[0] == 1):
            key_6 = 1
        zhouxian_info = bacinfo[1]

    info = info + zhouxian_info

    return info

if __name__ == '__main__':
    print '222'
    # import pandas as pd
    # pd.read_csv()

