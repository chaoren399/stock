#encoding=utf-8
import os
import tushare as ts




'''
获取股票一年的平均价格
'''


if __name__ == '__main__':

    # pd = ts.get_hist_data('000651',start='2019-01-01',end='2019-12-31')
    pd = ts.get_hist_data('000333',start='2019-01-01',end='2019-12-31')
    # pd = ts.get_hist_data('000651',start='2018-01-01',end='2019-12-31')

    aveTime=pd['close'].mean()
    # pd =  ts.get_hist_data('600848')  # 一次性获取全部日k线数据
    print aveTime
    # print pd['close']