#!/usr/bin/python
# -*- coding: utf8 -*-
import tushare as ts
import sys
import io


def setup_io():
    sys.stdout = sys.__stdout__ = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
    sys.stderr = sys.__stderr__ = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)


setup_io()

#获取股票1分钟数据
df = ts.pro_bar(ts_code='600000.SH',
                    freq='1min',
                    start_date='2020-01-07 09:00:00',
                    end_date='2020-01-08 17:00:00')