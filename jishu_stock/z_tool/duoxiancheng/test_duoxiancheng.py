#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import tushare as ts
import sys
import pandas as pd
from jishu_stock.Tool_jishu_stock import dingshi_ceshi
# coding:utf-8


from time import sleep  # 导入时间休眠函数

''''
测试多线程
# 功能1：如下代码实现了任务task1和task2同步进行，提高了效率。
参考: 
https://www.cnblogs.com/sunshine-blog/p/12186162.html


'''

def task1(n):  # 定义任务1
    for x in range(n):  # 遍历数组n里的x
        print("正在运行任务1,打印：", x)  # 打印正则运行任务1，打印x的值
    sleep(0.5)  # 时间休眠0.5秒


def task2():  # 定义任务2
    list1 = ["北京欢迎您", "红日", "故宫的记忆", "义勇军进行曲"]  # 定义列表1位4首歌曲名
    for info in list1:  # 遍历list1里的信息
        print("正在运行任务2，听音乐：", info)  # 打印正在运行任务2，听音乐:音乐名称
    sleep(0.6)  # 时间休眠0.6秒


def main():  # 定义main函数
    from threading import Thread  # 导入线程函数
    t1 = Thread(target=task1, args=(6,))  # 定义线程t1，线程任务为调用task1函数，task1函数的参数是6
    t2 = Thread(target=task2)  # 定义线程t2，线程任务为调用task2函数，task2函数无参数
    t1.start()  # 开始运行t1线程
    t2.start()  # 开始运行t2线程

    # join()只有在你需要等待线程完成时候才是有用的。
    t1.join()
    t2.join()

if __name__ == '__main__':
    main()  # 调用main函数