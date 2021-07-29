# encoding=utf-8
import datetime
import time
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render

from st_pool.get_stock_data_2019 import getstockdata
from st_pool.get_stock_data_2019.getstockdata import getdatafrom_ts
from st_pool.models import StockInfo
from stock.settings import BASE_DIR
import json

'''
1 单个指数 走势图

http://127.0.0.1:8087/oneindex/?index=600848

'''


def one_index_olddata_show(request):
    indexcode = request.GET['index']
    code = indexcode
    print 'code' + code

    index_pool_path = BASE_DIR + '/st_pool/get_index_data/指数池.csv'
    # 获取编码对应的股票名称
    indexname = ""
    dfname = pd.read_csv(index_pool_path, dtype=object)
    for index, row in dfname.iterrows():
        code_1 = dfname.iloc[index, 0]  # 指数代码
        if (code_1 == code):
            indexname = dfname.iloc[index, 1]

            break;

    oldstockdatapath_5year = BASE_DIR + '/st_pool/get_index_data/index_old_data/data/'
    # oldstockdatapath_1year = BASE_DIR + '/st_pool/get_index_data/index_old_data/data/'

    df = pd.read_csv(oldstockdatapath_5year + code + '.csv', dtype=object, header=None)

    # df1 = pd.read_csv(oldstockdatapath_1year + code + '.csv', dtype=object, header=None)
    # df = df.append(df1)
    df.columns = ['date', 'open', 'close', 'lowest', 'highest']

    df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期排序
    print 'df=' + df
    data = []
    for index, row in df_new.iterrows():
        date = row['date']  # '2019-01-16'
        open = row['open']
        close = row['close']
        lowest = row['lowest']
        highest = row['highest']
        xx = [str(date), open, close, lowest, highest]
        data.append(xx)

    indexinfo ={"name":indexname,"code":indexcode}
    # maxmin= {"min":lowprice,"max":upprice}
    return render(request, 'indexui/oneindexui.html', {'data': data,'indexinfo':json.dumps(indexinfo)})
    # return render(request, 'stockui/onestockui_1.html', { 'stockinfo': json.dumps(stockinfo),'data':data})


''''
2所有指数的走势图
'''


def index_old_all_show(request):
    index_pool_path = BASE_DIR + '/st_pool/get_index_data/指数池.csv'

    oldstockdatapath_5year = BASE_DIR + '/st_pool/get_index_data/index_old_data/data/'

    print  'index_pool_path ' + index_pool_path

    dict = {}
    dict_cod_name = {}
    df_1 = pd.read_csv(index_pool_path, dtype=object)
    codes = []
    for index, row in df_1.iterrows():
        name = df_1.iloc[index, 1]
        code = df_1.iloc[index, 0]  # 指数代码

        print 'code----' + code
        dict_cod_name.setdefault(str(code), name)  # code: name 字典
        codes.append(code)

        df = pd.read_csv(oldstockdatapath_5year + code + '.csv', dtype=object, header=None)

        # df= df.append(df1)

        df.columns = ['date', 'open', 'close', 'lowest', 'highest']

        df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期排序

        # print 'df='+df
        data = []

        for index, row in df_new.iterrows():
            date = row['date']

            date = row['date']  # '2019-01-16'
            open = row['open']
            close = row['close']
            lowest = row['lowest']
            highest = row['highest']
            xx = [str(date), open, close, lowest, highest]
            data.append(xx)

        dict.setdefault(code, data)

    print 'dict_cod_name=' + str(dict_cod_name)

    return render(request, 'indexui/old_index_ui_all.html',
                  {'codes': json.dumps(codes), 'dict': json.dumps(dict),'dict_cod_name':json.dumps(dict_cod_name)})



num_progress = 0 # 当前的后台进度值（不喜欢全局变量也可以很轻易地换成别的方法代替）
allcodenum =''
tmp=1

'''
3下载指数的历史数据 
'''


def down_index_data_from_tushare(request):
    global num_progress
    global allcodenum
    global tmp
    stock_pool_path = BASE_DIR + '/st_pool/get_index_data/指数池.csv'
    df_1 = pd.read_csv(stock_pool_path, dtype=object)

    codes = df_1.iloc[:, 0].values
    i = 0;
    # codes = df_1.shape[0]  # 行数

    str1 = ''
    for code in codes:

        getdatafrom_ts(code)  # 600887  下载最近一年的历史数据
        # getdatafrom_ts_5years(code)  # 下载 5 年的历史股票数据
        str1 = str1 + '(' + str(i + 1) + '-' + code + ')'
        # print code
        i = i + 1
        tmp = i;
        info = '完成  ' + str(i) + '只股票下载'
        time.sleep(5)  # //睡觉

        allcodenum = str1
        num_progress = i * 100 / len(codes);  # 更新后台进度值，因为想返回百分数所以乘100
        print  'num_progress=' + str(num_progress)
    # return JsonResponse({'res_1': info, 'res_2': 1}, safe=False)
    return JsonResponse({'res_1': info, 'res_2': 1}, safe=False)


'''
1.控制下载界面 html
'''


def down_index_data_ui(request):
    return render(request, 'indexui/downindexui.html')


'''
2更新进度条进度
'''


def show_downindex_progress(request):
    print  'show_downstock_progress =' + str(num_progress)
    print 'tmp=' + str(tmp)
    return JsonResponse({'num_progress': num_progress, 'allcodenum': allcodenum}, safe=False)
