#!/usr/bin/python
# -*- coding: utf8 -*-

import math


'''
python 
向上取整ceil 
向下取整floor 
四舍五入round
'''

#向上取整
print "math.ceil---"
print "math.ceil(2.3) => ", math.ceil(2.3)
print "math.ceil(2.6) => ", math.ceil(2.6)

#向下取整
print "\nmath.floor---"
print "math.floor(2.3) => ", math.floor(2.3)
print "math.floor(2.6) => ", math.floor(2.6)

#四舍五入
print "\nround---"
print "round(2.3) => ", round(2.3)
print "round(2.6) => ", round(2.6)


#四舍五入
print "\nround---"
print "round(2.3) => ", round(2.348,2)
print "round(2.6) => ", round(2.686,2)

#这三个的返回结果都是浮点型
print "\n\nNOTE:every result is type of float"
print "math.ceil(2) => ", math.ceil(2)
print "math.floor(2) => ", math.floor(2)
print "round(2) => ", round(2)