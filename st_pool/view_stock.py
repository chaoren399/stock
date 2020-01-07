#encoding=utf-8
import datetime
import time
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render

from st_pool.get_stock_data_2019 import getstockdata
from st_pool.get_stock_data_2019.getstockdata import getdatafrom_ts, getdatafrom_ts_5years
from st_pool.models import StockInfo
from stock.settings import BASE_DIR
import json


'''
股票池 UI
'''
def stock_show(request):

    stock_pool_path = BASE_DIR+'/st_pool/get_stock_data_2019/股票池.csv'
    stocks  = getstockdata.getdata(stock_pool_path)
    list = []
    for i, row in stocks.iterrows():

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
    return render(request, 'stockui/stock_ui.html', {'stocklist': list})

num_progress = 0 # 当前的后台进度值（不喜欢全局变量也可以很轻易地换成别的方法代替）
allcodenum =''
tmp=1


'''
3下载股票的历史数据 
'''
def down_stock_data_from_tushare(request):
    global num_progress
    global  allcodenum
    global tmp
    stock_pool_path = BASE_DIR + '/st_pool/get_stock_data_2019/股票池.csv'
    df_1 = pd.read_csv(stock_pool_path, dtype=object)
    i=0;
    codes= df_1.shape[0] # 行数

    str1=''
    for index, row in df_1.iterrows():

        code = row[0].zfill(6)
        getdatafrom_ts(code) #600887  下载最近一年的历史数据
        # getdatafrom_ts_5years(code)  # 下载 5 年的历史股票数据
        str1 = str1 + '(' + str(i + 1) + '-' + code + ')'
        # print code
        i=i+1
        tmp = i;
        info = '完成  ' + str(i) + '只股票下载'
        # time.sleep(5)  # //睡觉

        allcodenum = str1
        num_progress = i * 100 / codes;  # 更新后台进度值，因为想返回百分数所以乘100
        print  'num_progress=' + str(num_progress)
    # return JsonResponse({'res_1': info, 'res_2': 1}, safe=False)
    return JsonResponse({'res_1':info , 'res_2': 1}, safe=False)

'''
1.控制下载界面 html
'''
def down_stock_data_ui(request):

    return render(request, 'stockui/downstockui.html')

'''
2更新进度条进度
'''
def show_downstock_progress(request):
    print  'show_downstock_progress =' + str(num_progress)
    print 'tmp='+str(tmp)
    return JsonResponse({'num_progress':num_progress,'allcodenum':allcodenum}, safe=False)






'''
单个股票 走势图

http://127.0.0.1:8087/onestock/?stock=600848

'''
def one_stock_olddata_show(request):
    stockcode = request.GET['stock'].zfill(6)


    code = stockcode
    print 'code'+code
    # data201801-201908
    # oldstockdatapath = BASE_DIR + '/st_pool' + '/get_stock_data_2019/' + 'stock_old_data/data/'
    stock_pool_path = BASE_DIR + '/st_pool/get_stock_data_2019/股票池.csv'
    #获取编码对应的股票名称
    stockname = ""
    dfname = pd.read_csv(stock_pool_path, dtype=object)
    for index, row in dfname.iterrows():
        code_1 = dfname.iloc[index, 0].zfill(6)  # 股票代码
        if(code_1 == code):
            stockname = dfname.iloc[index, 1]

            # stockname=stockname.decode("utf-8").encode("utf-8")
            lowprice=dfname.iloc[index, 2]
            upprice=dfname.iloc[index, 3]
            break;


    oldstockdatapath_5year = BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data_2014_2019/'
    oldstockdatapath_1year = BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data/'

    df = pd.read_csv(oldstockdatapath_5year + code + '.csv', dtype=object,header=None)

    df1 = pd.read_csv(oldstockdatapath_1year + code + '.csv', dtype=object, header=None)
    df = df.append(df1)
    df.columns = ['date', 'value']

    df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期排序
    print 'df=' + df
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

    stockinfo ={"name":stockname,"code":stockcode}
    maxmin= {"min":lowprice,"max":upprice}
    return render(request, 'stockui/onestockui.html', { 'stockinfo': json.dumps(stockinfo),'data':data,'maxmin':maxmin})
    # return render(request, 'stockui/onestockui_1.html', { 'stockinfo': json.dumps(stockinfo),'data':data})

''''
所有股票的走势图
'''
def stock_old_all_show(request):
    stock_pool_path = BASE_DIR + '/st_pool/get_stock_data_2019/股票池.csv'

    oldstockdatapath_5year = BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data_2014_2019/'
    oldstockdatapath_1year = BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data/'

    print  'stock_pool_path '+ stock_pool_path
    # print fundpool_path
    # dict = {'Name': [["2000-06-05", 116], ["2000-06-06", 129]], 'Age': 7, 'Class': 'First'}

    dict ={}
    dict_cod_name={}
    dict_max_min={} # 最大值最小值
    df_1 = pd.read_csv(stock_pool_path, dtype=object)
    codes=[]
    for index, row in df_1.iterrows():
        name = df_1.iloc[index, 1]
        code = df_1.iloc[index, 0].zfill(6)  # 股票代码

        lowprice = df_1.iloc[index, 2]
        upprice = df_1.iloc[index, 3]
        max_min = [lowprice,upprice]
        print 'code----'+code
        dict_cod_name.setdefault(str(code),name) # code: name 字典
        codes.append(code)

        df = pd.read_csv(oldstockdatapath_5year + code + '.csv', dtype=object,header=None)
        df1 = pd.read_csv(oldstockdatapath_1year + code + '.csv', dtype=object,header=None)
        df= df.append(df1)
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
    print 'dict_cod_name='+str(dict_cod_name)
    # return render(request, 'st_pool/old_fund_ui.html', {'dict': json.dumps(dict)} )
    return render(request, 'stockui/old_stock_ui_all.html', {'codes': json.dumps(codes), 'dict': json.dumps(dict), 'dict_cod_name':json.dumps(dict_cod_name),'dict_max_min':json.dumps(dict_max_min)})
