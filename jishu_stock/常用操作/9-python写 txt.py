#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from stock.settings import BASE_DIR

# with open ('bai.html' ,'w',encoding='utf-8') as f:
#     f.write(response.text)
datetime.datetime.now().strftime('%Y-%m-%d' )
qianzhu= datetime.datetime.now().strftime('%Y-%m-%d' )
shuchupath = BASE_DIR + '/jishu_stock/zJieGuo/'+qianzhu+'.txt'
with open(shuchupath,"a") as f:
    f.write("aaaq"+''+"\n")

shuchupath = BASE_DIR + '/jishu_stock/zJieGuo/2021-08-15.txt'

fp = open(shuchupath, "a")
fp.write("hello1 python")
fp.close()