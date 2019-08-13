#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 01:51:27 2019

@author: zhuzirui
"""
# web server
from flask import Flask
import dataProcessing

# data visualisation lib
import dash
import dash_core_components as dcc
import dash_html_components as html


server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/')

# load dataframe from dataProcess.py
NZData = dataProcessing.NZData
NZ_MAX = dataProcessing.NZ_MAX
NZ_AVG = dataProcessing.NZ_AVG
NZ_MIN = dataProcessing.NZ_MIN
filtered_AvgTemperature = dataProcessing.filtered_NZData_AvgTemperature


# the layout of the webpage
app.layout = html.Div([
    html.Div(
        children=[
             html.H1(children='Dashboard'),
             dcc.Graph(
                id='graph1',
                figure={
                    'data': [
                        {'x': NZData.Date, 'y': NZData.AvgTemperature, 'type': 'line', 'name': 'unfiltered data'},
                        {'x': NZData.Date, 'y': filtered_AvgTemperature, 'type': 'line', 'name': 'filtered data'},
                    ],
                    'layout': {
                        'title': 'Temperature of NZ (by month)',
                        'xaxis': {'title': 'time'},
                        'yaxis': {'title': 'temperature(degree Celsius)'}
                    }
                }
            ),
            dcc.Graph(
                id='graph2',
                figure={
                    'data': [
                        {'x': NZ_MAX.Year, 'y': NZ_MAX.Temperature, 'type': 'line', 'name': 'MAX'},
                        {'x': NZ_MIN.Year, 'y': NZ_MIN.Temperature, 'type': 'line', 'name': 'MIN'},
                        {'x': NZ_AVG.Year, 'y': NZ_AVG.Temperature, 'type': 'line', 'name': 'AVG'},
                    ],
                    'layout': {
                        'title': 'Temperature of NZ (by year)',
                        'xaxis': {'title': 'time'},
                        'yaxis': {'title': 'temperature(degree Celsius)'}
                    }
                }
           ),          
        ]
    )    
])



if __name__ == '__main__':
   server.run(debug=True, port=8080)