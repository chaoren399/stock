#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts

'''
统一 token 获取 
避免后期 token 更新,带来更改的麻烦
'''

ts.set_token('0c9acbe761612301ff2baaa9b3e8ec4053150ad1c1fb0e7b6d53bd5d')

if __name__ == '__main__':
    print  "定时测试"
    # dingshi_ceshi()