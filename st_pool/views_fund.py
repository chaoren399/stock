#encoding=utf-8
import urllib

import logging
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from models import StockInfo, FundInfo
import  pandas as pd
import os
# Create your views here.
from st_pool.get_fund_data import getfunddata
from st_pool.get_fund_data.fund_old_data.get_fund_old_data import get_urls, get_urls_fundata_5yeas

from st_pool.zzyutils import load_user_agent
import json
import datetime
import requests
import time

from stock.settings import BASE_DIR

'''
基金池 UI
'''
def fund_show(request):
    fundpool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) +'/st_pool'+ '/get_fund_data/基金池.csv'

    funds = getfunddata.getdata(fundpool_path)
    # print funds
    fundlist = []
    for i, row in funds.iterrows():

        fd = FundInfo()
        fd.order = row[0]
        fd.code= row[1]
        fd.name = row[2]
        fd.tar_value = row[3]
        fd.net_value = row[4]
        fd.jzrq = row[5]

        if(row[6]):
            fd.zhongdian = row[6]
        elif():
            fd.zhongdian = '0'
        # print fd.zhongdian
        fd.url = "http://fund.eastmoney.com/" + fd.code + ".html"

        fd.jiazhilv= row[7]  #价值率
        fd.pingji = row[8] #星辰评级
        fd.guimo = row[9]  # 基金规模
        fd.chenglirq = row[10]  # 成立日期

        # print fd.order
        fundlist.append(fd)


    return render(request, 'fundui/fund_ui.html', {'fundlist':fundlist})


'''
投资理念 UI
'''
def linian_show(request):
    return render(request, 'fundui/linian_show.html')



'''
下载数据从 自己的服务器上

http://58.87.68.70/downfunddata/data/000172.csv
'''
def downdata_from_carxiuli(request):


    fundpool_path = BASE_DIR+ '/st_pool/get_fund_data/基金池.csv'
    datapath = BASE_DIR+ '/st_pool/get_fund_data/fund_old_data/data/'
    df_1 = pd.read_csv(fundpool_path, dtype=object)

    i = 0;
    str1 = ''
    for index, row in df_1.iterrows():
        name = df_1.iloc[index, 2]
        fundcode = df_1.iloc[index, 1]  # 基金代码

        url = 'http://58.87.68.70/downfunddata/data/'+fundcode+'.csv'
        f = requests.get(url)
        print "down"+ fundcode
        with open(datapath+fundcode+".csv", "w") as code:
            code.write(f.content)
        str1= str1+'('+str(i+1)+ '-'+ fundcode+')'
        i= i+1

    info = '完成  '+str(i)+'只基金下载'+str1

    return render(request, 'fundui/downdata.html', {'info':info})

'''
下载控制程序
从第三方服务器上下载数据
http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?fundcode=519688&startdate=2019-02-21&enddate=2019-07-21

动态显示日志
https://www.jianshu.com/p/bc40ac5bbea9
'''
num_progress = 0 # 当前的后台进度值（不喜欢全局变量也可以很轻易地换成别的方法代替）
allcodenum =''
def downdata_from_hexun(request):
    global num_progress
    global  allcodenum
    load_user_agent()

    fundpool_path = BASE_DIR + '/st_pool/get_fund_data/基金池.csv'
    df_1 = pd.read_csv(fundpool_path, dtype=object)
    codes = df_1.iloc[:,1].values
    info = []
    # codes = ['000172']
    # codes = ['000172','000577','110031']
    i = 0;
    str1 = ''
    for code in codes:
        time.sleep(10)  #//睡觉
        x = get_urls(code)
        # x = get_urls_fundata_5yeas(code) #获取 5 年基金数据

        str1 = str1 + '(' + str(i + 1) + '-' + code + ')'
        print 'come x '
        if (x == 'read the log'):
            str1= str1+ 'read the log  has error'
            # print 'x-reason' + x
        i = i + 1
        allcodenum=str1
        info = '完成  '+str(i)+'只基金下载'+str1
        # logging.error('all funds data = '+str(len(codes)))
        num_progress = i * 100 / len(codes);  # 更新后台进度值，因为想返回百分数所以乘100
    print  'num_progress='+str(num_progress)
    return JsonResponse({'res_1':info,'res_2':1}, safe=False)


'''
控制下载界面 html
'''
def downdata_from_hexun_ui(request):

    return render(request, 'fundui/datahexun.html')



'''
更新进度条进度
'''
def show_progress(request):
    print  'show_progress -num_progress=' + str(num_progress)
    return JsonResponse({'num_progress':num_progress,'allcodenum':allcodenum}, safe=False)

'''
展示日志界面
'''
def show_logs(request):
    logpath = BASE_DIR+'/stock/log/fund.log'

    with open(logpath) as file_object:
        contents = file_object.read()
        logs = contents.split('--done')

    # logs=[]
    # logs.append('2323')
    # logs.append('23233')
    count = len(logs)
    return render(request, 'fundui/showlogs.html', {'logs':logs,'count':count})

def clear_logs(request):
    logpath = BASE_DIR + '/stock/log/fund.log'
    f = open(logpath, 'w')
    f.write(' ')
    f.close()
    return JsonResponse({'res':1,}, safe=False)

'''
单个基金走势图

http://127.0.0.1:8081/one_fund_ui/?fund=000172

'''
def one_fundolddata_show(request):
    fundcode = request.GET['fund'].zfill(6)


    code = fundcode
    print 'code'+code
    fundpool_path = BASE_DIR + '/st_pool' + '/get_fund_data/基金池.csv'
    df_1 = pd.read_csv(fundpool_path, dtype=object)
    codes = []
    # 获取编码对应的基金名称
    fundname = ""
    for index, row in df_1.iterrows():


        code1 = df_1.iloc[index, 1]  # 基金代码
        if(code1==fundcode ):
            fundname = df_1.iloc[index, 2]
            lowprice = df_1.iloc[index, 3]
            break;


    # data201801-201908
    oldfunddatapath = BASE_DIR + '/st_pool' + '/get_fund_data/' + 'fund_old_data/data/'
    oldfunddatapath_5years = BASE_DIR + '/st_pool' + '/get_fund_data/' + 'fund_old_data/data2016-2019/'

    df = pd.read_csv(oldfunddatapath + code + '.csv', dtype=object,header=None)
    df1 = pd.read_csv(oldfunddatapath_5years + code + '.csv', dtype=object,header=None)
    df = df.append(df1)
    df.columns = ['date', 'value']

    df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期排序
    # print 'df=' + df
    data = []
    for index, row in df_new.iterrows():
            date = row['date']  #'2019-01-16'
            # //处理日期
            x = date.split("-", 2)
            anyday = datetime.datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%w")

            if (anyday == '5'):  # 选择周五的数据
                value = row['value']
                xx = [str(date), value]
                data.append(xx)
            today = datetime.date.today()
            y = str(today).split("-", 2)
            # 显示 最后一个周五 到目前 之间的几天数据
            if ((datetime.datetime(int(y[0]), int(y[1]), int(y[2])) - datetime.datetime(int(x[0]), int(x[1]),
                                                                                        int(x[2]))).days < 5):
                value = row['value']
                xx = [str(date), value]
                data.append(xx)
    # print 'data='+ data
    code =['fund',str(fundcode)] # 不知道什么原因, 000172 被转成 233 之类的数字
    fundinfo = {"name": fundname, "code": fundcode}
    maxmin = {"min": lowprice}
    return render(request, 'fundui/one_fund_ui.html', {'fundinfo': json.dumps(fundinfo),'data':data,'maxmin':maxmin})


'''
基金净值走势图 所有
'''
def fundold_show(request):

    fundpool_path = BASE_DIR + '/st_pool' + '/get_fund_data/基金池.csv'

    print  'fundpool_paht '+ fundpool_path
    # print fundpool_path
    # dict = {'Name': [["2000-06-05", 116], ["2000-06-06", 129]], 'Age': 7, 'Class': 'First'}

    dict ={}
    dict_cod_name={}
    dict_max_min={} # 目标线
    df_1 = pd.read_csv(fundpool_path, dtype=object)
    codes=[]
    for index, row in df_1.iterrows():
        name = df_1.iloc[index, 2]
        code = df_1.iloc[index, 1]  # 基金代码

        lowprice = df_1.iloc[index, 3]

        max_min = [lowprice]

        print 'code----'+code
        dict_cod_name.setdefault(str(code),name) # code: name 字典
        codes.append(code)

        oldfunddatapath= BASE_DIR+ '/st_pool' + '/get_fund_data/'+'fund_old_data/data/'
        oldfunddatapath_5years= BASE_DIR+ '/st_pool' + '/get_fund_data/'+'fund_old_data/data2016-2019/'

        df = pd.read_csv(oldfunddatapath + code + '.csv', dtype=object,header=None)
        df1 = pd.read_csv(oldfunddatapath_5years + code + '.csv', dtype=object,header=None)
        df = df.append(df1)
        df.columns = ['date', 'value']
        df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期排序

        # print 'df='+df
        data = []
        for index,row in df_new.iterrows():
            date = row['date']
            # //处理日期
            x = date.split("-", 2)
            anyday = datetime.datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%w")

            if (anyday == '5'):  #选择周五的数据
                value = row['value']
                xx = [str(date),value]
                data.append(xx)
            today = datetime.date.today()
            y = str(today).split("-", 2)
            # 显示 最后一个周五 到目前 之间的几天数据
            if((datetime.datetime(int(y[0]),int(y[1]),int(y[2])) - datetime.datetime(int(x[0]), int(x[1]), int(x[2]))).days <5):
                value = row['value']
                xx = [str(date), value]
                data.append(xx)
        dict.setdefault(code,data)
        dict_max_min.setdefault(code,max_min)
    # print 'dict_cod_name='+str(dict_cod_name)
    # return render(request, 'st_pool/old_fund_ui.html', {'dict': json.dumps(dict)} )
    return render(request, 'fundui/old_fund_ui_all.html', {'codes': json.dumps(codes), 'dict': json.dumps(dict), 'dict_cod_name':json.dumps(dict_cod_name),'dict_max_min':json.dumps(dict_max_min)})



def testJS(request):
    return render(request, 'fundui/testjs.html')



def testspider(request):
    return render(request, 'fundui/test.html')



