#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd

from jishu_stock.aKangLongyouHui.KangLongYHXiongShiMoQi import get_all_KangLongYouHuiXiongShiMoQi
from jishu_stock.aKangLongyouHui.KangLongYouHui_DaPan import get_all_KangLongYouHui_DaPan
from jishu_stock.bQiXingLuoChangKong.QiXingluochangkong1 import getallstockdata_is7start_FromLocal
from jishu_stock.bQiXingLuoChangKong.QiXingluochangkong2 import getallstockdata_is7start2_FromLocal
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei import getallstockdata_isShenLongBaiWei_fromLocal
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei0 import get_all_isShenLongBaiWei0
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei2 import get_all_ShenLongBaiWei2
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei3 import getallstockdata_isShenLongBaiWei3_fromLocal, \
    get_all_ShenLongBaiWei3
from jishu_stock.aKangLongyouHui.kanglongyouhui import getallstockdata_isKangLong_fromLocal
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei4 import getallstockdata_isShenLongBaiWei4_fromLocal
from jishu_stock.dVXingFanZhuan.VXingFanzhuan_all import getallstockdata_isV_fromLocal
from jishu_stock.eRiJunXianZuhe.RiJunXianZuhe import get_5_13_34_RiJunXian
from jishu_stock.fGeShiBaFa.GeShiBaFa_Pro import getallstockdata_is_GeShi_8fa
from jishu_stock.gShuangLong_Qushui.ShuangLong_Qushui import getallstockdata_is_ShuangLong_Qushui_FromLocal
from jishu_stock.getAllStockData import getAllStockData
from jishu_stock.iLongZhan_YuYe.LongZhanYuYe import getallstockdata_isLongZhan_YuYe
from jishu_stock.kQingTingDianShui_QueKou.QueKou_QingTingDianShui import get_all_QingTingDianShui
from jishu_stock.lLingBoWeiBu.LingBoWeiBu import get_all_LingBoWeiBu
from jishu_stock.mJiuSiYiSheng.JiuSiYiSheng1 import get_all_JiuSiYiSheng_1
from jishu_stock.mJiuSiYiSheng.JiuSiYiSheng2 import get_all_JiuSiYiSheng_2
from jishu_stock.nYiYiDaiLao.YiYiDaiLao import get_all_YiYiDaiLao
from jishu_stock.oYiJIanShuangDiao.YiJianShuangDiao import get_all_YiJianShuangDiao
from jishu_stock.zYouQianJun.YouQianJun120_250 import get_all_120_250


def yijianyunxing():

    # 日线 操作

    localpath1 = '/jishu_stock/stockdata/data1/'

    today = starttime.strftime('%Y%m%d')

    getAllStockData(start_date='20200701', end_date=today, localpath=localpath1) #这个时间 提供一年的得到 MA34

    #0  上证 50 上证指数  大盘亢龙有悔
    get_all_KangLongYouHui_DaPan()

    # 1 V型 反转
    getallstockdata_isV_fromLocal(localpath1)
    # 熊市末期亢龙有悔 个股上的应用:
    get_all_KangLongYouHuiXiongShiMoQi(localpath1)

    # 2以逸待劳
    get_all_YiYiDaiLao(localpath1)

    # 一箭双雕
    get_all_YiJianShuangDiao(localpath1)

    # 神龙摆尾0
    get_all_isShenLongBaiWei0(localpath1)

    #  神龙摆尾1
    getallstockdata_isShenLongBaiWei_fromLocal(localpath1)
    # 神龙摆尾2
    get_all_ShenLongBaiWei2(localpath1)
    #  神龙摆尾3
    get_all_ShenLongBaiWei3(localpath1)

    # 3 神龙摆尾 4
    getallstockdata_isShenLongBaiWei4_fromLocal(localpath1)



    #12 九死一生(1) #好用 分上涨和下跌 2 个阶段
    get_all_JiuSiYiSheng_1(localpath1)




    # 8 龙战于野
    getallstockdata_isLongZhan_YuYe(localpath1)






    # 9 蜻蜓点水  缺口理论
    get_all_QingTingDianShui(localpath1)
    # 10 凌波微步  缺口理论  模板
    get_all_LingBoWeiBu(localpath1)



    #13 九死一生(2) 容易失败
    get_all_JiuSiYiSheng_2(localpath1)

    #2 七星落长空 1
    getallstockdata_is7start_FromLocal(localpath1=localpath1)
    # 七星落长空 2
    getallstockdata_is7start2_FromLocal(localpath1)


    # 14 有钱君-120-250 均线交易法
    get_all_120_250()

    # 15 葛式八法
    # getallstockdata_is_GeShi_8fa()

    #7  双龙取水 模型
    getallstockdata_is_ShuangLong_Qushui_FromLocal(localpath1)
    # 6 5-13-34 日均线组合
    get_5_13_34_RiJunXian(localpath1)




if __name__ == '__main__':
    starttime = datetime.datetime.now()

    yijianyunxing()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print str((endtime - starttime).seconds/60) + "分钟"