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
from myscripts import neighbourhood_reshape, generate_config

temp_cfg = '/rscratch/vatj2/cloud/PolyominoDash/InteractivePolyomino/configure.cfg'

filepath = 'http://files.tcm.phy.cam.ac.uk/~vatj2/Polyominoes/data/gpmap/V8/interactive/'

display_names = ['genome', 'srobustness', 'irobustness', 'evolvability',  'robust_evolvability', 'complex_evolvability', 'rare', 'unbound', 'complex_diversity', 'diversity', 'pIDs']

df = pd.read_csv(filepath + 'GenomeMetrics_N2_C7_T25_B40_Cx9_J3.txt', sep=' ')

dfn = pd.read_csv(filepath + 'Neighbourhood_N2_C7_T25_B40_Cx9_J3.txt', sep=' ', names=['genome', 'pIDs'], index_col=False)

ndf = neighbourhood_reshape.neighbourhood_reshape(df, dfn, 2, 9)


layout = html.Div(children=[
    # Control Panel
    html.Div([
        html.H3('Control Parameters :'),
        html.Div([
    	   html.P('Number of genes : ', style={'verticalAlign': 'top', 'display' : 'inline-block'}),
    	   html.Div([dcc.Dropdown(
            id='dropdown-ngenes',
            options=[{'label': str(val), 'value': val} for val in range(2, 5)],
            value=2, multi=False, placeholder='ex : 2')],
            style={'marginTop': -5, 'display' : 'inline-block'})],
        style={'width': '400px'}),
        html.Div([
    	   html.P('Number of colours : ', style={'verticalAlign': 'top', 'display' : 'inline-block'}),
    	   html.Div([dcc.Dropdown(
            id='dropdown-metric-colours',
            options=[{'label': str(val), 'value': val} for val in range(3, 15, 2)],
            value=7, multi=False, placeholder='ex : 7')],
        style={'marginTop': -5, 'display' : 'inline-block'})],
        style={'width': '400px'}),
        html.Div([
    	   html.P('Number of builds : ', style={'display' : 'inline-block'}),
    	   html.Div([dcc.Input(
            id='box-builds', min=10, max=250, value=40,
            type='number', placeholder='ex : 40', style={'width' :  '70px'})],
            style={'marginTop': -5, 'display' : 'inline-block'})],
        style={'width': '400px'}),
        html.Div([
    	   html.P('Misfolding Threshold : ', style={'display' : 'inline-block'}),
    	   html.Div([dcc.Input(
            id='box-threshold', min=0.01, max=1., step=0.01, value=0.25,
            type='number', placeholder='ex : 0.25', style={'width' :  '70px'})],
        style={'marginTop': -5, 'display' : 'inline-block'})],
        style={'width': '400px'}),
        html.Div(
            id='custom-parameters',
            style={'display':'none'}
        ),
        html.Div(
            html.Button('Update Configuration', id='button-update-configuration'),
            style={'horizontalAlign' : 'middle'}),
        html.Div(
            id='config-output',
            style={'display':'none'}
        )],
        style={'verticalAlign' : 'top', 'display' : 'inline-block'}),

        # Genome Input

        html.Div([
            html.H3('Genome List : '),
            html.Div(
                dcc.Input(
                    value='', placeholder='[1,0,0,0,2,0,0,0]', type='text')),
            html.Div(children='Enter a genome...'),
            html.Div(
                html.Button('Submit Genome', id='button-submit-genome'),
            style={'horizontalAlign' : 'middle', 'verticalAlign' : 'bottom'})
            ], style={'verticalAlign' : 'top', 'display' : 'inline-block'}),
        html.Br(),

        # Interactive Metric Table

        html.Div(
            dt.DataTable(
                rows=df.round(4).to_dict('records'),
                # optional - sets the order of columns
                columns=display_names,
                row_selectable=True,
                filterable=True,
                sortable=True,
                selected_row_indices=[0],
                id='datatable-genome-metric'
            ), style={'display' : 'inline-block', 'width' : '1600px'}),

        # Bar Graph for Neighbours

        html.Div(
            dcc.Graph(
                id='graph-neighbourhood-distribution'
            ), style={'display' : 'inline-block'})

], className="container")



# Interactive callback functions

@app.callback(
    Output('custom-parameters', 'children'),
    [Input('dropdown-ngenes', 'value'),
    Input('dropdown-metric-colour', 'value'),
    Input('box-threshold', 'value'),
    Input('box-builds', 'value')])
def update_local_config(ngenes, metric_colours, threshold, builds):
    local_parameters = generate_config.parameters.copy()

    print('old : ', local_parameters)

    local_update = dict()
    local_update['ngenes'] = ngenes
    local_update['metric_colours'] = metric_colours
    local_update['threshold'] = threshold
    local_update['builds'] = builds

    local_parameters.update(local_update)

    print('new : ', local_parameters)

    return local_parameters


@app.callback(
    Output('config-output', 'children'),
    [Input('custom-parameters', 'children'),
    Input('button-update-configuration', 'event')])
def write_config_file(local_parameters):
    generate_config.write_config(temp_cfg, local_parameters)


@app.callback(
    Output('graph-neighbourhood-distribution', 'figure'),
    [Input('datatable-genome-metric', 'rows'),
     Input('datatable-genome-metric', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    print('Blueberry')

    dff = pd.DataFrame(rows)

    fig = plotly.tools.make_subplots(
        rows=max(1, len(selected_row_indices)), cols=2,
        # subplot_titles=titles,
        shared_xaxes=False)

    for index in indices:
        genome = dff.loc[index, 'genome']
        print(genome)
        dat = ndf.loc[slice(None),(genome,'pIDs')].value_counts()
        fig.append_trace({
            'x' : dat,
            'type' : 'histogram',
            'showlegend': True
        })
    return fig
