#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts
import sys
import pandas as pd
from jishu_stock.Tool_jishu_stock import dingshi_ceshi
# coding:utf-8


''''
测试 线程池

参考: 
https://blog.csdn.net/qq_45675449/article/details/106729552
'''

import threadpool  # 线程池模块
import time


def outdata(name):  # 线程池执行的函数
    print("你好 %s" % name)
    time.sleep(3)
def test_duoxiancheng():

    datalist = []  # 创建参数列表
    for i in range(10):
        datalist.append(i)

    pool = threadpool.ThreadPool(20)  # 线程池创建10个子线程
    tasks = threadpool.makeRequests(outdata, datalist)  # 参数列表长度为10 所以要执行10个任务
    [pool.putRequest(req) for req in tasks]  # 将要执行的任务放入线程池中
    pool.wait()  # 等待所有子线程执行完毕后退出

def test_duoxiancheng2():
    from multiprocessing.dummy import Pool
    datalist = []  # 创建参数列表
    for i in range(10):
        datalist.append(i)
    pool = Pool(2)
    result = pool.map(outdata, datalist)
    pool.close()
    pool.join()  # 等待所有子线程执行完毕后退出，在此之前要执行 .close 方法


if __name__ == '__main__':

    time1 = time.time()
    test_duoxiancheng2()
    # test_duoxiancheng()
    time2 = time.time()
    print(time2 - time1)  # 从开始到结束所用的时间
