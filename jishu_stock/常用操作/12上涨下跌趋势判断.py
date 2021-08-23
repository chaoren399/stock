'''

上涨趋势 判断

先把最近7 天的 数据拿到 最小值MIN7,  然后对比最近 30 天的数据做对比, 只要 min7  是最大的说明 这是一个上涨趋势
'''


'''
得到 之前的 60 天的数据, 只要当天是最大值, 说明是上涨趋势. 可以排除很多了 

'''


def isRiJunxianZuHe_mode(dataframe_df, stock_code):
    len1 = len(dataframe_df)
    # print len1
    count =0;
    for i in range(0, len1 - 2 + 1):
        x= isRiJunXianZuHe_2Days_data(dataframe_df[i:i + 2], stock_code)
        count = count + x

    # 找 最近 10 天的最小值
    min_10_tian = 0
    riqi= dataframe_df.ix[0]['trade_date']
    for index ,row in dataframe_df.iterrows():
        if(index == 1):
           min_10_tian = row['low']
        if( min_10_tian > row['low']):  # 近 10 天的最小值
            min_10_tian = row['low']
        if(row['ma34'] > row['ma5'] or row['ma34'] > row['ma13'] ): #  5日 和 13 日 必须大于 34 日慢线
            break;


    isYes = isLow_in_60days(stock_code,riqi,min_10_tian)
    if( count==2 and isYes == 1):
        info ="-----日均线组合5-13-34 成功了" +' ----'+ stock_code +' ----'+ str(riqi)
        print info
        writeLog_to_txt(info)


def isLow_in_60days(stock_code,date,min_10_tian):
    import datetime
    day1riqi = str(date)
    # day1riqi = '20210813'
    # print date
    cur_day = datetime.datetime(int(day1riqi[0:4]), int(day1riqi[4:6]), int(day1riqi[6:8]))
    result_date = cur_day + datetime.timedelta(days=-60)
    try:
        result_date = result_date.strftime('%Y%m%d')
    except Exception as e:
        print e

    pro = ts.pro_api()
    df = pro.daily(ts_code=stock_code, start_date=result_date, end_date=date)
    # print df
    # 计算最小值
    min = 0;
    date1 = date
    for index, row in df.iterrows():
        # 获取 每天的最低值
        if (index == 0):
            min = row['low']
            # print '------sss'+ str(row['low'])
        amin = row['low']
        if (amin < min):
            min = amin
            date1 = row['trade_date']
    if( min <= min_10_tian):
        return 1;
    return 0