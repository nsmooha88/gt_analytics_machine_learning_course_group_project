#!/usr/bin/env python

"""weather.py: reads climate related data provided in a file location.
   To use this module, import it into your file and call the get_weather_data function with
   the path to the files required in your local folder
"""
__author__      = "Vincent Amedekah"
__copyright__   = "Copyright 2022, Bee Project"

import pandas as pd
from os import path

absolute_path = path.dirname(__file__)
data_path = 'data'
full_data_path = path.join(absolute_path,data_path)
full_data_weather_path = path.join(full_data_path,'weather')
full_data_processed_path = path.join(full_data_path,'processed')  
full_data_processed_weather_file_path = path.join(full_data_processed_path,'annual_weather.csv')

def process_weather_data():           
        tmax_file = path.join(full_data_weather_path,'climdiv-tmaxst-v10.txt')
        tmin_file = path.join(full_data_weather_path,'climdiv-tminst-v10.txt')
        pcp_file =  path.join(full_data_weather_path,'climdiv-pcpnst-v10.txt')                           
        
        if not (path.exists(tmax_file) & path.exists(tmin_file) & path.exists(pcp_file)):
                raise Exception('The file path specified for weather source files not found')
                
        # define column names
        col_names =['code','jan','feb','mar','apr','may','jun','jul','aug','sept','oct','nov','dec']

        # state code mapping from weather file
        state_code_map = {'001':'Alabama','030':'New York','002':'Arizona','031':'North Carolina','003':'Arkansas','032':'North Dakota',
                '004':'California','033':'Ohio','005':'Colorado','034':'Oklahoma','006':'Connecticut','035':'Oregon','007':'Delaware',
                '036':'Pennsylvania','008':'Florida','037':'Rhode Island','009':'Georgia','038':'South Carolina','010':'Idaho',
                '039':'South Dakota','011':'Illinois','040':'Tennessee','012':'Indiana','041':'Texas','013':'Iowa','042':'Utah',
                '014':'Kansas','043':'Vermont','015':'Kentucky','044':'Virginia','016':'Louisiana','045':'Washington','017':'Maine',
                '046':'West Virginia','018':'Maryland','047':'Wisconsin','019':'Massachusetts','048':'Wyoming','020':'Michigan',
                '050':'Alaska','021':'Minnesota','101':'Northeast Region','022':'Mississippi','102':'East North Central Region',
                '023':'Missouri','103':'Central Region','024':'Montana','104':'Southeast Region','025':'Nebraska','105':'West North Central Region',
                '026':'Nevada','106':'South Region','027':'New Hampshire','107':'Southwest Region','028':'New Jersey','108':'Northwest Region',
                '029':'New Mexico','109':'West Region','110':'National (contiguous 48 States)'} 

        states = ['Alabama','New York','Arizona','North Carolina','Arkansas','North Dakota',
                'California','Ohio','Colorado','Oklahoma','Connecticut','Oregon','Delaware',
                'Pennsylvania','Florida','Rhode Island','Georgia','South Carolina','Idaho',
                'South Dakota','Illinois','Tennessee','Indiana','Texas','Iowa','Utah',
                'Kansas','Vermont','Kentucky','Virginia','Louisiana','Washington','Maine',
                'West Virginia','Maryland','Wisconsin','Massachusetts','Wyoming','Michigan',
                'Alaska','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada',
                'New Hampshire','New Jersey','New Mexico'] 

        # Read files into pandas data frames
        data_types ={i : str for i in range(13)}
        separtor = "\s+|\t+|\s+\t+|\t+\s+"
        tmax = pd.read_csv(tmax_file,sep=separtor, names=col_names, dtype=data_types, engine='python')
        tmin = pd.read_csv(tmin_file,sep=separtor, names=col_names, dtype=data_types, engine='python')
        pcp = pd.read_csv(pcp_file,sep=separtor, names=col_names, dtype=data_types, engine='python')

        # map the state codes in the file to state names as the first 3 digits
        tmax['state'] = tmax['code'].str[:3].map(state_code_map)
        tmin['state'] = tmin['code'].str[:3].map(state_code_map)
        pcp['state'] = pcp['code'].str[:3].map(state_code_map)

        # Drop data for regions and keep only state data
        tmax = tmax[tmax['state'].isin(states)]
        tmin = tmin[tmin['state'].isin(states)]
        pcp = pcp[pcp['state'].isin(states)]

        # convert the str values for the monthly metric into numeric
        months = ['jan','feb','mar','apr','may','jun','jul','aug','sept','oct','nov','dec']
        tmax[months] = tmax[months].apply(pd.to_numeric)  
        tmin[months] = tmin[months].apply(pd.to_numeric)  
        pcp[months] = pcp[months].apply(pd.to_numeric)  

        # Derive the year from the code as the last 4 digit
        tmax['year'] = tmax['code'].str[-4:]
        tmin['year'] = tmin['code'].str[-4:]
        pcp['year'] = pcp['code'].str[-4:]

        # calculate yearly average for the metrics
        tmax['temperature_max'] = tmax[months].max(axis=1)
        tmin['temperature_min'] = tmin[months].min(axis=1)
        pcp['precipitation_total'] = pcp[months].sum(axis=1) 
           
        
        # Get yearly metrics by state consolidated
        annual_weather = tmax.merge(tmin, how='inner',on=['year','state'])[['year','state','temperature_max','temperature_min']]
        annual_weather = annual_weather.merge(pcp, how='inner',on=['year','state'])[['year','state','temperature_max','temperature_min','precipitation_total']]
        annual_weather['year'] = annual_weather['year'].astype('datetime64')
        annual_weather.to_csv(full_data_processed_weather_file_path,index=False)                  
       
if __name__ == "__main__":
        process_weather_data()
       
        