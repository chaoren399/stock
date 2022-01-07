#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
from time import sleep

import tushare as ts
import sys
import pandas as pd
from jishu_stock.Tool_jishu_stock import dingshi_ceshi, print1, getRiQi_Befor_Ater_Days, writeLog_to_txt_path
from jishu_stock.aShengLv.HuiCeTool import wirteList_to_txt
from stock.settings import BASE_DIR
import sys

reload(sys)
sys.setdefaultencoding('utf8')
'''
第一天买,第 2 天卖的短线玩法

短期买卖的收益率 计算
计算一个符合模型的 股票 收益有多少, 传入 第一天买入价格 和 第 2 天卖出价格
stockcode

'''


FenCang_DaXiao=3000 #分仓的金额 比如, 2万元 分 10 仓,那么 每仓就是 2000 元.


def jisuan_all_shouyilv_one_two(chenggongs, modelname):
    # sleep(20)
    # wirteList_to_txt(chenggongs) # 保存 成功的票

    len_chengogns=len(chenggongs)

    zongde_yingli=0
    chenggong_cishu=0
    shibai_cishu=0

    chenggong_codeinfos=[]  #成功的 股票信息 包含代码以及买入卖出日期
    shibai_codeinfos=[]


    for index, item in enumerate(chenggongs):
        stockcode=item['stockcode']
        mairujiage=item['mairujiage']
        maichujiage=item['maichujiage']
        riqi=item['riqi']
        info= str(stockcode) +':'+str(riqi)

        chajia=maichujiage -mairujiage

        if(mairujiage < maichujiage) : # 收益为正
            chenggong_cishu = chenggong_cishu + 1
            chenggong_codeinfos.append(info)
        elif(maichujiage >= maichujiage): #收益为负
            shibai_cishu = shibai_cishu + 1
            shibai_codeinfos.append(info)
        #  比如我买 2 手, 200 股 * 买入价 如果 <  分仓的金额, 那么我就买 1 手,  就要写一个函数 精准的计算, 买入多少股票
        mairu_gushu= round(FenCang_DaXiao /(mairujiage * 100),0)  #几手
        zongde_yingli = zongde_yingli + (chajia * mairu_gushu*100)  # 这里 要用分仓的概念,  比如每仓 3000 元, 那么, 我盈利,是 3000 / 买入价 这是多少股



    # path = BASE_DIR + '/jishu_stock/sJieGuo/huice/' + datetime.datetime.now().strftime(
        # '%Y-%m-%d') + '.txt'
    path = BASE_DIR + '/jishu_stock/sJieGuo/huice/' + modelname+ '.txt'

    info1=''
    info1=info1+'chenggong_codeinfos'+ str(chenggong_codeinfos) +'\n'
    info1=info1+'shibai_codeinfos'+ str(shibai_codeinfos) +'\n'

    writeLog_to_txt_path(info1, path)

    info="\n"+modelname+'--回测盈利信息 第一天买 第 2 天卖 :'+"\n"
    info=info+ '总的盈利:'+str(round(zongde_yingli,0))+'元' +"\n"  # 改进, 我是分仓进去的, 如果 每仓 3000元.
    info=info+ '成功次数:'+str(chenggong_cishu) +'\n'
    info=info+ '失败次数:'+str(shibai_cishu) +'\n'


    info = info + '所有符合模型的个数:'+str(len_chengogns) +' ,可以手动计算  成功+ 失败+持仓是否 等于该值(限制价格的不会计算在内)'+'\n'

    info = info + '成功+失败:'+str(chenggong_cishu+shibai_cishu) +'\n'


    info = info + '胜率:'+str(round(chenggong_cishu /(chenggong_cishu+shibai_cishu+0.01),3)) +'\n'
    # info = info + '最早买入日期:'+str(zuizao_riqi) +'最后买入日期:'+str(zuihou_riqi)

    print info
    writeLog_to_txt_path(info, path)







def testlinshi():
    mairu_jiage=19
    mairu_gushu = round(FenCang_DaXiao / (mairu_jiage * 100), 0)
    print mairu_gushu


'''
回测的案例 在 出水芙蓉 test_shenglv_zhunquexing()

'''

if __name__ == '__main__':
    print  "定时测试"
    # dingshi_ceshi()
    testlinshi()
