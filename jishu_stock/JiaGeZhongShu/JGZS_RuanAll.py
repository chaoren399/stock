#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian1 import get_all_JGZS_KanZhangYinXian1
# from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian1 import get_all_JGZS_KanZhangYinXian1
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian2 import get_all_JGZS_KanZhangYinXian2
# from jishu_stock.JiaGeZhongShu.JGZS_KanZhangYinXian4 import get_all_JGZS_KanZhangYinXian4
from jishu_stock.JiaGeZhongShu.JGZS_KanZhangZuoZhang import get_all_JGZS_KanZhangZuoZhang
from jishu_stock.JiaGeZhongShu.JGZS_QiangShiGu import get_all_JGZS_QiangShiGu
from jishu_stock.JiaGeZhongShu.jiagezhognshu_Get_Week_K_data import getAll_jiagezhongshu_WeekKdata
from jishu_stock.JiaGeZhongShu.jiagezhongshu_KanDieZuoZhang import get_all_jiagezhongshu_KanDieZuoZhang
from jishu_stock.z_tool.email import webhook


#shell 定时脚本
def JGZS_yijianyunxing():
    # 日线 操作
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    starttime = datetime.datetime.now()
    today = starttime.strftime('%Y%m%d')
    #先更新数据
    webhook.sendData("-----周线数据更新-开始 ----"  )
    getAll_jiagezhongshu_WeekKdata(localpath1)
    webhook.sendData("-----周线数据更新-结束 ----"  )


    #2 看涨做涨
    webhook.sendData("-----看涨做涨-开始 ----"  )
    get_all_JGZS_KanZhangZuoZhang(localpath1)
    webhook.sendData("-----看涨做涨--结束 ----"  )

    # 3  看涨阴线1 回调位置
    webhook.sendData("-----看涨阴线1--开始 ----"  )
    get_all_JGZS_KanZhangYinXian1(localpath1)
    webhook.sendData("-----看涨阴线1--结束----"  )

    # 4 看涨阴线 2 回调位置
    webhook.sendData("-----看涨阴线2--开始 ----"  )
    get_all_JGZS_KanZhangYinXian2(localpath1)
    webhook.sendData("-----看涨阴线2--结束 ----"  )

    #3 zhouxian  qiangshi gu

    # get_all_JGZS_QiangShiGu(localpath1)


    #5 看涨阴线4
    # get_all_JGZS_KanZhangYinXian4(localpath1)




    # 其他 价格中枢
    # jiagezhognshu2(localpath1)



def  jiagezhognshu2(localpath1):


    # 4 看涨阴线 2 回调位置
    get_all_JGZS_KanZhangYinXian2(localpath1)

    # 1 看跌做涨
    get_all_jiagezhongshu_KanDieZuoZhang(localpath1)

if __name__ == '__main__':
    starttime = datetime.datetime.now()

    JGZS_yijianyunxing()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print str((endtime - starttime).seconds/60) + "分钟"