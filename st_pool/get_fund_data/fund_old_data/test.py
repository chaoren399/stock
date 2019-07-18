#!/usr/bin/python
# -*- coding: utf8 -*-

# import pandas as pd
# x = pd.DataFrame({"x1":[1,4,2,3],"x2":[4,3,2,1]})
# x.sort_index(by = ["x1","x2"],ascending = [False,True])
# print x

#
import urllib
import requests
import pandas as pd
# x = pd.DataFrame({"x1":[1,2,2,3],"x2":[4,3,2,1]})
# y=x.sort_index(by = ["x1","x2"],ascending = [False,True])
# print  y

# from datetime import datetime
# today = datetime.now().weekday()
# print (today)
#
# week = datetime.strptime("20190711","%Y%m%d").weekday()
# print (week)


# import time
import datetime
# # #今天星期几
# # today=int(time.strftime("%w"))
# # print today
# # #某个日期星期几
#
# str = '2019-07-12'
#
# x = str.split("-", 2)
# print x[2]
# year = int(x[0])
# anyday=datetime.datetime(year,int(x[1]),int(x[2])).strftime("%w")
# # print anyday
# if(anyday == '5'):
#      print anyday


# today = datetime.date.today()
# print today
#
# strftime = datetime.datetime.strptime("2017-11-02", "%Y-%m-%d")
# strftime2 = datetime.datetime.strptime("2017-01-04", "%Y-%m-%d")
# (datetime.datetime(2010,03,01) - datetime.datetime(2010,02,01)).days
#
# print((datetime.datetime(2010,03,01) - datetime.datetime(2010,02,01)).days-5)



def downdata_from_carxiuli():

    # file = open('crm/models.py', 'rb')
    url = 'http://58.87.68.70/downfunddata/data/000172.csv'
    # response = HttpResponse(url)
    # response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    # response['Content-Disposition'] = 'attachment;filename="models.py"'
    # return response
    # return render(request, 'st_pool/downdata.html')

    # url = '//www.jb51.net//test/demo.zip'
    print "downloading with urllib"
    # urllib.urlretrieve(url, "demo.zip")
    # 引用 requests文件

    # 下载地址
    # Download_addres = 'https://nj02cm01.baidupcs.com/file/da941ce26b392a4ea0b010b6e021a695?bkt=p3-1400da941ce26b392a4ea0b010b6e021a6956171262a00000003bca9&fid=3310494135-250528-127659779854873&time=1533574416&sign=FDTAXGERLQBHSK-DCb740ccc5511e5e8fedcff06b081203-KqPVE0es2sUR30U1G%2Fvps9I3VY4%3D&to=88&size=244905&sta_dx=244905&sta_cs=0&sta_ft=jpg&sta_ct=0&sta_mt=0&fm2=MH%2CQingdao%2CAnywhere%2C%2Cchongqing%2Ccmnet&resv0=cdnback&resv1=0&vuk=282335&iv=-2&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=1400da941ce26b392a4ea0b010b6e021a6956171262a00000003bca9&sl=82640974&expires=8h&rt=sh&r=220567738&mlogid=445212826855757932&vbdid=1883780403&fin=1533574308687.jpg&fn=1533574308687.jpg&rtype=1&dp-logid=445212826855757932&dp-callid=0.1.1&hps=1&tsl=50&csl=78&csign=0vnYzTYv2VV%2Ff%2FRkrbacf8q2JPs%3D&so=0&ut=8&uter=4&serv=0&uc=1400105996&ic=321428139&ti=86348c5ac45f19b1da511678c3490bd3448fbb7a71823ad8&by=themis'
    # 把下载地址发送给requests模块
    f = requests.get(url)
    print f
    # 下载文件
    with open("12.ipg", "wb") as code:
        code.write(f.content)


if __name__ == '__main__':
    downdata_from_carxiuli()