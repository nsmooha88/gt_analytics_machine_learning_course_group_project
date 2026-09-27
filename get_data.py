#!/usr/bin/env python

"""get_data.py: provides functionality to get all final datasets
"""
__author__      = "Vincent Amedekah"
__copyright__   = "Copyright 2022, Bee Project"

import pandas as pd
from os import path

def get_data():
        absolute_path = path.dirname(__file__)
        data_path = 'data'
        full_data_path = path.join(absolute_path,data_path)
        full_data_processed_path = path.join(full_data_path,'processed')
        full_data_processed_test_path = path.join(full_data_processed_path,'Test Data') 

        weather_file = path.join(full_data_processed_path,'annual_weather.csv')
        air_quality_file = path.join(full_data_processed_path,'yearlyAirQuality.csv')
        bee_file_state_colony = path.join(full_data_processed_path,'usda_annual_state_colony_A.csv')
        bee_file_state_colony_test = path.join(full_data_processed_test_path,'usda_annual_state_colony_A.csv')
        bee_file_state_full = path.join(full_data_processed_path,'usda_annual_state_full_B.csv')
        bee_file_state_full_test = path.join(full_data_processed_test_path,'usda_annual_state_full_B.csv')

        weather_data = pd.read_csv(weather_file)
        weather_data['year'] =weather_data['year'].astype('datetime64')
        weather_data['state'] = weather_data['state'].str.lower()

        air_data = pd.read_csv(air_quality_file)
        air_data['year'] = air_data['year'].astype('datetime64')   
        air_data['state'] = air_data['state'].str.lower()
        air_data = air_data.drop('stateabbrv',axis=1)
        
        bee_data = pd.read_csv(bee_file_state_colony)  
        bee_data_test = pd.read_csv(bee_file_state_colony_test) 
        bee_data = pd.concat([bee_data,bee_data_test])  
        bee_data['year'] = bee_data['year'].astype(str) +'-01-01'  
        bee_data['year'] =bee_data['year'].astype('datetime64')
        bee_data['state'] = bee_data['state'].str.lower()              

        bee_full_data = pd.read_csv(bee_file_state_full)
        bee_full_data_test = pd.read_csv(bee_file_state_full_test)
        bee_full_data = pd.concat([bee_full_data,bee_full_data_test])
        bee_full_data['year'] = bee_full_data['year'].astype(str) + '-01-01'
        bee_full_data['year'] = bee_full_data['year'].astype('datetime64')
        bee_full_data['state'] = bee_full_data['state'].str.lower() 
        
        air_weather_combined = air_data.merge(weather_data,on =['year','state'],how='left')
        air_weather_combined['temperature_max'].fillna(air_weather_combined['temperature_max'].mean(),inplace=True)
        air_weather_combined['temperature_min'].fillna(air_weather_combined['temperature_max'].mean(),inplace=True)
        air_weather_combined['precipitation_total'].fillna(air_weather_combined['precipitation_total'].mean(),inplace=True)
        dataset_a = bee_data.merge(air_weather_combined,on = ['year','state'])
        dataset_b = bee_full_data.merge(air_weather_combined, on =['year','state'])     
        dataset_a.sort_values(by=['year','state'], inplace=True)
        dataset_b.sort_values(by=['year','state'], inplace=True)   
        dataset_a_test = dataset_a[dataset_a['year']=='2022-01-01']
        dataset_a = dataset_a[dataset_a['year']!='2022-01-01']
        dataset_b_test = dataset_b[dataset_b['year']=='2022-01-01']
        dataset_b = dataset_b[dataset_b['year']!='2022-01-01']

        return dataset_a, dataset_b,dataset_a_test,dataset_b_test, weather_data, bee_data,bee_full_data, air_data



