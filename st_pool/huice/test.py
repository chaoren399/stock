#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from stock.settings import BASE_DIR
import pandas as pd
import openpyxl

'''
博时沪深 300 指数基金 (050002)

'''
def data_show_050002_wucelue( ):
    print("data_show_050002 come in ")
    # 获取编码对应的基金名称
    fundname = "博时沪深 300 指数基金"
    fundcode='050002'

    startdate='2019-12-30'
    enddate = '2021-01-01'

    dstart = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    dend = datetime.datetime.strptime(enddate, '%Y-%m-%d')


    oldfunddatapath = BASE_DIR + '/st_pool' + '/get_fund_data/' + 'fund_old_data/'
    df = pd.read_csv(oldfunddatapath+'other/050002/'  + '050002.csv', dtype=object, header=None)
    df.columns = ['date', 'value']
    df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

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
            date = row['date']  #'2019-01-16'

            d1 = datetime.datetime.strptime(date, '%Y-%m-%d')

            if (d1 > dstart and d1 < dend): #// 过滤日期
                # //处理日期
                x = date.split("-", 2)
                anyday = datetime.datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%w")

                if (anyday == '1'):  # 选择周五的数据
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
    print  "回测周期" + startdate+"~" + enddate
    print data
    print "定投次数为: "+str(count) +"次"
    print "收益率 = "+str(shouyilv)
    print "盈利=" + str(yingli)
    print "资金量=" + str(zongtouru)






def data_show_050002_celue( ):
    print("data_show_050002 come in ")
    # 获取编码对应的基金名称
    fundname = "博时沪深 300 指数基金"
    fundcode='050002'


    startdate='2019-12-30'
    enddate = '2021-01-01'

    dstart = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    dend = datetime.datetime.strptime(enddate, '%Y-%m-%d')


    oldfunddatapath = BASE_DIR + '/st_pool' + '/get_fund_data/' + 'fund_old_data/'
    df = pd.read_csv(oldfunddatapath+'other/050002/'  + '050002.csv', dtype=object, header=None)
    df.columns = ['date', 'value']
    df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期 从新到旧 排序


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
    ismaichu=0 #是否卖出

    for index, row in df_new.iterrows():
            ismaichu=0
            isjiama=0
            date = row['date']  #'2019-01-16'

            d1 = datetime.datetime.strptime(date, '%Y-%m-%d')

            if (d1 > dstart and d1 < dend): #// 过滤日期
                # //处理日期
                x = date.split("-", 2)
                anyday = datetime.datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%w")

                if (anyday == '1'):  # 选择周五的数据
                    value = row['value']
                    value= float(value)
                    fene= 500/value +fene
                    zongtouru = zongtouru+500
                    shouyilv = (fene * value - zongtouru) / zongtouru  #// 收益率


                    if (shouyilv < 0): #//收益率为负
                        jiamajine = zongtouru*0.2
                        zongtouru = jiamajine+zongtouru
                        isjiama=1
                        if(zongtouru > maxzijinliang):
                            maxzijinliang = zongtouru
                        fene= fene+jiamajine/value
                        print "收益率为负:"
                    if(shouyilv > 0.1): #(如果收益率大于 10% 全部卖出
                        yingli = yingli+(fene * value - zongtouru)
                        ismaichu=1;
                        fene=0
                        zongtouru=0
                        shouyilv=0
                        print "收益率为大于 10% "

                    xx = [str(date), value, shouyilv, zongtouru, ismaichu,isjiama]

                    data.append(xx)
                    count= count+1

    print  "回测周期" + startdate + "~" + enddate
    print data
    print "定投次数为: "+str(count) +"次"
    print "收益率 = "+str(shouyilv)
    # print "总投入="+str(zongtouru)
    print "盈利="+str(yingli)
    print "最大资金量=" + str(maxzijinliang)
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


if __name__ == '__main__':
    # data_show_050002_wucelue() #无策略
    data_show_050002_celue()