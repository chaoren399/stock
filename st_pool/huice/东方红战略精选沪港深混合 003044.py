#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from stock.settings import BASE_DIR
import pandas as pd
import openpyxl

'''
东方红战略精选混合A(003044) 失误的一次啊

'''

fundname = "东方红战略精选混合A"
fundcode = '003044'

startdate = '2021-05-30'
enddate = '2021-07-06'
dstart = datetime.datetime.strptime(startdate, '%Y-%m-%d')
dend = datetime.datetime.strptime(enddate, '%Y-%m-%d')

def data_chuli():

    oldfunddatapath = BASE_DIR + '/st_pool' + '/get_fund_data/' + 'fund_old_data/'
    df = pd.read_csv(oldfunddatapath+'other/'+fundcode+'/'+fundcode+'.csv', dtype=object, header=None)
    df.columns = ['date', 'value']
    df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

    # 因为下载的数据没有周末的数据, 为了方便定投计算, 缺失数据 补齐
    # 设置索引
    df_date = df_new.set_index("date")
    # 将df的索引设置为日期索引
    df_date = df_date.set_index(pd.to_datetime(df_date.index))
    # 生成完整的日期序列
    date_range = pd.date_range(start=startdate, end=enddate, normalize=True)
    # 填充缺失索引，
    df_date_new = df_date.reindex(date_range, axis=0)
    df_date_new = df_date_new.fillna(method='ffill', axis=0)
    df_new = df_date_new
    return df_new

def data_show_050002_celue( ):
    df_new=data_chuli()  #得到处理的原始数据
    T=0
    onerate=0
    fene=0
    data = []
    count = 0
    zongtouru =0 #总投入
    shouyilv=0 # 收益率
    yingli = 0  #盈利金额
    maxzijinliang=0 #最大资金量
    isjiama=0 # 是否加码
    jiamacishu=0
    ismaichu=0 #是否卖出
    maichucishu=0

    for index, row in df_new.iterrows():
            ismaichu=0
            isjiama=0
            date = str(index)

            d1 = date [0:10]
            date = d1
            d1 = datetime.datetime.strptime(d1, '%Y-%m-%d')

            if (d1 > dstart and d1 < dend): #// 过滤日期
                # //处理日期
                x = date.split("-", 2)
                anyday = datetime.datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%w")

                if (anyday == '1'):  # 选择周五的数据
                    value = row['value']
                    value= float(value)
                    fene= 500/value +fene
                    zongtouru = zongtouru+500

                    shouyilv =float((fene * value) - zongtouru)/zongtouru  #// 收益率
                    print "shouyilv==" + str(shouyilv)
                    print "fene * value==" + str(fene * value)
                    print "zongtouru==" + str(zongtouru)
                    print "0/500==" + str(0/500)
                    print "0/500==" + str(int(shouyilv))


                    if (shouyilv < -110): #//收益率为负 加码
                        jiamajine = zongtouru*0.2
                        zongtouru = jiamajine+zongtouru
                        isjiama=1
                        if(zongtouru > maxzijinliang):
                            maxzijinliang = zongtouru
                        fene= fene+jiamajine/value
                        jiamacishu= jiamacishu+1
                        print "收益率为负:"
                    if(shouyilv > 0.4): #(如果收益率大于 10% 全部卖出
                        # yingli = yingli+(fene * value - zongtouru)
                        ismaichu=1;
                        fene=0
                        zongtouru=0
                        shouyilv=0
                        maichucishu=maichucishu+1
                        print "收益率为大于 10% "

                    xx = [str(date), value, shouyilv, zongtouru, ismaichu,isjiama]
                    print "zongtouru==" + str(zongtouru)
                    yingli = yingli + (fene * value - zongtouru)
                    data.append(xx)
                    count= count+1
    print data

    print "定投次数为: "+str(count) +"次"
    print "加码次数为: "+str(jiamacishu) +"次"
    print "卖出次数为: "+str(maichucishu) +"次"
    print "收益率 = "+str(shouyilv)
    # print "总投入="+str(zongtouru)
    print "盈利="+str(yingli)
    print "最大资金量=" + str(maxzijinliang)
    print "基金代码:"+fundcode +'--'+ fundname
    print  "回测周期: " + startdate + "~" + enddate +"----有策略--"
    # python  数组转表格
    a_pd = pd.DataFrame(data)
    # create writer to write an excel file
    writer = pd.ExcelWriter('a.xlsx')
    # write in ro file, 'sheet1' is the page title, float_format is the accuracy of data
    a_pd.to_excel(writer, 'sheet1', float_format='%.6f')
    # save file
    writer.save()
    # close writer
    writer.close()



'''
月定投
'''
def data_show_050002_wucelue_yuedingtou( ):
    df_new = data_chuli()  # 得到处理的原始数据
    T=0
    onerate=0
    fene=0
    data = []
    count = 0
    zongtouru =0
    shouyilv=0
    yingli = 0
    value1=0


    for index, row in df_new.iterrows():

            date = str(index)

            d1 = date [0:10]
            date = d1
            d1 = datetime.datetime.strptime(d1, '%Y-%m-%d')

            if (d1 > dstart and d1 < dend): #// 过滤日期
                # //处理日期
                x = date.split("-", 2)
                # print x

                if(x[2] =="26"): #每月 的定投
                    value = row['value']
                    value= float(value)
                    value1 = value
                    fene= 500/value +fene
                    zongtouru = zongtouru+500
                    shouyilv = (fene * value - zongtouru) / zongtouru  #// 收益率
                    xx = [str(date), value,shouyilv]

                    data.append(xx)
                    count= count+1
    yingli = fene * value1 - zongtouru
    # print  "回测周期 （2019-01-02  ~ 2021-02-10  ）"
    print data
    print  "回测周期" + startdate+"~" + enddate+"----无策略--"+"519068,汇添富成长焦点,"

    print "月定投次数为: "+str(count) +"次"
    print "收益率 = "+str(shouyilv)
    print "盈利=" + str(yingli)
    print "资金量=" + str(zongtouru)



if __name__ == '__main__':

    data_show_050002_celue()
    # data_show_050002_wucelue_yuedingtou()