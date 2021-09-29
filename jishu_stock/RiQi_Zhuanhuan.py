#!/usr/bin/python
# -*- coding: utf8 -*-
# for i in range(1, 10)
from datetime import datetime


'''
2021-05-16   转化为  20210516
'''
def Y_D_M_To_YMD(date):
    date = str(date)
    if(len(date)==10):
        return date.split('-')[0]+date.split('-')[1]+date.split('-')[2]
