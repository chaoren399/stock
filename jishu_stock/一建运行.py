#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from jishu_stock.ChuShuiFuRong.ChuShuiFuRong import get_all_ChuShuiFuRong
from jishu_stock.DaYou.DaYou import get_all_DaYou
from jishu_stock.FanKeWeiZhu.FanKeWeiZhu import get_all_FanKeWeiZhu
from jishu_stock.FeiLongZaiTian.FeiLongZaiTian import get_all_FeiLongZaiTian
from jishu_stock.FengHuiLuZhuan.FengHuiLuZhuan import get_all_FengHuiLuZhuan
from jishu_stock.JiuSiYiSheng.jiusiyisheng1 import get_all_jiusiyisheng1
from jishu_stock.KanDieZuoZhang.KanDieZuoZhang import get_all_KanDieZuoZhang
from jishu_stock.KangLongyouHui.KangLongYouHuiGeGu import get_all_KangLongYouHui_GeGu
from jishu_stock.KangLongyouHui.KangLongYouHui_DaPan import get_all_KangLongYouHui_DaPan
from jishu_stock.LiuAnHuaMing.LiuAnHuaMing import get_all_LiuAnHuaMing
from jishu_stock.LongZhan_YuYe.LongZhanYuYe import get_all_LongZhanYuYe
from jishu_stock.PiJiTaiLai.PiJiTaiLai import get_all_PiJiTaiLai
from jishu_stock.Tool_jishu_stock import get_2stockcode
from jishu_stock.WuLiKanHua.WuLiKanHua import get_all_WuLiKanHua
from jishu_stock.YouJingWuXian.YouJingWuXian1 import get_all_YouJingWuXian1
from jishu_stock.YouJingWuXian.YouJingWuXian2 import get_all_YouJingWuXian2_1
from jishu_stock.bQiXingLuoChangKong.QiXingluochangkong1 import getallstockdata_is7start_FromLocal
from jishu_stock.bQiXingLuoChangKong.QiXingluochangkong2 import getallstockdata_is7start2_FromLocal
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei1 import  getall_ShenLongBaiWei1
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei0 import get_all_isShenLongBaiWei0
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei2 import get_all_ShenLongBaiWei2
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei3 import get_all_ShenLongBaiWei3
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei4 import get_all_ShenLongBaiWei4
from jishu_stock.VXingFanZhuan.VXingFanzhuan_all import getallstockdata_isV_fromLocal
from jishu_stock.ShuangLong_Qushui.ShuangLong_Qushui import getallstockdata_is_ShuangLong_Qushui_FromLocal
from jishu_stock.getAllStockData import getAllStockData
from jishu_stock.QingTingDianShui_QueKou.QueKou_QingTingDianShui import get_all_QingTingDianShui
from jishu_stock.LingBoWeiBu.LingBoWeiBu import get_all_LingBoWeiBu
from jishu_stock.JiuSiYiSheng.JiuSiYiSheng2 import get_all_JiuSiYiSheng_2
from jishu_stock.YiYiDaiLao.YiYiDaiLao import get_all_YiYiDaiLao
from jishu_stock.YiJIanShuangDiao.YiJianShuangDiao import get_all_YiJianShuangDiao
from jishu_stock.zYouQianJun.YouQianJun120_250 import get_all_120_250
from jishu_stock.RiJunXianZuhe.RiJunXianZuHe import get_all_5_13_34


def yijianyunxing():

    # 日线 操作

    localpath1 = '/jishu_stock/stockdata/data1/'

    today = starttime.strftime('%Y%m%d')

    getAllStockData(start_date='20200701', end_date=today, localpath=localpath1) #这个时间 提供一年的得到 MA34

    #  5-13-34 日均线组合
    get_all_5_13_34(localpath1)
    #有惊无险 2-1 2021年10月25日 get_all_YouJingWuXian2_1(localpath1):
    get_all_YouJingWuXian2_1(localpath1)
    #有惊无险 1 2021年10月25日
    get_all_YouJingWuXian1(localpath1)
    #出水芙蓉 主力底部强势洗盘
    get_all_ChuShuiFuRong(localpath1)
    #柳暗花明 底部强势上涨
    get_all_LiuAnHuaMing(localpath1)
    #看跌做涨 上涨结构 抄底 尾盘买入
    get_all_KanDieZuoZhang(localpath1)
    # 飞龙在天, 是萧先生 所有模型里边,挣钱最多, 最快的一个.  胜率最高的
    get_all_FeiLongZaiTian(localpath1)
    #反客为主 上涨 一天强势洗盘 胜率 80%
    get_all_FanKeWeiZhu(localpath1)
    #0  上证 50 上证指数  大盘亢龙有悔
    get_all_KangLongYouHui_DaPan()
    # 1 V型 反转
    getallstockdata_isV_fromLocal(localpath1)
    # 一箭双雕 复盘 8 月份 94% 的成功率
    get_all_YiJianShuangDiao(localpath1)
    #大有模型
    get_all_DaYou(localpath1)
    # 8 龙战于野
    get_all_LongZhanYuYe(localpath1)

    # 熊市末期亢龙有悔 个股上的应用:
    get_all_KangLongYouHui_GeGu(localpath1)
    # 2以逸待劳  完美符合模型, 第 6 天阳线收盘
    get_all_YiYiDaiLao(localpath1)

    #否极泰来 97% 的超高胜率
    get_all_PiJiTaiLai(localpath1)

    # 神龙摆尾0
    get_all_isShenLongBaiWei0(localpath1)
    #  神龙摆尾1
    getall_ShenLongBaiWei1(localpath1)

    # 神龙摆尾2
    get_all_ShenLongBaiWei2(localpath1)
    #  神龙摆尾3
    get_all_ShenLongBaiWei3(localpath1)

    #峰回路转  当天条件挂单
    get_all_FengHuiLuZhuan(localpath1)
    # 神龙摆尾4
    get_all_ShenLongBaiWei4(localpath1)

    #12 九死一生(1)底部强势反转
    get_all_jiusiyisheng1(localpath1)
    #13 九死一生(2)底部弱势反转
    get_all_JiuSiYiSheng_2(localpath1)
    # 9 蜻蜓点水  缺口理论
    get_all_QingTingDianShui(localpath1)
    # 10 凌波微步  缺口理论  模板
    get_all_LingBoWeiBu(localpath1)
    #2 七星落长空 1
    getallstockdata_is7start_FromLocal(localpath1=localpath1)
    # 七星落长空 2
    getallstockdata_is7start2_FromLocal(localpath1)




    # 15 葛式八法
    # getallstockdata_is_GeShi_8fa()

    #7  双龙取水 模型
    getallstockdata_is_ShuangLong_Qushui_FromLocal(localpath1)


    #雾里看花, 特殊的十字星 还没验证
    get_all_WuLiKanHua(localpath1)

    # 14 有钱君-120-250 均线交易法
    get_all_120_250()

    #通过分析每天的日志,得到 一只股票出现 2 次模型的 个股
    get_2stockcode()




if __name__ == '__main__':
    starttime = datetime.datetime.now()

    yijianyunxing()


    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print str((endtime - starttime).seconds/60) + "分钟"