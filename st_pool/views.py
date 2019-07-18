#encoding=utf-8
import urllib

from django.shortcuts import render
from models import StockInfo, FundInfo
import  pandas as pd
import os
# Create your views here.
from st_pool.get_fund_data import getfunddata
from st_pool.get_stock_data import getstockdata
import json
import datetime
import requests

'''
股票池 UI
'''
def stock_pool_show(request):
    path3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stock_pool_path = path3+'/st_pool' + '/get_stock_data/股票池.csv'

    stocks  = getstockdata.getdata(stock_pool_path)


    list = []
    for i, row in stocks.iterrows():
        print  'i=', i

        st = StockInfo()
        st.code = row[0]
        st.name = row[1]

        st.lowprice = row[2]

        st.upprice = row[3]
        st.order = row[4]
        st.tar_value=row[5]
        st.now_price=row[6]
        st.jiazhilv = row[7]
        st.date = row[8]


        list.append(st)

        # stocklist.update(stocklist2)
    return render(request, 'st_pool/stock_ui.html', {'stocklist': list})

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
        print fd.zhongdian
        fd.url = "http://fund.eastmoney.com/" + fd.code + ".html"

        fd.jiazhilv= row[7]  #价值率
        fd.pingji = row[8] #星辰评级
        fd.guimo = row[9]  # 基金规模
        fd.chenglirq = row[10]  # 成立日期

        # print fd.order
        fundlist.append(fd)


    return render(request,'st_pool/fund_ui.html',{'fundlist':fundlist})


'''
投资理念 UI
'''
def linian_show(request):
    return render(request, 'st_pool/linian_show.html')


'''
基金净值走势图
'''
def fundold_show(request):

    fundpool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/st_pool' + '/get_fund_data/基金池.csv'

    print fundpool_path
    # dict = {'Name': [["2000-06-05", 116], ["2000-06-06", 129]], 'Age': 7, 'Class': 'First'}

    dict ={}
    dict_cod_name={}
    df_1 = pd.read_csv(fundpool_path, dtype=object)

    # codes = df_1.iloc[:, 1].values
    codes=[]
    for index, row in df_1.iterrows():
        name = df_1.iloc[index, 2]
        code = df_1.iloc[index, 1]  # 基金代码
        dict_cod_name.setdefault(str(code),name) # code: name 字典
        codes.append(code)

        oldfunddatapath=  os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/st_pool' + '/get_fund_data/'+'fund_old_data/data/'
        df = pd.read_csv(oldfunddatapath + code + '.csv', dtype=object)
        df.columns = ['date', 'value']
        df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期排序
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
    print 'dict_cod_name='+str(dict_cod_name)
    # return render(request, 'st_pool/old_fund_ui.html', {'dict': json.dumps(dict)} )
    return render(request, 'st_pool/old_fund_ui.html', {'codes': json.dumps(codes), 'dict': json.dumps(dict),'dict_cod_name':json.dumps(dict_cod_name)} )


'''
下载数据从 自己的服务器上

http://58.87.68.70/downfunddata/data/000172.csv
'''
def downdata_from_carxiuli(request):


    fundpool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/st_pool' + '/get_fund_data/基金池.csv'
    datapath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/st_pool' + '/get_fund_data/fund_old_data/data/'
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

    return render(request, 'st_pool/downdata.html',{'info':info})

def testJS(request):
    return render(request, 'st_pool/testjs.html')



def testspider(request):
    return render(request, 'st_pool/test.html')
