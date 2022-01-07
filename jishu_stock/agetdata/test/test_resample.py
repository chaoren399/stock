#!/usr/bin/python
# -*- coding: utf8 -*-

import pandas as pd
import numpy as np

date_rng = pd.date_range('20170101', periods=100, freq='D')
ser_obj = pd.Series(range(len(date_rng)), index=date_rng)

print date_rng
# 统计每个月的数据总和
resample_month_sum = ser_obj.resample('M').sum()
# 统计每个月的数据平均
resample_month_mean = ser_obj.resample('M').mean()

print('按月求和：', resample_month_sum)
print('按月求均值：', resample_month_mean)