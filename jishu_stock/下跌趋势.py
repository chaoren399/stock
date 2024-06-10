#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR

#!/usr/bin/python
# -*- coding: utf8 -*-
import datetime
import tushare as ts
import pandas as pd
from stock.settings import BASE_DIR

'''
下跌趋势判断 

思路 当前日期的近 7 天的最低点,  判断 半年的 最低点是不是 小于那个值
'''

def getallstockdata_isXiaDie(start_date,end_date):
    path = BASE_DIR + '/jishu_stock/z_stockdata/stockcodelist_No_ST.csv'
    # print "ssss"
    print path
    count = 0
    data = pd.read_csv(path, dtype={'code': str})
    codes=[]



    for index, row in data.iterrows():
        # print row['ts_code']

        if (1):
            ss = anstock_isXiaDieQushi(row['ts_code'],start_date,end_date)
            if(not(ss ==0)):
                codes.append(ss)

        count=count+1
        # if(count =100):

    sss = pd.DataFrame(codes,columns=['ts_code'])
    path1= BASE_DIR+'/jishu_stock/z_stockdata/xiadiecodes.csv'
    sss.to_csv(path1)
        # print "第"+str(count)+"个"
        # print code

'''

'''
def anstock_isXiaDieQushi(stock_code,start_date,end_date):

    ts.set_token('731d2ea0abcf1f14d59ec7215d6ec520e09a439fccd2772c43a906be')
    pro = ts.pro_api()
    # stock_code='600887.SH'
    # print 'stockcode'+stock_code
    # df = pro.daily(ts_code='000002.SZ', start_date='20210701', end_date='2021726')
    try:
        df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
        # df = pro.daily(ts_code=stock_code, start_date='20200701', end_date='20210802')
        # df = pro.daily(ts_code='002942.SZ', start_date='20200701', end_date='2021726')
        if(df.empty):
            return 0
        if(len(df) <200):
            return 0
        # 1 得到 第一个 7 交易日数据
        # iloc只能用数字索引，不能用索引名
        data7_1 = df.iloc[0:22]  # 前7行
        # print data7_1
        # 2 单独一个函数 判断是不是符合 7 星落长空模型
        mini = isAnXiaDie_model_pro(data7_1, stock_code)
        dataBannian_1 = df.iloc[40:220]  # 前7行
        isXiadie = isXiadieQuShi(dataBannian_1,mini)
        # print  isXiadie
        # print 'dd'
        if (isXiadie ):
            # liststocks.append(stock_code)
            print "下跌趋势--------------------------------------:"+stock_code
            return stock_code

    except Exception:
        # print "Exception"
        ss = ""
        # print " "
    return 0



def isAnXiaDie_model_pro(dataframe_df,stockcode):
    min=0
    riqi= ''

    for index, row in dataframe_df.iterrows():
        if (index == 0):  # 最新的一天, 阳线突破实体
            min = row['open']
        day1open = row['open']
        day1riqi = row['trade_date']
        if(day1open < min):
            min = day1open
            riqi=str(day1riqi)

    # print min
    # print riqi
    return min

def isXiadieQuShi(dataframe_df,mini):
    for index, row in dataframe_df.iterrows():
        day1open = row['open']
        if(day1open < mini):
            return 0;
    return 1;






if __name__ == '__main__':
    import datetime

    starttime = datetime.datetime.now()

    # anstock_isAnKanglongyouhui_model("300020.SZ",'20210701', '20210802')
    getallstockdata_isXiaDie('20200701', '20210803')




    endtime = datetime.datetime.now()
    print  "总共运行时长:"
    print (endtime - starttime).seconds

    '''
    追求的 比较符合的 趋势
    '''