#!/usr/bin/python
# -*- coding: utf8 -*-
import os
import sys
import tushare as ts
from jishu_stock.z_tool.PyDateTool import getMonthNumber, get_date_Befor_Ater_Days

reload(sys)
sys.setdefaultencoding('utf8')

from stock.settings import BASE_DIR
import pandas as pd


# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

def testHuangXian():

    #1 获取文件名字

    path_dir = BASE_DIR + '/jishu_stock/bRuoFeng/data/' + 'zhangtingkaiban' + '/'
    files=[]
    for filename in os.listdir(path_dir):
        files.append(filename)
    files.sort() # 对目录里的文件名 排序

    # print files[-1]
    filename_day = files[0]  #取出最后一个文件的名字
    filename_day = files[1]  #取出最后一个文件的名字
    # print filename_day

    #
    for filename_day in files:

        print filename_day
        #2 读取 数据

        path = path_dir+ filename_day   # 每天导出的数据目录 '/jishu_stock/bRuoFeng/data/2022年6月3日.csv'
        data = pd.read_csv(path,sep=',',encoding='GBK',header=0)
        # print data

        # 3 取出重要的列数据
        # data = data.iloc[0:10]  # 前6行
        data=data.dropna(axis=0, how='any') #删除表中含有任何NaN的行
        data=data.iloc[:, [ 1]]  # .iloc为按位置索引提取 , # 涨停原因为 4

        for index,row in data.iterrows():
            # print row[0]
            # 获取股票代码
            code = getcode(row[0])
            if(code !=0):
                # 获取 数据
                # print code
                date= filename_day.split('.')[0]
                # print date
                getdata(code, date)

            #只包含 00, 60 的才可以
'''
根据代码 日期 获取数据
'''
def getdata(code,date):
    start_date='20210701'
    date=date_chuli(date)
    end_date=date

    stock_code=code
    # print date

    df = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_date, end_date=end_date)
    data1 = df.iloc[0:2]  # 前6行
    # print data1

    # 判断 第 2 天的开盘价 高于 第 1 天的收盘价

    day1_open =''
    day1_close =''
    day2_open = ''
    day2_pct_chg=''
    for index, row in data1.iterrows():
        if(index==0): #第 2 天开盘价
            day2_open=row['open']
            day2_pct_chg=row['pct_chg']
        if(index==1): #第一天 收盘价
            day1_close = row['close']

    if(day2_open > day1_close):
        baifenlv= round((day2_open-day1_close)/day1_close  * 100,2)
        # print baifenlv
        # print str(date)+'-'+str(code) +'--'+ str(day2_pct_chg)
        info = ''
        info = str(date)+'-'+str(code) +'--'+'高开:'+str(baifenlv) +'--第2天涨幅:'+str(day2_pct_chg)
        print info
'''
输入日期 格式: 2022年06月05日

处理日期 , 如果是周五,就要 +3, 其他的+1
'''
def date_chuli(date):
    import re
    s = date.decode('utf-8')  # 举个栗子是字符串s，为了匹配下文的unicode形式，所以需要解码
    p = re.compile(ur'[\u4e00-\u9fa5]')  # 这里是精髓，[\u4e00-\u9fa5]是匹配所有中文的正则，因为是unicode形式，所以也要转为ur

    year=int( p.split(s)[0])  # 使用re库的split切割
    yue = int(p.split(s)[1] ) # 使用re库的split切割
    day =int (p.split(s)[2] ) # 使用re库的split切割
    from datetime import datetime
    # christmas = datetime(2013, 2, 25)
    christmas = datetime(year, yue, day)
    date_YMD= christmas.strftime('%Y%m%d')


    import datetime
    # zhouji = datetime.date(year,yue, day).isoweekday()
    zhouji = datetime.date(year,yue, day).isoweekday()

    date_out=''
    if(zhouji ==5):

        date_out = get_date_Befor_Ater_Days(date_YMD, 3)
        # print date_out
    else:
        date_out = get_date_Befor_Ater_Days(date_YMD, 1)

    # print date_out
    return date_out

    # datetime.date(2022, 2, 22).weekday()


'''
="600633"  -> 600633.SH
'''
def getcode(code):

    code = code[2:-1]
    # print code
    code_2=code[:2]
    # print code_2
    if(code_2=='60'):
        return code+'.SH'
    elif(code_2=='00'):
        return code+'.SZ'

    return 0



if __name__ == '__main__':
    testHuangXian()


