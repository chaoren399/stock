#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_parent_dir_name = os.path.dirname(os.path.dirname(current_dir))
# print current_dir
print(parent_parent_dir_name)
sys.path.append(parent_parent_dir_name)

from datetime import datetime

from jishu_stock.JiaGeZhongShu.JGZS_KanZhangZuoZhang import get_all_JGZS_KanZhangZuoZhang
from jishu_stock.JiaGeZhongShu.JGZS_RuanAll import JGZS_yijianyunxing
# from jishu_stock.JiaGeZhongShu.JGZS_RuanAll import JGZS_yijianyunxing
from jishu_stock.JiaGeZhongShu.jiagezhognshu_Get_Week_K_data import getAll_jiagezhongshu_WeekKdata
from jishu_stock.z_tool.email import webhook

if __name__ == '__main__':
    # G8M2_yijianyunxing()
    JGZS_yijianyunxing()


