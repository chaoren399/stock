#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
import os

from jishu_stock.zGetStockCode.Xmind.get_Xmind_Data import getXimndData

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_parent_dir_name = os.path.dirname(os.path.dirname(current_dir))
# print current_dir
print(parent_parent_dir_name)
sys.path.append(parent_parent_dir_name)



if __name__ == '__main__':


    getXimndData()