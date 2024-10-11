#!/usr/bin/python
# -*- coding: utf8 -*-
import sys
import os

from jishu_stock.bRuoFeng.youzimodel.fancuiruo_shuangxiangpao import isAn_fancuiruo_shuangxiangpao_model
from jishu_stock.bRuoFeng.youzimodel.lizhuang_fanbao import isAn_lizhuang_fanbao_model

# from jishu_stock.agetdata.test_ziji_model.ZTB.ZTB_Yin_Yang_Yin.ZTB_Yin_Yang_Yin import get_all_ZTB_Yin_Yang_Yin

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_parent_dir_name = os.path.dirname(os.path.dirname(current_dir))
# print current_dir
print(parent_parent_dir_name)
sys.path.append(parent_parent_dir_name)


from jishu_stock.agetdata.test_ziji_model.XiaoV.XiaoV import get_all_XiaoV_from_Qiang_QuShi, isAn_XiaoV_model
from jishu_stock.z_tool.email import webhook
import pandas as pd
from jishu_stock.DaPan.DaPan_HuanJing import get_DaPan_HuanJing
from jishu_stock.GeShiBaFa.G8M2_RuanAll import G8M2_yijianyunxing
from jishu_stock.JiaGeZhongShu.JGZS_RuanAll import JGZS_yijianyunxing
from jishu_stock.KangLongyouHui.KangLongYouHui_DaPan import get_all_KangLongYouHui_DaPan
from jishu_stock.Tool_jishu_stock import get_all_codes_from_tool, \
    csv_paixu_path1_zhuanyong
from jishu_stock.YouJingWuXian.YouJingWuXian1 import isAn_YouJingWuXian1_model
from jishu_stock.YouJingWuXian.YouJingWuXian2_1 import isAn_YouJingWuXian2_1_model
from jishu_stock.YouJingWuXian.YouJingWuXian2_2 import isAn_YouJingWuXian2_2_model
from jishu_stock.YouJingWuXian.YouJingWuXian2_3 import isAn_YouJingWuXian2_3_model
from jishu_stock.agetdata.getdata_2theard import get_all_codes
from jishu_stock.bRuoFeng.youzimodel.erlianban_damian_fanbao_guchi import isAn_lianban_damian_fanbao_model
from jishu_stock.cShenLongBaiWei.Shen1 import isAn_Shen1_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei2 import get_all_ShenLongBaiWei2
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei2_Pro import isAn_ShenLongBaiWei2_Pro_model
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei4 import get_all_ShenLongBaiWei4
from jishu_stock.cShenLongBaiWei.ShenLongBaiWei4_1 import get_all_ShenLongBaiWei4_1
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
def yijianyunxing_jiagezhongshu():
    JGZS_yijianyunxing()

'''
日线 一键运行
平时下午 4 点准时更新
周五数据延迟, 5:58 可以下载
'''
def yijianyunxing_rixian():

    today = getDayNumberYMD()

    webhook.sendData("开始下载数据--"+ today)
    print  '-----大盘环境------'+ get_DaPan_HuanJing(today)
    # 日线 操作
    localpath1 = '/jishu_stock/z_stockdata/data1/'



    get_all_codes() #下载所有 股票数据

    getXiaoV()
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
        # task2(data6_1, stock_code)
        # task3(data6_1, stock_code)
        # task6(data6_1, stock_code) # 有惊无险的 专用方法


    endtime = time()
    print "task1,2,3 总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"
    # task4_teshu()
    csv_paixu_path1_zhuanyong()

    #根据股票代码 获取 当天是不是价格中枢
    # GetToday_JGZS()


    webhook.sendData("--all 执行完毕--" )

def getXiaoV():
    localpath1 = '/jishu_stock/z_stockdata/data1/'
    get_all_XiaoV_from_Qiang_QuShi(localpath1)

"""
主要是 今天要看的模型数据
"""
def task1(data6_1,stock_code):

    # 二连板大面反包
    isAn_lianban_damian_fanbao_model(data6_1, stock_code)
     # 立桩反包
    isAn_lizhuang_fanbao_model(data6_1, stock_code)
    # 反脆弱双响炮
    isAn_fancuiruo_shuangxiangpao_model(data6_1, stock_code)

    #  神龙摆尾1 神1
    isAn_Shen1_model(data6_1, stock_code)

    # 神1  6天数据模型
    # isAn_Shen1_Pro_model(data6_1, stock_code)  #pro  济民医疗
    # 神2pro 改进版, 之前的有些拿不到
    isAn_ShenLongBaiWei2_Pro_model(data6_1, stock_code)
    #  神龙摆尾3 神3
    # isAnShenLongBaiwei3_model(data6_1, stock_code)


'''
目前精力不放在这里的
'''
def task5(data6_1,stock_code):
    # 1 V型 反转
    # isAnV_model(data6_1, stock_code)
    # 8 龙战于野
    # isAn_LongZhanYuYe_model(data6_1, stock_code)
    # 以逸待劳
    # isAn_YiYiDaiLao_model(data6_1, stock_code)
    # xiaoV
    isAn_XiaoV_model(data6_1,stock_code)

    # 海底捞
    # isAn_HaiDiLao_model(data6_1,stock_code)

    # 岛型反转缺口  大盘 破 20 日均线才可以做
    # isAn_DaoXingQueKou_model(data6_1, stock_code)

    # 建仓破绽 洗盘模型
    # isAn_JianCangPoZhan_model(data6_1, stock_code)

    # 筹码突破
    # isAn_ChouMaTuPo_model(data6_1, stock_code)
    # 短线强庄股2
    # isAn_DuanXianQiangZhuangGu2_model(data6_1, stock_code)
    # 短线强庄股
    # isAn_DuanXianQiangZhuangGu_model(data6_1, stock_code)

    # 阴错阳差
    # isAn_YinCuoYangCha_model(data6_1, stock_code)

    # 见龙在田5
    # isAn_JianLongZaiTian5_model(data6_1, stock_code)

    # 出水芙蓉 主力底部强势洗盘
    # isAn_ChuShuiFuRong_model(data6_1, stock_code)

    # 飞龙在天, 是萧先生 所有模型里边,挣钱最多, 最快的一个.  胜率最高的
    # isAn_FeiLongZaiTian_model(data6_1, stock_code)
    # 反客为主 上涨 一天强势洗盘 胜率 80%
    # isAn_FanKeWeiZhu_model(data6_1, stock_code)
    # 反客为主plus
    # isAn_FanKeWeiZhu_Plus_model(data6_1, stock_code)

    # 一箭双雕 复盘 8 月份 94% 的成功率
    # isAn_YiJianShuangDiao_model(data6_1, stock_code)
    # 大有模型
    # isAn_DaYou_model(data6_1, stock_code)

    # 隔山打牛
    # isAn_GeShanDaNiu_model(data6_1, stock_code)

    # 熊市末期亢龙有悔 个股上的应用:
    # isAn_KangLongYouHui_GeGu_model(data6_1, stock_code)

    # 晓波 SCS1
    # isAn_SCS_1_model(data6_1, stock_code)

    # 见龙在田1 判断 3个 K 线 , 一阳一阴一阳
    # isAn_JianLongZaiTian1_model(data6_1, stock_code)

    # 结界, 后期有账户再操作
    # isAn_JieJie_model(data6_1, stock_code)

    #看跌做涨 上涨结构 抄底 尾盘买入
    # isAn_KanDieZuoZhang_model(data6_1, stock_code)

    # 早晨之星2 十字星下影线比实体大 1.5 倍
    # isAn_ZaoChenZhiXing2_model(data6_1, stock_code)


    #一阳穿多均
    # isAn_YiYangChuanDuoJun_model(data6_1, stock_code)



    #涨停板后 跳空的大阴线
    # isAn_ZTB_YinXian_TiaoKong_model(data6_1, stock_code)

    #李栋 追击一字板
    # isAn_ZhuiJiYiZiBan_model (data6_1, stock_code)
    #涨停板后 跳空的小阴线, 胜率 70%
    # isAn_ZTB_YinXian_TiaoKong_model(data6_1, stock_code)

    #N型反转
    # isAn_NXingFanZhuan_model(data6_1, stock_code)
    #塔形底
    # isAn_TaXingDi_model(data6_1, stock_code)
    #早晨之星 十字星实体 小于 0.6
    # isAn_ZaoChenZhiXing_model(data6_1, stock_code)

    #VOL阴尽阳生 , 回调低吸大法,抄底
    # isAn_VOLYinJinYangSheng_model(data6_1, stock_code)

    #5连阳,开盘价依次提高
    # isAn_5LianYang_model(data6_1, stock_code)

    # 4阳+ 1个涨停板
    # isAn_4Yang1ZTB_model(data6_1, stock_code)

    #堆量 为了找小阳建仓
    # isAn_DuiLiang1_model(data6_1, stock_code)
    #小阳建仓1
    # isAn_XiaoYangJianCang_model(data6_1, stock_code)
    #反包 1 记住那一句话，该弱的不弱必强
    # isAn_FanBao1_model(data6_1, stock_code)


    print 'task4目前精力不放在这里的运行完了'

'''
有惊无险 4 个方法 + 起爆均线 4 个
'''
def task6(data6_1,stock_code):
    #有惊无险1
    isAn_YouJingWuXian1_model(data6_1,stock_code)
    #有惊无险2-1
    isAn_YouJingWuXian2_1_model(data6_1, stock_code)
    # 有惊无险2-2
    isAn_YouJingWuXian2_2_model(data6_1, stock_code)
    # 有惊无险2-3
    isAn_YouJingWuXian2_3_model(data6_1, stock_code)


    #起爆均线 1
    # isAn_QiBaoJunXian1_model(data6_1, stock_code)
    #起爆均线 2
    # isAn_QiBaoJunXian2_model(data6_1, stock_code)
    # 起爆均线 3
    # isAn_QiBaoJunXian3_model(data6_1, stock_code)
    #起爆均线4 胜率 80%
    # isAn_QiBaoJunXian4_model(data6_1, stock_code)



'''
明天要盯盘的任务
'''
def task2(data6_1,stock_code):
        # 峰回路转  当天条件挂单
        # isAn_FengHuiLuZhuan_model(data6_1, stock_code)
        # 飞龙在天2, 超短线  第 3 天盯收盘价 高过小 K 线实体买入
        # isAn_FeiLongZaiTian2_model(data6_1, stock_code)
        # 龙战于野2 找 2 天的数据, 第 3 天盯盘
        # isAn_LongZhanYuYe2_model(data6_1, stock_code)
        # 见龙在田2  第 3 天买入
        # isAn_JianLongZaiTian2_model(data6_1, stock_code)
        # 以逸待劳2前 5 天满足模型, 第 6 天盯盘
        # isAn_YiYiDaiLao2_model(data6_1, stock_code)

        print 'task2'

'''
抄底模型
'''
def task3(data6_1,stock_code):

    # 神龙摆尾0
    # isAn_ShenLongBaiWei0_model(data6_1, stock_code)
    #12 九死一生(1)底部强势反转
    # isAn_jiusiyisheng1_model(data6_1, stock_code)
    #13 九死一生(2)底部弱势反转
    # isAn_JiuSiYiSheng_2_model(data6_1, stock_code)


    # 死灰复燃
    # isAn_SiHuiFuRan_model(data6_1, stock_code)
    # 柳暗花明 底部强势上涨  , 每天标记 ,后期出现 等模型可以加仓
    # isAn_LiuAnHuaMing2_model(data6_1, stock_code)

    #雾里看花, 特殊的十字星 还没验证
    # isAn_WuLiKanHua_model(data6_1, stock_code)



    print 'task3'


'''
还没有改进的 不能用于循环的模型
'''
def task4_teshu():
    #0  上证 50 上证指数  大盘亢龙有悔
    get_all_KangLongYouHui_DaPan()
    # 神龙摆尾2
    get_all_ShenLongBaiWei2(localpath1)  # 改起来有点复杂

    # 神龙摆尾4 神4
    get_all_ShenLongBaiWei4(localpath1)  # 改起来有点复杂
    get_all_ShenLongBaiWei4_1(localpath1)#成交量 改为 vol 之前的都是 amount 搞错了

    #否极泰来 97% 的超高胜率
    # get_all_PiJiTaiLai(localpath1)

    # 9 蜻蜓点水  缺口理论
    # get_all_QingTingDianShui(localpath1)
    # 10 凌波微步  缺口理论  模板
    # get_all_LingBoWeiBu(localpath1)


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
    # get_all_120_250()

    #通过分析每天的日志,得到 一只股票出现 2 次模型的 个股
    # get_2stockcode()




if __name__ == '__main__':
    from  time import  *
    starttime = time()
    ts.set_token('0c9acbe761612301ff2baaa9b3e8ec4053150ad1c1fb0e7b6d53bd5d')

    localpath1 = '/jishu_stock/z_stockdata/data1/'

    yijianyunxing_rixian()


    endtime = time()
    print "总共运行时长:" + str(round((endtime - starttime) / 60, 2)) + "分钟"