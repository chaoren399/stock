#!/usr/bin/python
# -*- coding: utf8 -*-
# for i in range(1, 10)

''''


    for index, row in data.iterrows():
        name = row['name']
        if('ST' not in name):
           print name
'''


'''

两列相减
data_merge['差值'] = data_merge['数量_x'] - data_merge['数量_y']

'''

''''
取某几列

df = df[['ts_code','trade_date','ma5','ma13']]

'''


'''
循环 3 个迭代

len1 = len(dataframe_df)
    # print len1
    for i in range(0,len1-3+1):
        # print "i" + str(i )+ "j"+str(i+3)
        # print dataframe_df[i:i+3]
        # isKanglongyouhui_3Days_data(dataframe_df[0:3])
        isKanglongyouhui_3Days_data(dataframe_df[i:i+3],stockcode)
'''


''''
取某一行某一列的值
day1open = data3days.ix[2][2]
a1=data.ix[0]['ma5_13_cha']
'''

'''
批量更改 日期格式
   stock_data['trade_date'] =pd.to_datetime(stock_data['trade_date'], format='%Y%m%d', errors='coerce')


'''