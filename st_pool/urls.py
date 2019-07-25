#!/usr/bin/python
# -*- coding: utf8 -*-
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^stock/$',views.stock_pool_show),
    # url(r'^$',views.fund_show),
    url(r'^fund/$', views.fund_show),
    url(r'^linian/$', views.linian_show),#投资理念
    url(r'^fundold/$', views.fundold_show), #基金走势图
    url(r'^download/$', views.downdata_from_carxiuli),

    url(r'^dowanloadhexunui/$', views.downdata_from_hexun_ui), # 下边 3 个是用来控制进度条的 下载第三方基金历史数据
    url(r'^downloadhexun/$', views.downdata_from_hexun),
    url(r'^show_progress/$', views.show_progress),

    url(r'^showlogs/$', views.show_logs), #日志展示





]
