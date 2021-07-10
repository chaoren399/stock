#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from stock.settings import BASE_DIR
import pandas as pd
import openpyxl

'''
519712,交银阿尔法核心混合

'''
def data_show_050002_wucelue( ):
    print("data_show_交银阿尔法核心混合 come in ")
    # 获取编码对应的基金名称
    fundname = "交银阿尔法核心混合"
    fundcode='519712'

    startdate='2019-3-30'
    enddate = '2021-06-28'

    dstart = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    dend = datetime.datetime.strptime(enddate, '%Y-%m-%d')


    oldfunddatapath = BASE_DIR + '/st_pool' + '/get_fund_data/' + 'fund_old_data/'
    df = pd.read_csv(oldfunddatapath+'other/519712/'  + '519712.csv', dtype=object, header=None)
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
    print data
    print  "回测周期" + startdate+"~" + enddate+"----无策略--"+"519068,汇添富成长焦点,"

    print "定投次数为: "+str(count) +"次"
    print "收益率 = "+str(shouyilv)
    print "盈利=" + str(yingli)
    print "资金量=" + str(zongtouru)






def data_show_050002_celue( ):
    print("data_show_519068 come in ")
    # 获取编码对应的基金名称
    fundname = "汇添富成长焦点"
    fundcode='519068'

    startdate='2019-3-30'
    enddate = '2021-06-28'

    dstart = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    dend = datetime.datetime.strptime(enddate, '%Y-%m-%d')



    oldfunddatapath = BASE_DIR + '/st_pool' + '/get_fund_data/' + 'fund_old_data/'
    df = pd.read_csv(oldfunddatapath+'other/519068/'  + '519068.csv', dtype=object, header=None)
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
    jiamacishu=0
    ismaichu=0 #是否卖出
    maichucishu=0

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


                    if (shouyilv < 0): #//收益率为负 加码
                        jiamajine = zongtouru*0.2
                        zongtouru = jiamajine+zongtouru
                        isjiama=1
                        if(zongtouru > maxzijinliang):
                            maxzijinliang = zongtouru
                        fene= fene+jiamajine/value
                        jiamacishu= jiamacishu+1
                        print "收益率为负:"
                    if(shouyilv > 0.2): #(如果收益率大于 10% 全部卖出
                        yingli = yingli+(fene * value - zongtouru)
                        ismaichu=1;
                        fene=0
                        zongtouru=0
                        shouyilv=0
                        maichucishu=maichucishu+1
                        print "收益率为大于 10% "

                    xx = [str(date), value, shouyilv, zongtouru, ismaichu,isjiama]

                    data.append(xx)
                    count= count+1
    print data
    print  "回测周期: " + startdate + "~" + enddate +"----有策略--"+"519068,汇添富成长焦点,"
    print "定投次数为: "+str(count) +"次"
    print "加码次数为: "+str(jiamacishu) +"次"
    print "卖出次数为: "+str(maichucishu) +"次"
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



'''
月定投
'''
def data_show_050002_wucelue_yuedingtou( ):
    print("data_show_519068 come in ")
    # 获取编码对应的基金名称
    fundname = "519712"
    fundcode='519712'

    startdate='2019-4-30'
    enddate = '2021-06-28'

    dstart = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    dend = datetime.datetime.strptime(enddate, '%Y-%m-%d')


    oldfunddatapath = BASE_DIR + '/st_pool' + '/get_fund_data/' + 'fund_old_data/'
    df = pd.read_csv(oldfunddatapath+'other/519712/'  + '519712.csv', dtype=object, header=None)
    df.columns = ['date', 'value']
    df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期 从新到旧 排序

    print "df_new---"
    # print  df_new
    # 设置索引
    df_date = df_new.set_index("date")
    # 将df的索引设置为日期索引
    df_date = df_date.set_index(pd.to_datetime(df_date.index))

    # 生成完整的日期序列
    # df_new = pd.date_range(start="2019-12-01", end="2019-12-05")
    date_range = pd.date_range(start="2016-01-04", end='2021-06-25',normalize=True)

    # 填充缺失索引，
    # df_date_new = df_date.reindex(pdates, fill_value=0)
    df_date_new = df_date.reindex(date_range, axis=0)

    df_date_new= df_date_new.fillna(method='ffill',axis=0)

    # df_new=pd.DataFrame(df_date_new)
    df_new=df_date_new

    # print date_range
    print "df_new"
    # print df_new
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
            # print index
            # print row
            # date = row['date']  #'2019-01-16'
            date = str(index)
            print date[0:10]


            # d1 = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            d1 = date [0:10]
            date = d1
            d1 = datetime.datetime.strptime(d1, '%Y-%m-%d')


            if (d1 > dstart and d1 < dend): #// 过滤日期
                # //处理日期
                x = date.split("-", 2)
                # print x
                anyday = datetime.datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%w")

                if(x[0]=="2019" and x[1]=='05'):
                    print

                if(x[2] =="26"): #每月 的定投100
                    value = row['value']
                    value= float(value)
                    value1 = value
                    fene= 100/value +fene
                    zongtouru = zongtouru+100
                    shouyilv = (fene * value - zongtouru) / zongtouru  #// 收益率
                    xx = [str(date), value,shouyilv]

                    data.append(xx)
                    count= count+1
    yingli = fene * value1 - zongtouru
    # print  "回测周期 （2019-01-02  ~ 2021-02-10  ）"
    print data
    print  "回测周期" + startdate+"~" + enddate+"----月定投 无策略--"+"519712,交银阿尔法核心混合,"

    print "定投次数为: "+str(count) +"次"
    print "累计份额为: "+str(fene)
    print "收益率 = "+str(shouyilv)
    print "盈利=" + str(yingli)
    print "资金量=" + str(zongtouru)
    print"期末资产="+str(fene * value1)

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
    # data_show_050002_celue()
    data_show_050002_wucelue_yuedingtou()