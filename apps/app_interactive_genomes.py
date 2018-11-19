import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import numpy as np
import plotly
from dash.dependencies import Input, Output, State
import itertools
import seaborn as sns
import plotly.graph_objs as go


import pandas as pd
import re

from app import app
from scripts/generate_config.py import parameters


layout = html.Div([
    html.H3('Control Parameters :'),
    html.Div(dcc.Dropdown(
        id='dropdown-ngenes',
        options=[{'label': str(val), 'value': val} for val in range(2, 5)],
        value=2, multi=False, placeholder='ex : 2'),
    style={'width': '400px'}),
    html.Div(dcc.Dropdown(
        id='dropdown-metric-colours',
        options=[{'label': str(val), 'value': val} for val in range(3, 15, 2)],
        value=7, multi=False, placeholder='ex : 7'),
    style={'width': '400px'}),
], className="container")
