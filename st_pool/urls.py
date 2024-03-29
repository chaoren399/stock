#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf.urls import include, url

from st_pool import view_index
from . import views_fund
from . import view_stock

urlpatterns = [

    # url(r'^$',views.fund_show),
    url(r'^fund/$', views_fund.fund_show),
    url(r'^linian/$', views_fund.linian_show),#投资理念
    url(r'^fundold/$', views_fund.fundold_show), #所有基金走势图
    url(r'^onefund/$', views_fund.one_fundolddata_show), #单个基金走势图  http://127.0.0.1:8081/onefund/?fund=000172
    url(r'^onefund050002/$', views_fund.data_show_050002), # 博时沪深 300 单个基金走势图  http://127.0.0.1:8087/onefund050002/


    url(r'^download/$', views_fund.downdata_from_carxiuli),

    url(r'^dowanloadhexunui/$', views_fund.downdata_from_hexun_ui), # 下边 3 个是用来控制进度条的 下载第三方基金历史数据
    url(r'^downloadhexun/$', views_fund.downdata_from_hexun),
    url(r'^show_progress/$', views_fund.show_progress),

    url(r'^showlogs/$', views_fund.show_logs), #日志展示
    url(r'^clearlogs/$', views_fund.clear_logs), #日志清除

    url(r'^page(?P<num>\d+)/$', 'blog.views.page'), #  带参数 test

    #2019年12月16日  stockr--------------------


    url(r'^stock/$',view_stock.stock_show),

    url(r'^downstockfromtushare/$', view_stock.down_stock_data_from_tushare),
    url(r'^onestock/$', view_stock.one_stock_olddata_show),  # 单个股票走势图  http://127.0.0.1:8081/onestock/?stock=600887


    url(r'^down_stock_data_ui/$', view_stock.down_stock_data_ui), # 下边 3 个是用来控制进度条的
    url(r'^down_stock_data_from_tushare/$', view_stock.down_stock_data_from_tushare),
    url(r'^show_downstock_progress/$', view_stock.show_downstock_progress),

    url(r'^stock_old_all_show/$', view_stock.stock_old_all_show), #所有股票走势图
    # url(r'^stock_readme/$', views.stock_readme), #一些操作要点

    # 2020年01月26日  index 指数--------------------
    url(r'^oneindex/$', view_index.one_index_olddata_show),  # 单个指数走势图  http://127.0.0.1:8081/oneindex/?index=hs300
    url(r'^index_old_all_show/$', view_index.index_old_all_show),  # 所有指数走势图

    url(r'^down_index_data_ui/$', view_index.down_index_data_ui),  # 下边 3 个是用来控制进度条的
    url(r'^down_index_data_from_tushare/$', view_index.down_index_data_from_tushare),
    url(r'^show_downindex_progress/$', view_index.show_downindex_progress),

    url(r'^hs/$', view_index.get_SH_SZ_index_data_JiaoYiE), # 沪深2 市交易额 2022年02月06日 add



]
