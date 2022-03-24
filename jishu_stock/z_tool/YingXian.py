#!/usr/bin/python
# -*- coding: utf8 -*-

from jishu_stock.Tool_jishu_stock import  isYangXian

'''
获取 阳线 上影线的比例 ,跟实体的比值
'''
def YangXianShangYingXian(row ):

    if(isYangXian(row)==1):
        highprice=row['high']
        closeprice=row['close']
        openprice=row['open']

        shangyingxian=highprice-closeprice
        shitidaxiao= closeprice - openprice +0.001

        shangyingxian_shiti= shangyingxian / shitidaxiao

        return shangyingxian_shiti

