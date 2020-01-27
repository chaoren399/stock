#!/usr/bin/python
# -*- coding: utf8 -*-

import os
from stock.settings import BASE_DIR

user_agents = list()


# 加载 user_agents配置文件
def load_user_agent():
    fpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fpath = BASE_DIR + '/st_pool/get_fund_data/user_agents'

    # print 'fpath'+fpath
    fp = open(fpath, 'r')
    line = fp.readline().strip('\n')
    while (line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close()
