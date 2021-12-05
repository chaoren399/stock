#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

import pandas as pd

from jishu_stock.ChuShuiFuRong.ChuShuiFuRong import get_all_ChuShuiFuRong
from jishu_stock.DaYou.DaYou import get_all_DaYou
from jishu_stock.FanKeWeiZhu.FanKeWeiZhu import get_all_FanKeWeiZhu
from jishu_stock.FanKeWeiZhu.FanKeWeiZhu_Plus import get_all_FanKeWeiZhu_Plus
from jishu_stock.FeiLongZaiTian.FeiLongZaiTian import get_all_FeiLongZaiTian
from jishu_stock.FeiLongZaiTian.FeiLongZaiTian2 import get_all_FeiLongZaiTian2, isAn_FeiLongZaiTian2_model
from jishu_stock.FengHuiLuZhuan.FengHuiLuZhuan import get_all_FengHuiLuZhuan, isAn_FengHuiLuZhuan_model
from jishu_stock.GeShanDaNiu.GeShanDaNiu import get_all_GeShanDaNiu
from jishu_stock.GeShiBaFa.G8M2_RuanAll import G8M2_yijianyunxing
from jishu_stock.JiaGeZhongShu.JGZS_RuanAll import JGZS_yijianyunxing
from jishu_stock.JianLongZaiTian.JianLongZaiTian1 import get_all_JianLongZaiTian1
from jishu_stock.JianLongZaiTian.JianLongZaiTian2 import get_all_JianLongZaiTian2
from jishu_stock.JieJie.JieJie import get_all_JieJie
from jishu_stock.JiuSiYiSheng.jiusiyisheng1 import get_all_jiusiyisheng1
from jishu_stock.KanDieZuoZhang.KanDieZuoZhang import get_all_KanDieZuoZhang
from jishu_stock.KangLongyouHui.KangLongYouHuiGeGu import get_all_KangLongYouHui_GeGu
from jishu_stock.KangLongyouHui.KangLongYouHui_DaPan import get_all_KangLongYouHui_DaPan
from jishu_stock.LiuAnHuaMing.LiuAnHuaMing2 import get_all_LiuAnHuaMing2
from jishu_stock.LongZhan_YuYe.LongZhanYuYe import get_all_LongZhanYuYe
from jishu_stock.LongZhan_YuYe.LongZhanYuYe2 import get_all_LongZhanYuYe2
from jishu_stock.PiJiTaiLai.PiJiTaiLai import get_all_PiJiTaiLai
from jishu_stock.QiBaoJunXian.QiBaoJunXian1 import get_all_QiBaoJunXian1
from jishu_stock.QiBaoJunXian.QiBaoJunXian2 import get_all_QiBaoJunXian2
from jishu_stock.QiBaoJunXian.QiBaoJunXian3 import get_all_QiBaoJunXian3
from jishu_stock.SCS.SCS1 import get_all_SCS_1
from jishu_stock.SiHuiFuRan.SiHuiFuRan import get_all_SiHuiFuRan
from jishu_stock.Tool_jishu_stock import get_2stockcode, dingshi_ceshi, get_all_codes_from_tool, \
    csv_paixu_path1_zhuanyong
from jishu_stock.WuLiKanHua.WuLiKanHua import get_all_WuLiKanHua
from jishu_stock.YiYiDaiLao.YiYiDaiLao2 import get_all_YiYiDaiLao2
from jishu_stock.YouJingWuXian.YouJingWuXian1 import get_all_YouJingWuXian1
from jishu_stock.YouJingWuXian.YouJingWuXian2 import get_all_YouJingWuXian2_1
from jishu_stock.bCaoMaoGui.YiYangChuanDuoJun import get_all_YiYangChuanDuoJun
from jishu_stock.bCaoMaoGui.ZaoChenZhiXing import get_all_ZaoChenZhiXing, isAn_ZaoChenZhiXing_model
from jishu_stock.agetdata.test_2_token import get_all_codes_k_data
from jishu_stock.cShenLongBaiWei.Shen1 import get_all_Shen1
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei1 import  getall_ShenLongBaiWei1
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei0 import get_all_isShenLongBaiWei0
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei2 import get_all_ShenLongBaiWei2
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei3 import get_all_ShenLongBaiWei3
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei4 import get_all_ShenLongBaiWei4
from jishu_stock.VXingFanZhuan.VXingFanzhuan_all import getallstockdata_isV_fromLocal
from jishu_stock.QingTingDianShui_QueKou.QueKou_QingTingDianShui import get_all_QingTingDianShui
from jishu_stock.LingBoWeiBu.LingBoWeiBu import get_all_LingBoWeiBu
from jishu_stock.JiuSiYiSheng.JiuSiYiSheng2 import get_all_JiuSiYiSheng_2
from jishu_stock.YiYiDaiLao.YiYiDaiLao3 import get_all_YiYiDaiLao
from jishu_stock.YiJIanShuangDiao.YiJianShuangDiao import get_all_YiJianShuangDiao
from jishu_stock.zYouQianJun.YouQianJun120_250 import get_all_120_250


from stock.settings import BASE_DIR

'''
G8M2 一键运行
'''
def g8m2_yijianyunxing():
    G8M2_yijianyunxing()

'''
周线 价格中枢一键运行
'''
def jiagezhognshu_yijianyunxing():
    JGZS_yijianyunxing()

'''
日线 一键运行
平时下午 4 点准时更新
周五数据延迟, 5:58 可以下载
'''
def yijianyunxing():
    # 日线 操作
    localpath1 = '/jishu_stock/stockdata/data1/'
    today = starttime.strftime('%Y%m%d')
    dingshi_ceshi()

    # getAllStockData(start_date='20200701', end_date=today, localpath=localpath1) #这个时间 提供一年的得到 MA34
    get_all_codes_k_data()
    endtime = datetime.datetime.now()
    print  "下载数据运行时长:"
    print str((endtime - starttime).seconds/60) + "分钟"





"""
主要是 今天要看的模型数据
"""
def task1(localpath1):
    # 一阳穿多均
    get_all_YiYangChuanDuoJun(localpath1)
    # 早晨之星
    get_all_ZaoChenZhiXing(localpath1)
    # 晓波 SCS1
    get_all_SCS_1(localpath1)
    # 死灰复燃
    get_all_SiHuiFuRan(localpath1)
    # 柳暗花明 底部强势上涨  , 每天标记 ,后期出现 等模型可以加仓
    get_all_LiuAnHuaMing2(localpath1)
    # 见龙在田1 判断 3个 K 线 , 一阳一阴一阳
    get_all_JianLongZaiTian1(localpath1)

    # 结界, 后期有账户再操作
    get_all_JieJie(localpath1)
    # 起爆均线 1
    get_all_QiBaoJunXian1(localpath1)
    # 起爆均线 2
    get_all_QiBaoJunXian2(localpath1)
    # 起爆均线 3
    get_all_QiBaoJunXian3(localpath1)

    # 出水芙蓉 主力底部强势洗盘
    get_all_ChuShuiFuRong(localpath1)

    # 雾里看花, 特殊的十字星 还没验证
    get_all_WuLiKanHua(localpath1)

    # 看跌做涨 上涨结构 抄底 尾盘买入
    get_all_KanDieZuoZhang(localpath1)
    # 飞龙在天, 是萧先生 所有模型里边,挣钱最多, 最快的一个.  胜率最高的
    get_all_FeiLongZaiTian(localpath1)
    # 反客为主 上涨 一天强势洗盘 胜率 80%
    get_all_FanKeWeiZhu(localpath1)
    # 反客为主plus
    get_all_FanKeWeiZhu_Plus(localpath1)
    # 0  上证 50 上证指数  大盘亢龙有悔
    get_all_KangLongYouHui_DaPan()
    # 1 V型 反转
    getallstockdata_isV_fromLocal(localpath1)
    # 8 龙战于野
    get_all_LongZhanYuYe(localpath1)
    # 一箭双雕 复盘 8 月份 94% 的成功率
    get_all_YiJianShuangDiao(localpath1)
    # 大有模型
    get_all_DaYou(localpath1)
    # 以逸待劳
    get_all_YiYiDaiLao(localpath1)

    # yijianyunxing_new()

    # 熊市末期亢龙有悔 个股上的应用:
    get_all_KangLongYouHui_GeGu(localpath1)

    # 否极泰来 97% 的超高胜率
    get_all_PiJiTaiLai(localpath1)
    #  神龙摆尾1
    getall_ShenLongBaiWei1(localpath1)
    get_all_Shen1(localpath1)  # pro

"""
明天要盯盘的任务
"""
def task2(localpath1):
    # 盯盘 的模型
    # 峰回路转  当天条件挂单
    infolists1=get_all_FengHuiLuZhuan(localpath1)
    # 飞龙在天2, 超短线  第 3 天盯收盘价 高过小 K 线实体买入
    infolists2=get_all_FeiLongZaiTian2(localpath1)
    # 龙战于野2 找 2 天的数据, 第 3 天盯盘
    # get_all_LongZhanYuYe2(localpath1)

def test2():

    stock_codes = get_all_codes_from_tool()
    len_codes=len(stock_codes)
    a = stock_codes[0:1000]
    b = stock_codes[len_codes /2 :len_codes]

    for index, item in enumerate(a):
        # print index, item
        stock_code=item
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        data6_1 = df.iloc[0:30]  # 前6行

        isAn_FengHuiLuZhuan_model(data6_1, stock_code)
        # isAn_FeiLongZaiTian2_model(data6_1, stock_code)

        # 早晨之星
        isAn_ZaoChenZhiXing_model(data6_1, stock_code)
        # get_all_ZaoChenZhiXing(localpath1)

    # name = gl.get_value('fenghuiluzhan')
    # print name
    print '------'


    csv_paixu_path1_zhuanyong()



def test():
    zzys = 3


if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    # yijianyunxing()
    # task2(localpath1)
    # test()
    test2()
    # zzys=2



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"