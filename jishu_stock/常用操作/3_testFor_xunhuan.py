#!/usr/bin/python
# -*- coding: utf8 -*-
# for i in range(1, 10)
from jishu_stock.fGeShiBaFa.GeShiBaFa_Mai2 import is_big_to_small, is_small_to_big


def test_for():
    dd = [0,1, 2, 3, 4]
    for i in range(2, len(dd)-1):
        print dd[0:i]
        print dd[i:]
        print i
def test_break():
    dd=[1,2,3,4]
    for i in range(0,len(dd)):
        if(i==3):
            break
        print i

def test_is_big_to_small():
    dd = [1, 2, 3, 4]
    # dd = [6, 5, 6, 4]
    # print is_big_to_small(dd)
    print is_small_to_big(dd)


if __name__ == '__main__':
    # test_break()
    # test_is_big_to_small()
    test_for()