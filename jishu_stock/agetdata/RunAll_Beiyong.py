#!/usr/bin/python
# -*- coding: utf8 -*-

import pandas as pd

from jishu_stock.ChuShuiFuRong.ChuShuiFuRong import isAn_ChuShuiFuRong_model
from jishu_stock.DaYou.DaYou import isAn_DaYou_model
from jishu_stock.FanKeWeiZhu.FanKeWeiZhu import isAn_FanKeWeiZhu_model
from jishu_stock.FanKeWeiZhu.FanKeWeiZhu_Plus import isAn_FanKeWeiZhu_Plus_model
from jishu_stock.FeiLongZaiTian.FeiLongZaiTian import isAn_FeiLongZaiTian_model
from jishu_stock.FeiLongZaiTian.FeiLongZaiTian2 import isAn_FeiLongZaiTian2_model
from jishu_stock.FengHuiLuZhuan.FengHuiLuZhuan import isAn_FengHuiLuZhuan_model
from jishu_stock.GeShanDaNiu.GeShanDaNiu import isAn_GeShanDaNiu_model
from jishu_stock.GeShiBaFa.G8M2_RuanAll import G8M2_yijianyunxing
from jishu_stock.JiaGeZhongShu.JGZS_RuanAll import JGZS_yijianyunxing
from jishu_stock.JianLongZaiTian.JianLongZaiTian1 import isAn_JianLongZaiTian1_model
from jishu_stock.JianLongZaiTian.JianLongZaiTian2 import isAn_JianLongZaiTian2_model
from jishu_stock.JianLongZaiTian.JianLongZaiTian5 import isAn_JianLongZaiTian5_model
from jishu_stock.JieJie.JieJie import isAn_JieJie_model
from jishu_stock.JiuSiYiSheng.jiusiyisheng1 import isAn_jiusiyisheng1_model
from jishu_stock.KanDieZuoZhang.KanDieZuoZhang import isAn_KanDieZuoZhang_model
from jishu_stock.KangLongyouHui.KangLongYouHuiGeGu import isAn_KangLongYouHui_GeGu_model
from jishu_stock.KangLongyouHui.KangLongYouHui_DaPan import get_all_KangLongYouHui_DaPan
from jishu_stock.LiuAnHuaMing.LiuAnHuaMing2 import isAn_LiuAnHuaMing2_model
from jishu_stock.LongZhan_YuYe.LongZhanYuYe import isAn_LongZhanYuYe_model
from jishu_stock.LongZhan_YuYe.LongZhanYuYe2 import isAn_LongZhanYuYe2_model
from jishu_stock.PiJiTaiLai.PiJiTaiLai import get_all_PiJiTaiLai
from jishu_stock.QiBaoJunXian.QiBaoJunXian1 import isAn_QiBaoJunXian1_model
from jishu_stock.QiBaoJunXian.QiBaoJunXian2 import isAn_QiBaoJunXian2_model
from jishu_stock.QiBaoJunXian.QiBaoJunXian3 import isAn_QiBaoJunXian3_model
from jishu_stock.QiBaoJunXian.QiBaoJunXian4 import isAn_QiBaoJunXian4_model
from jishu_stock.SCS.SCS1 import isAn_SCS_1_model
from jishu_stock.SiHuiFuRan.SiHuiFuRan import isAn_SiHuiFuRan_model
from jishu_stock.Tool_jishu_stock import get_2stockcode, get_all_codes_from_tool, \
    csv_paixu_path1_zhuanyong
from jishu_stock.WuLiKanHua.WuLiKanHua import isAn_WuLiKanHua_model
from jishu_stock.YiYiDaiLao.YiYiDaiLao0 import isAn_YiYiDaiLao2_model
from jishu_stock.YouJingWuXian.YouJingWuXian1 import isAn_YouJingWuXian1_model
from jishu_stock.YouJingWuXian.YouJingWuXian2 import isAn_YouJingWuXian2_1_model
from jishu_stock.agetdata.getdata_2theard import get_all_codes
from jishu_stock.agetdata.test_ziji_model.ZTB_XiaoYinXian_TiaoKong import isAn_ZTB_YinXian_TiaoKong_model
from jishu_stock.bCaoMaoGui.NXingFanZhuan import isAn_NXingFanZhuan_model
from jishu_stock.bCaoMaoGui.TaXingDi import isAn_TaXingDi_model
from jishu_stock.bCaoMaoGui.YiYangChuanDuoJun import isAn_YiYangChuanDuoJun_model
from jishu_stock.bCaoMaoGui.ZaoChenZhiXing import isAn_ZaoChenZhiXing_model
from jishu_stock.bCaoMaoGui.ZaoChenZhiXing2 import isAn_ZaoChenZhiXing2_model
from jishu_stock.cShenLongBaiWei.Shen1 import isAn_Shen1_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei0 import isAn_ShenLongBaiWei0_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei2 import get_all_ShenLongBaiWei2
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei3 import isAnShenLongBaiwei3_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei4 import get_all_ShenLongBaiWei4
from jishu_stock.VXingFanZhuan.VXingFanzhuan_all import isAnV_model
from jishu_stock.QingTingDianShui_QueKou.QueKou_QingTingDianShui import get_all_QingTingDianShui
from jishu_stock.LingBoWeiBu.LingBoWeiBu import get_all_LingBoWeiBu
from jishu_stock.JiuSiYiSheng.JiuSiYiSheng2 import isAn_JiuSiYiSheng_2_model
from jishu_stock.YiYiDaiLao.yiyidailaoAll.YiYiDaiLao0 import isAn_YiYiDaiLao_model
from jishu_stock.YiJIanShuangDiao.YiJianShuangDiao import isAn_YiJianShuangDiao_model
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

    get_all_codes() #下载所有 股票数据

    stock_codes = get_all_codes_from_tool() # 获取所有股票代码
    for index, item in enumerate(stock_codes):
        # print index, item
        stock_code=item
        stockdata_path = BASE_DIR + localpath1 + stock_code + ".csv"
        df = pd.read_csv(stockdata_path, index_col=0)

        # data6_1 = df.iloc[0:30]  # 前6行
        data6_1 = df.iloc[0:132]  # 前6行
        data6_1 = df.iloc[0:136]  # 前6行
        # data6_1 = df.iloc[2:136]  # 前6行
        task1(data6_1, stock_code)
        task2(data6_1, stock_code)
        task3(data6_1, stock_code)

    endtime = time()
    print "task1,2,3 总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"
    task4()
    csv_paixu_path1_zhuanyong()

"""
主要是 今天要看的模型数据
"""
def task1(data6_1,stock_code):
    #涨停板后 跳空的小阴线, 胜率 70%
    isAn_ZTB_YinXian_TiaoKong_model(data6_1, stock_code)

    #N型反转
    isAn_NXingFanZhuan_model(data6_1, stock_code)
    #塔形底
    isAn_TaXingDi_model(data6_1, stock_code)
    #早晨之星 十字星实体 小于 0.6
    isAn_ZaoChenZhiXing_model(data6_1, stock_code)

    #见龙在田5
    isAn_JianLongZaiTian5_model(data6_1, stock_code)

    # 早晨之星2 十字星下影线比实体大 1.5 倍
    isAn_ZaoChenZhiXing2_model(data6_1, stock_code)

    #出水芙蓉 主力底部强势洗盘
    isAn_ChuShuiFuRong_model(data6_1, stock_code)
    #起爆均线4 胜率 80%
    isAn_QiBaoJunXian4_model(data6_1, stock_code)

    #涨停板后 跳空的大阴线
    isAn_ZTB_YinXian_TiaoKong_model(data6_1, stock_code)

    # 1 V型 反转
    isAnV_model(data6_1, stock_code)
    # 8 龙战于野
    isAn_LongZhanYuYe_model(data6_1, stock_code)
    #以逸待劳
    isAn_YiYiDaiLao_model(data6_1, stock_code)

    # 晓波 SCS1
    isAn_SCS_1_model(data6_1, stock_code)
    # 死灰复燃
    isAn_SiHuiFuRan_model(data6_1, stock_code)
    # 柳暗花明 底部强势上涨  , 每天标记 ,后期出现 等模型可以加仓
    isAn_LiuAnHuaMing2_model(data6_1, stock_code)
    # 见龙在田1 判断 3个 K 线 , 一阳一阴一阳
    # isAn_JianLongZaiTian1_model(data6_1, stock_code)


    # 结界, 后期有账户再操作
    isAn_JieJie_model(data6_1, stock_code)
    #起爆均线 1
    isAn_QiBaoJunXian1_model(data6_1, stock_code)
    #起爆均线 2
    isAn_QiBaoJunXian2_model(data6_1, stock_code)
    # 起爆均线 3
    isAn_QiBaoJunXian3_model(data6_1, stock_code)


    #雾里看花, 特殊的十字星 还没验证
    isAn_WuLiKanHua_model(data6_1, stock_code)


    #看跌做涨 上涨结构 抄底 尾盘买入
    isAn_KanDieZuoZhang_model(data6_1, stock_code)
    # 飞龙在天, 是萧先生 所有模型里边,挣钱最多, 最快的一个.  胜率最高的
    isAn_FeiLongZaiTian_model(data6_1, stock_code)
    #反客为主 上涨 一天强势洗盘 胜率 80%
    isAn_FanKeWeiZhu_model(data6_1, stock_code)
    #反客为主plus
    isAn_FanKeWeiZhu_Plus_model(data6_1, stock_code)

    # 一箭双雕 复盘 8 月份 94% 的成功率
    isAn_YiJianShuangDiao_model(data6_1, stock_code)
    #大有模型
    isAn_DaYou_model(data6_1, stock_code)


    #  神龙摆尾1 神1
    isAn_Shen1_model(data6_1, stock_code)  #pro
    #  神龙摆尾3 神3
    isAnShenLongBaiwei3_model(data6_1, stock_code)



    #隔山打牛
    isAn_GeShanDaNiu_model(data6_1, stock_code)

    # 熊市末期亢龙有悔 个股上的应用:
    isAn_KangLongYouHui_GeGu_model(data6_1, stock_code)

    #一阳穿多均
    # isAn_YiYangChuanDuoJun_model(data6_1, stock_code)


'''
明天要盯盘的任务
'''
def task2(data6_1,stock_code):
        # 峰回路转  当天条件挂单
        isAn_FengHuiLuZhuan_model(data6_1, stock_code)
        # 飞龙在天2, 超短线  第 3 天盯收盘价 高过小 K 线实体买入
        # isAn_FeiLongZaiTian2_model(data6_1, stock_code)
        # 龙战于野2 找 2 天的数据, 第 3 天盯盘
        # isAn_LongZhanYuYe2_model(data6_1, stock_code)
        # 见龙在田2  第 3 天买入
        # isAn_JianLongZaiTian2_model(data6_1, stock_code)
        # 以逸待劳2前 5 天满足模型, 第 6 天盯盘
        isAn_YiYiDaiLao2_model(data6_1, stock_code)

'''
不经常用的
'''
def task3(data6_1,stock_code):

    # 神龙摆尾0
    isAn_ShenLongBaiWei0_model(data6_1, stock_code)
    #12 九死一生(1)底部强势反转
    isAn_jiusiyisheng1_model(data6_1, stock_code)
    #13 九死一生(2)底部弱势反转
    isAn_JiuSiYiSheng_2_model(data6_1, stock_code)

    #有惊无险 2-1 2021年10月25日 get_all_YouJingWuXian2_1(localpath1):
    isAn_YouJingWuXian2_1_model(data6_1, stock_code)
    #有惊无险 1 2021年10月25日
    isAn_YouJingWuXian1_model(data6_1, stock_code)


'''
还没有改进的
'''
def task4():
    #0  上证 50 上证指数  大盘亢龙有悔
    get_all_KangLongYouHui_DaPan()
    # 神龙摆尾2
    get_all_ShenLongBaiWei2(localpath1)  # 改起来有点复杂

    # 神龙摆尾4
    get_all_ShenLongBaiWei4(localpath1)  # 改起来有点复杂

    #否极泰来 97% 的超高胜率
    get_all_PiJiTaiLai(localpath1)

    # 9 蜻蜓点水  缺口理论
    get_all_QingTingDianShui(localpath1)
    # 10 凌波微步  缺口理论  模板
    get_all_LingBoWeiBu(localpath1)


    # 15 葛式八法
    # getallstockdata_is_GeShi_8fa()
    # 未来节约时间 不运行一下程序 2021年11月29日

    #  5-13-34 日均线组合
    # get_all_5_13_34(localpath1)
    #2 七星落长空 1
    # getallstockdata_is7start_FromLocal(localpath1=localpath1)
    # 七星落长空 2
    # getallstockdata_is7start2_FromLocal(localpath1)
    #7  双龙取水 模型
    # getallstockdata_is_ShuangLong_Qushui_FromLocal(localpath1)

    # 14 有钱君-120-250 均线交易法
    get_all_120_250()

    #通过分析每天的日志,得到 一只股票出现 2 次模型的 个股
    get_2stockcode()




if __name__ == '__main__':
    from  time import  *
    starttime = time()

    localpath1 = '/jishu_stock/stockdata/data1/'
    yijianyunxing()
    # task2(localpath1)
    # test()

    # zzys=2



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"