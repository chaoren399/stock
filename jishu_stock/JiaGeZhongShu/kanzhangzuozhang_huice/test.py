#!/usr/bin/python
# -*- coding: utf8 -*-
import pandas as pd

import pandas as pd
data_test= pd.DataFrame([
                    ['张三',1,1],
                    ['李四',2,2],
                    ['张三',3,3],
                    ['张三',4,4],
                    ['王五',5,5],
                    ['王五',6,6,],
                    ['赵六',7,7]
                    ],
                    columns =['name','number_1','number_2']
                    )
# print data_test

# data_test.loc['axis_0']=data_test.loc[:,['number_1','number_2','axis_1']].apply(lambda x:x.sum())
# data_test['sum'] = data_test.iloc[:,1:3].sum(axis=0)
# data_test
data_test.loc['Col_sum1'] = data_test.iloc[1:-1,1:3 ].sum(axis=0) # 对0，1行按列求和，生成新行
# data_test['Row_sum'] = data_test.iloc[:,1:3].sum(axis=1)  # 对0，1列按行求和，生成新列

print data_test
