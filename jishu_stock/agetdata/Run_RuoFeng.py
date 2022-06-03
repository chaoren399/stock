#!/usr/bin/python
# -*- coding: utf8 -*-

import pandas as pd

from jishu_stock.ChuShuiFuRong.ChuShuiFuRong import isAn_ChuShuiFuRong_model
from jishu_stock.DaPan.DaPan_HuanJing import get_DaPan_HuanJing
from jishu_stock.DaYou.DaYou import isAn_DaYou_model
from jishu_stock.FanKeWeiZhu.FanKeWeiZhu import isAn_FanKeWeiZhu_model
from jishu_stock.FanKeWeiZhu.FanKeWeiZhu_Plus import isAn_FanKeWeiZhu_Plus_model
from jishu_stock.FeiLongZaiTian.FeiLongZaiTian import isAn_FeiLongZaiTian_model
from jishu_stock.FengHuiLuZhuan.FengHuiLuZhuan import isAn_FengHuiLuZhuan_model
from jishu_stock.GeShanDaNiu.GeShanDaNiu import isAn_GeShanDaNiu_model
from jishu_stock.GeShiBaFa.G8M2_RuanAll import G8M2_yijianyunxing
from jishu_stock.JiaGeZhongShu.GetToday_JGZS import GetToday_JGZS
from jishu_stock.JiaGeZhongShu.JGZS_RuanAll import JGZS_yijianyunxing
from jishu_stock.JianLongZaiTian.JianLongZaiTian5 import isAn_JianLongZaiTian5_model
from jishu_stock.JieJie.JieJie import isAn_JieJie_model
from jishu_stock.JiuSiYiSheng.jiusiyisheng1 import isAn_jiusiyisheng1_model
from jishu_stock.KanDieZuoZhang.KanDieZuoZhang import isAn_KanDieZuoZhang_model
from jishu_stock.KangLongyouHui.KangLongYouHuiGeGu import isAn_KangLongYouHui_GeGu_model
from jishu_stock.KangLongyouHui.KangLongYouHui_DaPan import get_all_KangLongYouHui_DaPan
from jishu_stock.LiuAnHuaMing.LiuAnHuaMing2 import isAn_LiuAnHuaMing2_model
from jishu_stock.LongZhan_YuYe.LongZhanYuYe import isAn_LongZhanYuYe_model
from jishu_stock.PiJiTaiLai.PiJiTaiLai import get_all_PiJiTaiLai
from jishu_stock.QiBaoJunXian.QiBaoJunXian1 import isAn_QiBaoJunXian1_model
from jishu_stock.QiBaoJunXian.QiBaoJunXian2 import isAn_QiBaoJunXian2_model
from jishu_stock.QiBaoJunXian.QiBaoJunXian3 import isAn_QiBaoJunXian3_model
from jishu_stock.QiBaoJunXian.QiBaoJunXian4 import isAn_QiBaoJunXian4_model
from jishu_stock.SiHuiFuRan.SiHuiFuRan import isAn_SiHuiFuRan_model
from jishu_stock.Tool_jishu_stock import get_2stockcode, get_all_codes_from_tool, \
    csv_paixu_path1_zhuanyong
from jishu_stock.WuLiKanHua.WuLiKanHua import isAn_WuLiKanHua_model
from jishu_stock.YiYiDaiLao.YiYiDaiLao0 import isAn_YiYiDaiLao2_model
from jishu_stock.YinCuoYangCha.YinCuoYangCha import isAn_YinCuoYangCha_model
from jishu_stock.YouJingWuXian.YouJingWuXian1 import isAn_YouJingWuXian1_model
from jishu_stock.YouJingWuXian.YouJingWuXian2_1 import isAn_YouJingWuXian2_1_model
from jishu_stock.YouJingWuXian.YouJingWuXian2_2 import isAn_YouJingWuXian2_2_model
from jishu_stock.YouJingWuXian.YouJingWuXian2_3 import isAn_YouJingWuXian2_3_model
from jishu_stock.agetdata.getdata_2theard import get_all_codes
from jishu_stock.agetdata.test_ziji_model.ZTB_XiaoYinXian_TiaoKong import isAn_ZTB_YinXian_TiaoKong_model
from jishu_stock.bCaoMaoGui.NXingFanZhuan import isAn_NXingFanZhuan_model
from jishu_stock.bCaoMaoGui.TaXingDi import isAn_TaXingDi_model
from jishu_stock.bCaoMaoGui.ZaoChenZhiXing import isAn_ZaoChenZhiXing_model
from jishu_stock.bChanKe.ChouMaTuPo import isAn_ChouMaTuPo_model
from jishu_stock.bChanKe.JianCangPoZhan import isAn_JianCangPoZhan_model
from jishu_stock.bChanKe.quekou.DaoXingQueKou import isAn_DaoXingQueKou_model
from jishu_stock.bRuoFeng.HaiDiLao import isAn_HaiDiLao_model
from jishu_stock.bWuWei.DuiLiang1 import isAn_DuiLiang1_model
from jishu_stock.bWuWei.FanBao1 import isAn_FanBao1_model
from jishu_stock.bWuWei.VOLYinJinYangSheng import isAn_VOLYinJinYangSheng_model
from jishu_stock.bWuWei.Wu_LianYang import isAn_5LianYang_model
from jishu_stock.bWuWei.XiaoYangJianCang import isAn_XiaoYangJianCang_model
from jishu_stock.bWuWei.Yang4_1ZhangTB import isAn_4Yang1ZTB_model
from jishu_stock.bWuWei.ZhuiJiYiZiBan import isAn_ZhuiJiYiZiBan_model
from jishu_stock.b_xiaogujiang.DuanXianQiangZhuangGu import isAn_DuanXianQiangZhuangGu_model
from jishu_stock.b_xiaogujiang.DuanXianQiangZhuangGu2 import isAn_DuanXianQiangZhuangGu2_model
from jishu_stock.cShenLongBaiWei.Shen1 import isAn_Shen1_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei0 import isAn_ShenLongBaiWei0_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei2 import get_all_ShenLongBaiWei2
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei2_Pro import isAn_ShenLongBaiWei2_Pro_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei3 import isAnShenLongBaiwei3_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei4 import get_all_ShenLongBaiWei4
from jishu_stock.VXingFanZhuan.VXingFanzhuan_all import isAnV_model
from jishu_stock.QingTingDianShui_QueKou.QueKou_QingTingDianShui import get_all_QingTingDianShui
from jishu_stock.LingBoWeiBu.LingBoWeiBu import get_all_LingBoWeiBu
from jishu_stock.JiuSiYiSheng.JiuSiYiSheng2 import isAn_JiuSiYiSheng_2_model
from jishu_stock.YiYiDaiLao.yiyidailaoAll.YiYiDaiLao0 import isAn_YiYiDaiLao_model
from jishu_stock.YiJIanShuangDiao.YiJianShuangDiao import isAn_YiJianShuangDiao_model
from jishu_stock.cShenLongBaiWei.Shen1_Pro import isAn_Shen1_Pro_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei4_1 import get_all_ShenLongBaiWei4_1
from jishu_stock.zYouQianJun.YouQianJun120_250 import get_all_120_250
from jishu_stock.z_tool.PyDateTool import getDayNumberYMD

from stock.settings import BASE_DIR
import tushare as ts

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
    today = getDayNumberYMD()
    print  '-----大盘环境------'+ get_DaPan_HuanJing(today)
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



    endtime = time()
    print "task1,2,3 总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"




"""
主要是 今天要看的模型数据
"""
def task1(data6_1,stock_code):

    #海底捞
    isAn_HaiDiLao_model(data6_1,stock_code)



if __name__ == '__main__':
    from  time import  *
    starttime = time()
    ts.set_token('0c9acbe761612301ff2baaa9b3e8ec4053150ad1c1fb0e7b6d53bd5d')

    localpath1 = '/jishu_stock/stockdata/data1/'

    yijianyunxing()



    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"