#!/usr/bin/python
# -*- coding: utf8 -*-

import pandas as pd

# 缺失时间索引的填充
df = pd.DataFrame({
    "pdate": ["2019-12-01", "2019-12-02", "2019-12-04", "2019-12-05"],
    "pv": [100, 200, 400, 500],
    "uv": [10, 20, 40, 50],
})
print(df)



# 方法1：使用pandas.reindex方法
# 设置索引
df_date = df.set_index("pdate")
# 将df的索引设置为日期索引
df_date = df_date.set_index(pd.to_datetime(df_date.index))

print(df_date)

# 使用pandas.reindex填充缺失的索引
# 生成完整的日期序列
pdates = pd.date_range(start="2019-12-01", end="2019-12-05")
print(pdates)
'''
DatetimeIndex(['2019-12-01', '2019-12-02', '2019-12-03', '2019-12-04',
               '2019-12-05'],
              dtype='datetime64[ns]', freq='D')
'''

# 填充缺失索引，并填充默认值
# df_date_new = df_date.reindex(pdates, fill_value=0)
df_date_new = df_date.reindex(pdates, axis=0)
# df.fillna(method='ffill')

print(df_date_new)
# 用前一行的值填补空值

new= df_date_new.fillna(method='ffill',axis=0)
print(new)

for index, row in new.iterrows():
    print index
    print row

