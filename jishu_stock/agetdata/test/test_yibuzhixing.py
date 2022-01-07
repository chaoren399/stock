#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from jishu_stock.Tool_jishu_stock import dingshi_ceshi

from threading import Thread
from time import sleep


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async
def A():
    sleep(2)
    print("函数A睡了2秒钟。。。。。。")
    print("a function")


def B():
    print("b function")




if __name__ == '__main__':
    A()
    B()