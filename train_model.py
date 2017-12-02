#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: leidelong
@license: Apache Licence 
@contact: leidl8907@gmail.com
@site: https://github.com/JoneNash
@software: PyCharm Community Edition
@time: 2017/12/2 下午6:54
"""


import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from datetime import datetime,timedelta
from lightgbm import LGBMRegressor


#读取数据集
father_path="/Users/leidelong/competition/uai/UAI_Data/"
train_data=pd.read_csv(father_path+"training_data.csv")

target='count'
IDcol = 'index'
startID='start_geo_id'
endID='end_geo_id'
date='create_date'
hour='create_hour'
predictors = [x for x in train_data.columns if x not in [target, IDcol,startID,endID,date,hour]]

# LightGBM params
lgb_params = {}
lgb_params['learning_rate'] = 0.02
lgb_params['n_estimators'] = 10
lgb_params['max_bin'] = 10
lgb_params['subsample'] = 0.8
lgb_params['subsample_freq'] = 10
lgb_params['colsample_bytree'] = 0.8
lgb_params['min_child_samples'] = 500
lgb_params['random_state'] = 99
lgb_params['n_jobs'] = -1

lgb_model = LGBMRegressor(**lgb_params)

