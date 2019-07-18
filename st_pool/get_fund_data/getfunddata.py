#!/usr/bin/python
# -*- coding: utf8 -*-

import pandas as pd
import os
import numpy as np


import urllib2
import json
import requests

def getdata(fundpool_path):
#1. 打开基金池表格
    df_1 = pd.read_csv(fundpool_path,dtype=object)
    # print 'df_1', df_1
    df_1.columns = ['order', 'code','name','tar_value','net_value','jzrq','zhongdian','url','pingji','guimo',
                    'chenglirq']



#2.  将表格数据与 互联网基金净值 合并成 pd 格式.
    # print  df_1
    for index ,row in df_1.iterrows():
        # print row['code']

        'http://fundgz.1234567.com.cn/js/001186.js'

        code = row['code'].zfill(6)

        df_1.iloc[index, 1] = code  # 把 776转成 000776

        jsondata = getNetValue(code)

        jsondata =  jsondata[8:-2]
        jsondata = json.loads(jsondata)
        netValue = jsondata['dwjz']
        jzrq= jsondata['jzrq']
        df_1.iloc[index,4] = netValue
        df_1.iloc[index,5] =jzrq
        df_1.iloc[index, 7]= float(netValue)- float (row['tar_value'])  # 价值率
        df_1.iloc[index, 8] = row['pingji'] #评级
        df_1.iloc[index, 9] = row['guimo'] #规模
        df_1.iloc[index, 10] = row['chenglirq'] #成立日期





    return df_1


'http://fundgz.1234567.com.cn/js/001186.js'

def getNetValue(fundcode):
    try:
        url = 'http://fundgz.1234567.com.cn/js/' + str(fundcode) + '.js'


        request = urllib2.Request(url)
        response = urllib2.urlopen(url = request,timeout=15)
        return response.read().decode('utf-8')

    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print u"获取基金数据失败,错误原因", e.reason
            return None



    # print  array
if __name__ == '__main__':
    fundpool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/get_fund_data/基金池.csv'
    print fundpool_path
    getdata(fundpool_path)