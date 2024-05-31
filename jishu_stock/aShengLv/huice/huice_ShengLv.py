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
计算收益率, 需要知道, 
stockcode
mairuriqi
zhisunddian
zhiyingdian

要再主程序中, 做一个全局数组A, 
满足条件的 就放到这个A 中, 然后 单独调用 计算收益率的 函数, 
可以统计  整体的收益率.



'''

# zhiying_shouyilv=1.05


'''
回测的案例 在 出水芙蓉 test_shenglv_zhunquexing()

'''



'''

计算一个符合模型的 股票 收益有多少, 传入 止盈点, 止损点, 还有买入日期
stockcode

mairu_riqi- 买入的日期
zhisunddian 止损点, 一般是 某个K 线 的最低值
zhiying_shouyilv= 1.05,1.10
'''

IS_YEAR=1  # 计算收益率 不能太快的锁

FenCang_DaXiao=3000 #分仓的金额 比如, 2万元 分 10 仓,那么 每仓就是 2000 元.

def get_shouyi(stockcode, mairu_riqi, zhisunddian,zhiying_shouyilv):
    if(IS_YEAR):
        # sleep(0.05)
        sleep(0.2)
        # sleep(0.12) #  60/500 =0.12

    # if(zhiying_shouyilv is None ):
    #     zhiying_shouyilv=1.05
    # else:
    #     zhiying_shouyilv = zhiying_shouyilv
    zhiying_shouyilv = zhiying_shouyilv

    # df1 = ts.pro_bar(ts_code='002011.SZ', adj='qfq', start_date='20210206', end_date='20211014')
    mairu_riqi= getRiQi_Befor_Ater_Days(mairu_riqi, 1)
    today = datetime.datetime.now().strftime('%Y%m%d')#20211204
    df1 = ts.pro_bar(ts_code=stockcode, start_date=mairu_riqi, end_date=today)
    df1 = df1.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    df1 = df1.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。
    # print1(df1)
    len_df1 = len(df1)
    if (len_df1 == 0):
        print str(stockcode) + '--data --is null'

    if (len_df1 >0):

        # data7_1 = df1.iloc[0:30]  # 前7行
        maichu_riqi = df1.ix[0]['trade_date']  # 阳线的日期
        key1=0 # 标记是否还未到到 止损止盈的 ,还在持仓中

        day1_open=0 # 买入当天的价格
        day_maichu_close=0
        for index,row in df1.iterrows():
            if(index==0):
                day1_open=row['open']
                break
        # zhiyingdian = day1_open * 1.05  # 5% 的收益率止盈
        zhiyingdian = day1_open * zhiying_shouyilv  # 5% 的收益率止盈
        count=0
        for index, row in df1.iterrows():
            openprice=row['open']
            closeprice=row['close']
            count=count+1
            maichu_riqi=row['trade_date']
            if(count < len_df1) : # 截止到今天期间到达止盈点,止损点
                if(openprice <= zhisunddian or closeprice <= zhisunddian):#如果达到 止损点, 卖出
                    day_maichu_close= closeprice
                    break  # 结束 for 循环
                if(openprice >= zhiyingdian or closeprice >= zhiyingdian): #如果达到止盈点, 卖出
                    day_maichu_close = closeprice
                    break
            elif(count==len_df1):# 截止到今天还没到达止盈点,止损点
                # print '# 截止到今天还没到达止盈点,止损点'
                # print1(closeprice)
                # print1(zhisunddian)
                key1=1  # 标记是否还未到到 止损止盈的 ,还在持仓中

        chicang_tianshu=count
        mairu_jiage=day1_open
        maichu_jiage=day_maichu_close
        chajia = (maichu_jiage - mairu_jiage) #卖出价格 - 买入价格



        # print1(chajia)
        # print1(chicang_tianshu)
        #
        # print1(mairu_riqi)
        # print1(maichu_riqi)
        #
        # print1(mairu_jiage)
        # print1(maichu_jiage)
        # print1(zhiyingdian)
        # print1(zhisunddian)

        codeinfo = {'stockcode': stockcode, 'chajia': chajia, 'chicang_tianshu': chicang_tianshu
                       ,'maichu_riqi':maichu_riqi,'mairu_riqi':mairu_riqi ,'key1':key1,
                    'mairu_jiage':mairu_jiage,'maichu_jiage':maichu_jiage}
        return codeinfo


def jisuan_all_shouyilv(chenggongs, modelname, zhiying_shouyilv):
    # sleep(20)
    wirteList_to_txt(chenggongs) # 保存 成功的票

    len_chengogns=len(chenggongs)

    zongde_yingli=0
    chenggong_cishu=0
    shibai_cishu=0
    weizhiyingsun_cishu=0

    chenggong_codeinfos=[]  #成功的 股票信息 包含代码以及买入卖出日期
    shibai_codeinfos=[]
    weizhiyingsun_codeinfos=[]

    zijinzonge=0 # 所需资金, 就是买入价 的总和
    zongde_chicang_tianshu=0 #总的持仓天数
    datais_null=0
    zuizao_riqi=0
    zuihou_riqi=0
    for index, item in enumerate(chenggongs):
        stockcode=item['stockcode']
        mairuriqi=item['mairuriqi']
        zhisundian=item['zhisundian']
        item1= get_shouyi(stockcode, mairuriqi, zhisundian,zhiying_shouyilv)
        if (index == 0):
            zuizao_riqi = item1['maichu_riqi']
            zuihou_riqi = item1['maichu_riqi']

        if(item1): # 得到每一个成功案例的详细收益情况就
            mairu_jiage = item1['mairu_jiage']
            # if(mairu_jiage < 40 and mairu_jiage> 4):  # 目前只统计 小于 30 元的股票 大于 4 元的股票
            if(1):  # 目前只统计 小于 30 元的股票 大于 4 元的股票
                key1 = item1['key1']
                chajia=item1['chajia']
                chicang_tianshu=item1['chicang_tianshu']
                stockcode=item1['stockcode']
                maichu_riqi = item1['maichu_riqi']
                mairu_riqi = item1['mairu_riqi']

                chicang_tianshu = item1['chicang_tianshu']
                zongde_chicang_tianshu=zongde_chicang_tianshu+chicang_tianshu  # 持有天数

                maichu_jiage = item1['maichu_jiage']
                # zijinzonge=zijinzonge+mairu_jiage  #资金总的金额

                codeinfo= stockcode+'--mairu_riq:'+str(mairu_riqi) + '--maichu_riq:'+str(maichu_riqi)
                #计算 最早买入日期和 最后买入如期
                if(mairu_riqi < zuizao_riqi):
                    zuizao_riqi = mairu_riqi
                if(maichu_riqi > zuihou_riqi):
                    zuihou_riqi= mairu_riqi
                if (key1 == 0):
                    if(chajia >0): # 成功的
                        chenggong_cishu=chenggong_cishu+1
                        chenggong_codeinfos.append(codeinfo)
                    elif(chajia <0): #失败的
                        shibai_cishu=shibai_cishu+1
                        shibai_codeinfos.append(codeinfo)
                    else :
                        print codeinfo
                elif(key1==1): # 还在持仓中
                    # print '还在持仓中 '
                    weizhiyingsun_cishu = weizhiyingsun_cishu + 1
                    weizhiyingsun_codeinfos.append(codeinfo)
                    chajia=0

                #  比如我买 2 手, 200 股 * 买入价 如果 <  分仓的金额, 那么我就买 1 手,  就要写一个函数 精准的计算, 买入多少股票
                mairu_gushu= round(FenCang_DaXiao /(mairu_jiage * 100),0)  #几手
                zongde_yingli = zongde_yingli + (chajia * mairu_gushu*100)  # 这里 要用分仓的概念,  比如每仓 3000 元, 那么, 我盈利,是 3000 / 买入价 这是多少股

                zijinzonge = zijinzonge + mairu_jiage * mairu_gushu *100


        else:  #item1 为空 , 为什么为空呢?
            datais_null=datais_null+1

    # path = BASE_DIR + '/jishu_stock/zJieGuo/huice/' + datetime.datetime.now().strftime(
        # '%Y-%m-%d') + '.txt'
    path = BASE_DIR + '/jishu_stock/zJieGuo/huice/' + modelname+ '.txt'

    info1=''
    info1=info1+'chenggong_codeinfos'+ str(chenggong_codeinfos) +'\n'
    info1=info1+'shibai_codeinfos'+ str(shibai_codeinfos) +'\n'
    info1=info1+'weizhiyingsun_codeinfos'+ str(weizhiyingsun_codeinfos) +'\n'
    writeLog_to_txt_path(info1, path)

    info="\n"+modelname+'--回测盈利信息 目标止盈率:'+str(zhiying_shouyilv)+'----日期间隔:'+str(zuizao_riqi) +'--'+str(zuihou_riqi)+"\n"
    info=info+ '总的盈利:'+str(round(zongde_yingli,0))+'元' +"\n"  # 改进, 我是分仓进去的, 如果 每仓 3000元.
    info=info+ '成功次数:'+str(chenggong_cishu) +'\n'
    info=info+ '失败次数:'+str(shibai_cishu) +'\n'
    info=info+ '持仓中的:'+str(weizhiyingsun_cishu) +'\n'

    info = info + '所有符合模型的个数:'+str(len_chengogns) +' ,可以手动计算  成功+ 失败+持仓是否 等于该值(限制价格的不会计算在内)'+'\n'
    info = info + '符合模型 中数据为空的个数:'+str(datais_null) +'\n'
    info = info + '成功+失败+未止损盈:'+str(chenggong_cishu+shibai_cishu+weizhiyingsun_cishu) +'\n'
    info = info + '平均持仓天数:'+str(zongde_chicang_tianshu / (len_chengogns+0.1)) +'\n'
    info = info + '所需资金总额:'+str( round(zijinzonge/10000,2))+'万元' +'\n'
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
