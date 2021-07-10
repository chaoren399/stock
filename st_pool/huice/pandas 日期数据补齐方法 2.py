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


# 方法2：使用pandas.resample方法
# 先将索引变成日期索引，并删除原先得pdate一列
df_new2 = df.set_index(pd.to_datetime(df["pdate"])).drop("pdate", axis=1)
# 使用dataframe的resample的方法按照天重采样
# 由于采样会让区间变成一个值，所以需要指定mean等采样值的设定方法
df_new2 = df_new2.resample("D").mean().fillna(0)
print(df_new2)

'''
              pv    uv
pdate                  
2019-12-01  100.0  10.0
2019-12-02  200.0  20.0
2019-12-03    0.0   0.0
2019-12-04  400.0  40.0
2019-12-05  500.0  50.0
'''


# resample的使用方式（2D每隔两天，pv/uv是两天得平均值）
res12 = df_new2.resample("2D").mean()
print(res12)
