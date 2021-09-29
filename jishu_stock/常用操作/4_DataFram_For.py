#!/usr/bin/python
# -*- coding: utf8 -*-
# for i in range(1, 10)


'''
# 两个数据合并
   df = pd.read_csv(oldfunddatapath + code + '.csv', dtype=object,header=None)
    df1 = pd.read_csv(oldfunddatapath_5years + code + '.csv', dtype=object,header=None)
    df = df.append(df1)
    df.columns = ['date', 'value']

'''
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

取前 3 行
data7_1 = df.iloc[0:3]
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


''''
10

pandas删除含有空值的行

data = data.dropna(how='any', axis=0) 可以用
df.dropna(axis=0, how='any', inplace=True)  不能用

https://blog.csdn.net/Guo_ya_nan/article/details/81042882
axis：
0: 行操作（默认）
1: 列操作
how：
any: 只要有空值就删除（默认）
all:全部为空值才删除
inplace：
False: 返回新的数据集（默认）
True: 在愿数据集上操作

'''

''''
11

1、python中数据框求每列的最大值和最小值

df.min()
df.max()

'''


''''
12  按照列 排序
    data = data.sort_values(by='trade_date', axis=0, ascending=True)  # 按照日期 从旧到新 排序
    data = data.reset_index(drop=True)  # 重新建立索引 ,
    data = data.reset_index()  # 重新建立索引 , 保留日期


     ts_code  trade_date  open  high  ...    ma13     ma_v_13    ma34     ma_v_34
0  000006.SZ    20210826  4.64  4.72  ...  4.6254  64885.3354  4.6179  69862.9471
1  000006.SZ    20210827  4.63  4.65  ...  4.6215  70125.2015  4.6097  70755.0403
2  000006.SZ    20210830  4.55  4.55  ...  4.6069  68943.3223  4.5991  71789.6232

'''