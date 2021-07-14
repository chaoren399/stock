#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime

from stock.settings import BASE_DIR
import pandas as pd
import openpyxl

'''
嘉实泰和混合(000595) 失误的一次啊

'''

fundname = "嘉实泰和混合"
fundcode = '000595'

startdate = '2019-07-07'
# startdate = '2021-02-08'
enddate = '2021-07-07'

minshoulv = 0 # 有策略
# minshoulv = -10 # 无策略


# startdate = '2021-05-30'
# enddate = '2021-07-06'
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
    yinglijieduan=0 # 卖出之前的盈利
    maxzijinliang=0 #最大资金量
    isjiama=0 # 是否加码
    jiamacishu=0
    ismaichu=0 #是否卖出
    maichucishu=0

    for index, row in df_new.iterrows():
            ismaichu=0
            isjiama=0
            date = str(index)
            dingtoujine=500

            d1 = date [0:10]
            date = d1
            d1 = datetime.datetime.strptime(d1, '%Y-%m-%d')
            value = row['value']
            value = float(value)

            if (d1 > dstart and d1 < dend): #// 过滤日期
                # //处理日期
                x = date.split("-", 2)
                anyday = datetime.datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%w")

                if (anyday == '2'):  # 选择周2的数据

                    fene= dingtoujine/value +fene
                    zongtouru = zongtouru+dingtoujine

                    # if (shouyilv < -10): #//收益率为负 加码
                    if (shouyilv < minshoulv): #//收益率为负 加码
                        x1= zongtouru-dingtoujine #//计算 之前总投入
                        jiamajine = x1*0.3
                        x2 = dingtoujine + jiamajine  # 加码后的金额要统计一下,方便判断回测的准确率
                        zongtouru = jiamajine+zongtouru
                        isjiama=1
                        # if(zongtouru > maxzijinliang):
                        #     maxzijinliang = zongtouru
                        fene= fene+jiamajine/value
                        jiamacishu= jiamacishu+1

                        dingtoujine = x2

                        print "收益率为负:"

                    yinglijieduan = yinglijieduan + (fene * value - zongtouru)
                    if(yinglijieduan > 5000): #(如果收益大于 5000 全部卖出
                        ismaichu=1;
                        fene=0
                        zongtouru=0.1
                        # shouyilv=0
                        maichucishu=maichucishu+1
                        print "收益率为大于 10% "
                        yinglijieduan=0


                    if(zongtouru > maxzijinliang):
                        maxzijinliang = zongtouru
                    xx = [str(date), value, shouyilv, zongtouru, ismaichu,isjiama,dingtoujine]
                    yingli = (fene * value - zongtouru) +yinglijieduan
                    shouyilv =float((fene * value) - zongtouru)/zongtouru  #// 收益率
                    #
                    data.append(xx)
                    count= count+1

            # if(date == '2021-03-03'):
            #     print "2021-03-03 "
            #     fene = fene + 1000/value
            #     zongtouru = zongtouru + 1000
            #     xx = [str(date), value, shouyilv, zongtouru, ismaichu, isjiama,'1000']
            #     data.append(xx)
            # if(date == '2021-03-14'):
            #     print "2021-03-14 "
            #     value = 3.885
            #     fene = fene + 1000/value
            #     zongtouru = zongtouru + 1000
            #     xx = [str(date), value, shouyilv, zongtouru, ismaichu, isjiama,'1000']
            #     data.append(xx)


    # print data
    if (minshoulv == 0):
        print "有策略"
    else:
        print "无策略"

    print "定投次数为: "+str(count) +"次" + "----"+ "加码次数为: "+str(jiamacishu) +"次" +"----"+  "卖出次数为: "+str(maichucishu) +"次"
    print "收益率 = "+str(shouyilv)
    # print "总投入="+str(zongtouru)
    print "盈利="+str(yingli)
    print "总投入=" + str(zongtouru)
    print "份额=" + str(fene)  +"净值=" + str(value) +"日期="+str(date)
    print "最大资金量=" + str(maxzijinliang)
    print "基金代码:"+fundcode +'--'+ fundname
    print  "回测周期: " + startdate + "~" + enddate

    # python  数组转表格
    a_pd = pd.DataFrame(data)
    # create writer to write an excel file
    # a_pd.to_csv('a.csv')
    writer = pd.ExcelWriter('a.xlsx')
    # write in ro file, 'sheet1' is the page title, float_format is the accuracy of data
    # a_pd.to_excel(writer, 'sheet1', float_format='%.6f',header=0,sheet_name=)
    header=['日期','净值','收益率','累计投入','是否卖出','是否加码',"购买金额"]
    a_pd.to_excel(writer, 'sheet1', float_format='%.6f',header=header)
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