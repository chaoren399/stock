
#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd




''''
dataframe_df[1:4]
取出数据后索引 是这样的 , 1,23 , 而我想要的是 012 
'''

''''

     ts_code trade_date   open   high  ...  change  pct_chg        vol       amount
1  600887.SH   20210730  32.60  33.58  ...    0.64   1.9542  736197.69  2441038.592
2  600887.SH   20210729  32.58  33.08  ...    0.51   1.5819  574561.14  1876835.755
3  600887.SH   20210728  30.90  32.48  ...    0.78   2.4793  792441.11  2523597.994
'''

'''
data3days = data3days.reset_index(drop=True)  # 重新建立索引 ,
data3days
'''



''''

     ts_code trade_date   open   high  ...  change  pct_chg        vol       amount
0  600887.SH   20210730  32.60  33.58  ...    0.64   1.9542  736197.69  2441038.592
1  600887.SH   20210729  32.58  33.08  ...    0.51   1.5819  574561.14  1876835.755
2  600887.SH   20210728  30.90  32.48  ...    0.78   2.4793  792441.11  2523597.994
'''