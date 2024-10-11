import tushare as ts

pro = ts.pro_api()

df = pro.limit_list_d(trade_date='20220615', limit_type='U', fields='ts_code,trade_date,industry,name,close,pct_chg,open_times,up_stat,limit_times')

print df
