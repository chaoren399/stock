#!/usr/bin/python
# -*- coding: utf8 -*-
from stock.settings import BASE_DIR
import pandas as pd

'''
博时沪深 300 指数基金 (050002)

'''
def data_show_050002( ):
    print("data_show_050002 come in ")
    # 获取编码对应的基金名称
    fundname = "博时沪深 300 指数基金"
    fundcode='050002'
    oldfunddatapath = BASE_DIR + '/st_pool' + '/get_fund_data/' + 'fund_old_data/'
    df = pd.read_csv(oldfunddatapath+'other/050002/'  + '050002.csv', dtype=object, header=None)
    df.columns = ['date', 'value']
    df_new = df.sort_values(by='date', axis=0, ascending=True)  # 按照日期 从新到旧 排序
    data = []
    for index, row in df_new.iterrows():
        date = row['date']  # '2019-01-16'
        value = row['value']
        xx = [str(date), value]
        data.append(xx)
    code = ['fund', str(fundcode)]  # 不知道什么原因, 000172 被转成 233 之类的数字
    fundinfo = {"name": fundname, "code": fundcode}
    maxmin = {"min": '1'}
    print df_new

    data = []
    for index, row in df_new.iterrows():
            date = row['date']  #'2019-01-16'
            # //处理日期
            x = date.split("-", 2)
            anyday = datetime.datetime(int(x[0]), int(x[1]), int(x[2])).strftime("%w")

            if (anyday == '5'):  # 选择周五的数据
                value = row['value']
                xx = [str(date), value]
                data.append(xx)
            today = datetime.date.today()
            y = str(today).split("-", 2)
            # 显示 最后一个周五 到目前 之间的几天数据
            if ((datetime.datetime(int(y[0]), int(y[1]), int(y[2])) - datetime.datetime(int(x[0]), int(x[1]),
                                                                                        int(x[2]))).days < 5):
                value = row['value']
                xx = [str(date), value]
                data.append(xx)


if __name__ == '__main__':
    data_show_050002()
