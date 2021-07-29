#!/usr/bin/python
# -*- coding: utf8 -*-

import tushare as ts
import sys

reload(sys)

sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    # dt.to_csv('Result.csv') #相对位置，保存在getwcd()获得的路径下
    # dt.to_csv('C:/Users/think/Desktop/Result.csv') #绝对位置

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')

    # 查询当前所有正常上市交易的股票列表
    pro = ts.pro_api()

    data = pro.stock_basic()
    data.to_csv("1.csv")