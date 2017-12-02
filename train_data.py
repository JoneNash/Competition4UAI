#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: leidelong
@license: Apache Licence 
@contact: leidl8907@gmail.com
@site: https://github.com/JoneNash
@software: PyCharm Community Edition
@time: 2017/12/2 下午4:20
"""
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from datetime import datetime,timedelta


#读取数据集
father_path="/Users/leidelong/competition/uai/UAI_Data/"
hash_poi_info=pd.read_csv(father_path+"poi.csv",encoding="gb2312",sep=';')
# train_Aug=pd.read_csv(father_path+"train_Aug.csv",encoding="gb2312")
# train_July=pd.read_csv(father_path+"train_July.csv",encoding="gb2312")
tmp=pd.read_csv(father_path+"train_Aug.csv",encoding="gb2312")
test_public=pd.read_csv(father_path+"test_id_Aug_agg_public5k.csv")
weather_info=pd.read_csv(father_path+"weather.csv",encoding="utf-8")
weather_info=weather_info.drop(['text','wind_direction'],1)

#空间特征
day_waybill_count=pd.DataFrame({'count' : tmp.groupby('create_date')['id'].size()}).reset_index()
hour_waybill_count=pd.DataFrame({'count' : tmp.groupby('create_hour')['id'].size()}).reset_index()
testid_waybill_count=pd.DataFrame({'count' : tmp.groupby(['create_date','create_hour','start_geo_id','end_geo_id'])['id'].size()}).reset_index()
area2area_waybill_count=pd.DataFrame({'count' : tmp.groupby(['start_geo_id','end_geo_id'])['id'].size()}).reset_index()

waybill_count_extend1=testid_waybill_count.merge(hash_poi_info,how='left',left_on='start_geo_id',right_on='hash_id')
waybill_count_extend1.rename(columns={'filling_station':'start_filling_station',
                  'super_market':'start_super_market',
                  'house':'start_house',
                  'subway_station':'start_subway_station',
                  'bus_station':'start_bus_station',
                  'coffee_shop':'start_coffee_shop',
                  'chinese_restaurant':'start_chinese_restaurant',
                  'atm':'start_atm',
                  'office_house':'start_office_house',
                  'hotel':'start_hotel'
                  }, inplace = True)
print waybill_count_extend1.columns
# waybill_count_extend1.drop('hash_id')

waybill_count_extend2=waybill_count_extend1.merge(hash_poi_info,how='left',left_on='end_geo_id',right_on='hash_id')
waybill_count_extend2.rename(columns={'filling_station':'end_filling_station',
                  'super_market':'end_super_market',
                  'house':'end_house',
                  'subway_station':'end_subway_station',
                  'bus_station':'end_bus_station',
                  'coffee_shop':'end_coffee_shop',
                  'chinese_restaurant':'end_chinese_restaurant',
                  'atm':'end_atm',
                  'office_house':'end_office_house',
                  'hotel':'end_hotel'
                  }, inplace = True)
waybill_count_poiextend=waybill_count_extend2.drop(['hash_id_x','hash_id_y'],1)
print waybill_count_poiextend.columns
print testid_waybill_count.shape
print waybill_count_poiextend.shape

#时间特征

waybill_count_poiextend['month']=[datetime.strptime(d,'%Y-%m-%d').month for d in waybill_count_poiextend['create_date']]
waybill_count_poiextend['day']=[datetime.strptime(d,'%Y-%m-%d').day for d in waybill_count_poiextend['create_date']]
waybill_count_poiextend['hour']=waybill_count_poiextend['create_hour']
waybill_count_poiextend['minute']=[datetime.strptime(d,'%Y-%m-%d').minute for d in waybill_count_poiextend['create_date']]
waybill_count_poiextend['weekday']=[datetime.strptime(d,'%Y-%m-%d').weekday() for d in waybill_count_poiextend['create_date']]



#天气特征
#暂时加上天气特征，后续考虑是否有用

weather_info['month']=[datetime.strptime(d,'%Y-%m-%d %H:%M').month for d in weather_info['date']]
weather_info['day']=[datetime.strptime(d,'%Y-%m-%d %H:%M').day for d in weather_info['date']]
weather_info['hour']=[datetime.strptime(d,'%Y-%m-%d %H:%M').hour for d in weather_info['date']]
weather_info['minute']=[datetime.strptime(d,'%Y-%m-%d %H:%M').minute for d in weather_info['date']]

weather_info['month_before30']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')- timedelta(minutes=30)).month for d in weather_info['date']]
weather_info['day_before30']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')- timedelta(minutes=30)).day for d in weather_info['date']]
weather_info['hour_before30']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')- timedelta(minutes=30)).hour for d in weather_info['date']]
weather_info['minute_before30']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')- timedelta(minutes=30)).minute for d in weather_info['date']]


weather_info['month_before60']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')- timedelta(minutes=60)).month for d in weather_info['date']]
weather_info['day_before60']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')- timedelta(minutes=60)).day for d in weather_info['date']]
weather_info['hour_before60']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')- timedelta(minutes=60)).hour for d in weather_info['date']]
weather_info['minute_before60']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')- timedelta(minutes=60)).minute for d in weather_info['date']]

weather_info['month_30later']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')+ timedelta(minutes=30)).month for d in weather_info['date']]
weather_info['day_30later']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')+ timedelta(minutes=30)).day for d in weather_info['date']]
weather_info['hour_30later']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')+ timedelta(minutes=30)).hour for d in weather_info['date']]
weather_info['minute_30later']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')+ timedelta(minutes=30)).minute for d in weather_info['date']]


weather_info['month_60later']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')+ timedelta(minutes=60)).month for d in weather_info['date']]
weather_info['day_60later']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')+ timedelta(minutes=60)).day for d in weather_info['date']]
weather_info['hour_60later']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')+ timedelta(minutes=60)).hour for d in weather_info['date']]
weather_info['minute_60later']=[(datetime.strptime(d,'%Y-%m-%d %H:%M')+ timedelta(minutes=60)).minute for d in weather_info['date']]

#当前天气
tmp_weather=weather_info[['code','temperature','feels_like','pressure','humidity','visibility','wind_direction_degree','wind_speed','wind_scale','month','day','hour','minute']]
waybill_count_weatherextend=waybill_count_poiextend
waybill_count_weatherextend=waybill_count_weatherextend.merge(tmp_weather,
                                                          how='left',left_on=['month','day','hour','minute'],right_on=['month','day','hour','minute'])
#30分钟后天气
tmp_weather=weather_info[['code','temperature','feels_like','pressure','humidity','visibility','wind_direction_degree','wind_speed','wind_scale','month_before30','day_before30','hour_before30','minute_before30']]
tmp_weather.rename(columns={'code':'code_30before',
                  'temperature':'temperature_30before',
                  'feels_like':'feels_like_30before',
                  'pressure':'pressure_30before',
                  'humidity':'humidity_30before',
                  'visibility':'visibility_30before',
                  'wind_direction_degree':'wind_direction_degree_30before',
                  'wind_speed':'wind_speed_30before',
                  'wind_scale':'wind_scale_30before',
                  }, inplace = True)
waybill_count_weatherextend=waybill_count_weatherextend.merge(tmp_weather,
                                                          how='left',left_on=['month','day','hour','minute'],right_on=['month_before30','day_before30','hour_before30','minute_before30'])
#60分钟后天气
tmp_weather=weather_info[['code','temperature','feels_like','pressure','humidity','visibility','wind_direction_degree','wind_speed','wind_scale','month_before60','day_before60','hour_before60','minute_before60']]
tmp_weather.rename(columns={'code':'code_60before',
                  'temperature':'temperature_60before',
                  'feels_like':'feels_like_60before',
                  'pressure':'pressure_60before',
                  'humidity':'humidity_60before',
                  'visibility':'visibility_60before',
                  'wind_direction_degree':'wind_direction_degree_60before',
                  'wind_speed':'wind_speed_60before',
                  'wind_scale':'wind_scale_60before',
                  }, inplace = True)
waybill_count_weatherextend=waybill_count_weatherextend.merge(tmp_weather,
     how='left',left_on=['month','day','hour','minute'],right_on=['month_before60','day_before60','hour_before60','minute_before60'])


#30分钟后天气
tmp_weather=weather_info[['code','temperature','feels_like','pressure','humidity','visibility','wind_direction_degree','wind_speed','wind_scale','month_30later','day_30later','hour_30later','minute_30later']]
tmp_weather.rename(columns={'code':'code_30later',
                  'temperature':'temperature_30later',
                  'feels_like':'feels_like_30later',
                  'pressure':'pressure_30later',
                  'humidity':'humidity_30later',
                  'visibility':'visibility_30later',
                  'wind_direction_degree':'wind_direction_degree_30later',
                  'wind_speed':'wind_speed_30later',
                  'wind_scale':'wind_scale_30later',
                  }, inplace = True)
waybill_count_weatherextend=waybill_count_weatherextend.merge(tmp_weather,
                                                          how='left',left_on=['month','day','hour','minute'],right_on=['month_30later','day_30later','hour_30later','minute_30later'])
#60分钟后天气
tmp_weather=weather_info[['code','temperature','feels_like','pressure','humidity','visibility','wind_direction_degree','wind_speed','wind_scale','month_60later','day_60later','hour_60later','minute_60later']]
tmp_weather.rename(columns={'code':'code_60later',
                  'temperature':'temperature_60later',
                  'feels_like':'feels_like_60later',
                  'pressure':'pressure_60later',
                  'humidity':'humidity_60later',
                  'visibility':'visibility_60later',
                  'wind_direction_degree':'wind_direction_degree_60later',
                  'wind_speed':'wind_speed_60later',
                  'wind_scale':'wind_scale_60later',
                  }, inplace = True)

waybill_count_weatherextend=waybill_count_weatherextend.merge(tmp_weather,
     how='left',left_on=['month','day','hour','minute'],right_on=['month_60later','day_60later','hour_60later','minute_60later'])

waybill_count_weatherextend=waybill_count_weatherextend.drop(['month','day','hour','minute',
                                  'month_before30','day_before30','hour_before30','minute_before30',
                                  'month_before60','day_before60','hour_before60','minute_before60',
                                  'month_30later','day_30later','hour_30later','minute_30later',
                                  'month_60later','day_60later','hour_60later','minute_60later'],1)
print waybill_count_weatherextend.columns
print waybill_count_weatherextend.shape


waybill_count_weatherextend.to_csv(father_path+"training_data.csv",index=True,index_label='index')
