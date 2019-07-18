#encoding=utf-8
import os
import tushare as ts


df = ts.get_report_data(2019,1)

path= '/Users/zzy/PycharmProjects/python-workspace/stock/st_pool/get_stock_data/'

print  df[df['net_profits']>500000]
# df[df['net_profits']>5000].to_csv(path+'filtered.csv')
# print 'ss'