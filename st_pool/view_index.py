# encoding=utf-8
import datetime
import time
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render

from jishu_stock.DaPan.DaPan_HuanJing import get_DaPan_HuanJing
from jishu_stock.z_tool.PyDateTool import getDayNumberYMD
from st_pool.get_index_data.JiaoYiE.GetDayliyJiaoYiE import  get_HS_index_data
from st_pool.get_index_data.getindexdata import get_index_data_from_ts
from stock.settings import BASE_DIR
import json
import tushare as ts

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

        get_index_data_from_ts(code)  # 600887  下载最近一年的历史数据

        # getdatafrom_ts_5years(code)  # 下载 5 年的历史股票数据
        tmp=BASE_DIR + '/st_pool/get_stock_data_2019/stock_old_data/data/'
        str1 = str1 + '(' + str(i + 1) + '-' + code + ')' +' tmpBASE_DIR='+tmp
        # print code
        i = i + 1
        tmp = i;
        info = '完成  ' + str(i) + '只股票下载'+'BASE_DIR='+tmp
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


'''
沪深 2 市每天的成交量  add 2022年02月06日  by zzy
'''

def get_SH_SZ_index_data_JiaoYiE(request):


    df = get_HS_index_data() # 下载数据
    df = df.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    df = df.reset_index(drop=True)  # 重新建立索引 ,默认为false，索引列（被设置为索引的列）被还原为普通列，并将索引重置为整数索引，否则直接丢弃索引列。

    data = []
    for index, row in df.iterrows():
        date = row['trade_date']  # '20190116'
        # date ='20190909'  # '20190116'
        amount = round(row['amount'] /1000000000,2) # 单位 万亿 保留 2 位有效数字
        xx = [int(date), amount]

        data.append(xx)

    lowprice=1
    fundinfo = {"name": '沪深2市交易额', "code": '0000001.SH'}
    maxmin = {"min": lowprice}

    # 获取大盘信息:
    dapan_huanjing= 'is null zzy'
    try:
        today = getDayNumberYMD()
        dapan_info = get_DaPan_HuanJing(today)
        dapan_huanjing = dapan_info
    except:
        print 'dapan_huanjing is null zzy '

    # dapan_huanjing = {"dapan_huanjing": dapan_info}



    return render(request, 'indexui/HuShen_JiaoYiE_ui.html', {'fundinfo': json.dumps(fundinfo),'data':data,'maxmin':maxmin,'dapan_huanjing':dapan_huanjing})
    # return render(request, 'indexui/HuShen_JiaoYiE_ui.html', {'fundinfo': json.dumps(fundinfo),'data':data,'maxmin':maxmin})



