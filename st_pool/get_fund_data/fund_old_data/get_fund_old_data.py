#!/usr/bin/python
# -*- coding: utf8 -*-
from xml.dom import minidom

import datetime

import logging
import pandas as pd
import os,random

import urllib2

from xml.sax import parse, ContentHandler, parseString  #引入继承包ContentHandler
#基金净值的类
import time

from st_pool.zzyutils import user_agents, load_user_agent
from stock.settings import BASE_DIR

class Fund:
    #定义初始化属性，和xml文件属性相同
    def __init__(self,fld_enddate=None,fld_unitnetvalue=None,price=None):
        self.fld_enddate=fld_enddate
        self.fld_unitnetvalue=fld_unitnetvalue
        self.price=price
    def __str__(self):  #转化为字符串输出
        return self.fld_enddate+","+self.fld_unitnetvalue+","
        # return self.fld_unitnetvalue
funds=[]#定义一个基金 的数组,用来存放每次得到的数据
#定义继承ContentHandler的类，可以实现相应的方法
class funddemo(ContentHandler):
    def __init__(self):
        #定义全局变量
        self.fund=None #用来接收funds的相应数据
        self.tag=None  #用来接收characters方法得到的content内容
    def startDocument(self): #funds对象开始
        print("对象开始")
    def endDocument(self):  #funds对象结束
        print("对象结束")
    def startElement(self, name, attrs): #每一个标签元素的开始，name：标签名称 attrs:标签内部相应属性
        if name=='Data':  #如果标签名是Data
            self.fund=Fund()  #创建一个Fund()对象
    def endElement(self, name):  #每一个标签元素的结束，name：标签名称 （此时才会得到相应的content）
        if name=='fld_enddate':
            self.fund.fld_enddate=self.tag  #对象的标签名=得到相应content的值
        if name=='fld_unitnetvalue':
            self.fund.fld_unitnetvalue=self.tag

        if name=='Data':
            funds.append(self.fund)  #为定义的数组追加得到的相应元素

    def characters(self, content):
        self.tag=content   #写了self的，就可以定义为全局变量






'''
url  :需要抓取的网址


http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?fundcode=519688&startdate=2016-11-21&enddate=2018-12-08

'''
def get_urls(fund_code):
        global funds

	length = len(user_agents)
	index=random.randint(0,length-1)
	user_agent = user_agents[index]
	headers={
		'User-Agent':user_agent,
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
	}

        # print user_agent
        fundcode = fund_code
        startdate = '2019-01-01'
        # enddate = '2019-07-10'
        enddate =  str(datetime.date.today())
        # print 'enddate'+ str(enddate)

        url = 'http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?fundcode=' + str(fundcode) + '&startdate=' + startdate + '&enddate=' + enddate
        #  url 连同 headers，一起构造Request请求，这个请求将附带 IE9.0 浏览器的User-Agent
        try:
            request = urllib2.Request(url, headers = headers)

            # 向服务器发送这个请求
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            logging.error('get url error ')
            logging.error(e.reason)
            return  'read the log '
        html = response.read()
        # print html

        f = open(BASE_DIR+'/st_pool/get_fund_data/fund_old_data/data/'+fund_code+'.csv', 'w')
        try:
            parseString(html, funddemo())  # parse的方法，分别指明xml文件，并调用查找的类方法
        except:
            logging.error('parseString error ')
        for fund in funds:  # 对数组funds[]循环
            f.write(fund.fld_enddate+','+fund.fld_unitnetvalue+'\n')
            # print(fund)
        logging.info('--'+str(fundcode) + '--done')
        funds = []#循环到下一个基金的时候要清空全局数组的数据 必须要
        f.close()


'''
获取历史 5 年的基金数据
'''
def get_urls_fundata_5yeas(fund_code):
    global funds

    length = len(user_agents)
    index = random.randint(0, length - 1)
    user_agent = user_agents[index]
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    # print user_agent
    fundcode = fund_code
    startdate = '2016-01-01'
    enddate = '2019-01-01'
    # enddate = str(datetime.date.today())
    # print 'enddate'+ str(enddate)

    url = 'http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?fundcode=' + str(
        fundcode) + '&startdate=' + startdate + '&enddate=' + enddate
    #  url 连同 headers，一起构造Request请求，这个请求将附带 IE9.0 浏览器的User-Agent
    try:
        request = urllib2.Request(url, headers=headers)

        # 向服务器发送这个请求
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        logging.error('get url error ')
        logging.error(e.reason)
        return 'read the log '
    html = response.read()
    # print html

    f = open(BASE_DIR + '/st_pool/get_fund_data/fund_old_data/data2016-2019/' + fund_code + '.csv', 'w')
    try:
        parseString(html, funddemo())  # parse的方法，分别指明xml文件，并调用查找的类方法
    except:
        logging.error('parseString error ')
    for fund in funds:  # 对数组funds[]循环
        f.write(fund.fld_enddate + ',' + fund.fld_unitnetvalue + '\n')
        # print(fund)
    logging.info('--' + str(fundcode) + '--done')
    funds = []  # 循环到下一个基金的时候要清空全局数组的数据 必须要
    f.close()


if __name__ == '__main__':
    load_user_agent()

    fundpool_path = BASE_DIR+ '/st_pool/get_fund_data/基金池.csv'
    print fundpool_path

    df_1 = pd.read_csv(fundpool_path, dtype=object)
    codes = df_1.iloc[:,1].values
    # codes = ['166002','163406']
    codes = ['110031']
    for code in codes:
        print code;
        time.sleep(10)  #//睡觉
        x = get_urls(code)
        if (x=='read the log'):
            print 'x-reason'+x

        # funds=[]  # 循环到下一个基金的时候要清空全局数组的数据