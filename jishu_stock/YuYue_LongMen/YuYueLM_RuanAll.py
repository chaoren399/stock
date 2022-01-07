#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian1 import get_all_JGZS_KanZhangYinXian1
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian2 import get_all_JGZS_KanZhangYinXian2
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian4 import get_all_JGZS_KanZhangYinXian4
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangZuoZhang import get_all_JGZS_KanZhangZuoZhang
from jishu_stock.JiaGeZhongShu.jiagezhognshu_Get_Week_K_data import getAll_jiagezhongshu_WeekKdata
from jishu_stock.JiaGeZhongShu.jiagezhongshu_KanDieZuoZhang import get_all_jiagezhongshu_KanDieZuoZhang
from jishu_stock.YuYue_LongMen.Get_Month_K_data import getAllMonth_Kdata
from jishu_stock.YuYue_LongMen.YuYueLongMen import getallstockdata_isYuYueLongMen_fromLocal

'''
YuYueLM
'''

def YuYueLM_yijianyunxing():

    localpath1 = '/jishu_stock/stockdata/data1/'

    # 1下载数据
    # getAllMonth_Kdata(localpath1)

    #2  获取 鱼跃龙门 模型 1
    getallstockdata_isYuYueLongMen_fromLocal()

if __name__ == '__main__':
    starttime = datetime.datetime.now()

    YuYueLM_yijianyunxing()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print str((endtime - starttime).seconds/60) + "分钟"