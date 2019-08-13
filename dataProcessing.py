#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 01:21:04 2019

@author: ray zhu
"""


import numpy as np
import pandas as pd

# The raw data comes from the Berkeley Earth data page:
# http://berkeleyearth.org/data/ 
#
#{
#    "name": "GlobalLandTemperaturesByCountry.csv",
#    "descr": "it is a data table that records the average temperature of different countries on different date. Temperature records are null for some specific dates.",
#    "number of row": "577463",
#    "number of column": "4",
#    "columns": {
#        "dt": {
#            "descr": "on which date that the data was recorded",
#            "type": "datetime",
#            "not null": true
#        },
#        "AverageTemperature": {
#            "descr": "The average temperature of that date.",
#            "type": "float",
#            "not null": false
#        },
#        "AverageTemperatureUncertainty": {
#            "descr": "Uncertainty of the temperature record.",
#            "type": "float",
#            "not null": false
#        },
#        "Country": {
#            "descr": "on which country that the data was recorded ",
#            "type": "float",
#            "not null": true
#        }
#    }
#}

df = pd.read_csv('GlobalLandTemperaturesByCountry.csv', skiprows=0)

data_column=list(df.columns)
# filter columns
data = df[[data_column[0],data_column[1],data_column[3]]]
# column name
data.columns = ['Date', 'AvgTemperature', 'Country']

# take a look at the data
# for idx in data.index:
#     print(data.loc[idx])
    
NZData = data[data.Country == 'New Zealand']

# apply butterworth low_pass filter to filter on NZData
from scipy.signal import butter, lfilter

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


order = 2
fs = 500.0 # sample rate, Hz
cutoff = 10.0 # desired cutoff frequency of the filter, Hz 

filtered_NZData_AvgTemperature = butter_lowpass_filter(NZData.AvgTemperature, cutoff, fs, order)


# get max min avg temperature of every year
NZ_MAX = pd.DataFrame(columns = ['Year','Temperature']) 
NZ_AVG = pd.DataFrame(columns = ['Year','Temperature'])
NZ_MIN = pd.DataFrame(columns = ['Year','Temperature'])

current_year = 0
MAX_t = 0.0
MIN_t = 0.0
AVG_t = 0.0

for idx in NZData.index:
    if current_year != NZData.loc[idx].Date[0:4]:
        # insert rows to dataframes
        if current_year != 0:
            AVG_t = AVG_t/12
            NZ_MAX = NZ_MAX.append({'Year': current_year, 'Temperature': MAX_t}, ignore_index=True)
            NZ_AVG = NZ_AVG.append({'Year': current_year, 'Temperature': AVG_t}, ignore_index=True)
            NZ_MIN = NZ_MIN.append({'Year': current_year, 'Temperature': MIN_t}, ignore_index=True)
            
        # move to a new year
        current_year = NZData.loc[idx].Date[0:4]
        MAX_t = MIN_t = AVG_t = NZData.loc[idx].AvgTemperature
    else:
        t = NZData.loc[idx].AvgTemperature
        MAX_t = max(MAX_t, t)
        MIN_t = min(MIN_t, t)
        # AVG_t will be devided by 12 months finally
        AVG_t = AVG_t + t








