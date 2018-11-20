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

from app import app, scripts
# from scripts/generate_config.py import parameters

########################
##
## REMOVE TO USE THE FUNCTION DEFINED IN SCRIPTS
##
def neighbourhood_reshape(df, dfn, n_genes, colours):
    neighbours = 4 * n_genes * (colours - 1)
    columns = pd.MultiIndex.from_product([df['genome'].tolist(), ['genome', 'pIDs']], names=['original', 'neighbour'])

    new_df = pd.DataFrame(index=pd.Series(range(0, neighbours)), columns=columns)

    for genome, index in zip(df['genome'], range(0, len(df['genome']))):
        new_df.T.loc[(genome, 'genome'), :] = dfn[(index * neighbours):((index + 1) * neighbours)]['genome'].values
        new_df.T.loc[(genome, 'pIDs'), :] = dfn[(index * neighbours):((index + 1) * neighbours)]['genome'].values

    return new_df
##
########################################

filepath = 'http://files.tcm.phy.cam.ac.uk/~vatj2/Polyominoes/data/gpmap/V8/interactive/'

display_names = ['genome', 'srobustness', 'irobustness', 'evolvability',  'robust_evolvability', 'complex_evolvability', 'rare', 'unbound', 'complex_diversity', 'diversity', 'pIDs']

df = pd.read_csv(filepath + 'GenomeMetrics_N2_C7_T25_B40_Cx9_J3.txt', sep=' ')

dfn = pd.read_csv(filepath + 'Neighbourhood_N2_C7_T25_B40_Cx9_J3.txt', sep=' ', names=['genome', 'pIDs'], index_col=False)

ndf = neighbourhood_reshape(df, dfn, 2, 9)

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
            html.Button('Update Configuration', id='button-update-configuration'),
            style={'horizontalAlign' : 'middle'})],
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
                rows=df.round(3).to_dict('records'),
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
    Output('graph-neighbourhood-distribution', 'figure'),
    [Input('datatable-genome-metric', 'rows'),
     Input('datatable-genome-metric', 'selected_row_indices')])
def update_figure(rows, indices):
    dff = pd.DataFrame(rows)

    fig = plotly.tools.make_subplots(
        rows=max(1, len(selected_row_indices)), cols=2,
        # subplot_titles=titles,
        shared_xaxes=False)

    for index in indices:
        genome = dff.loc[index, 'genome']
        print(genome)
        dat = dfn.loc[slice(None),(genome,'pIDs')].value_counts()
        fig.append_trace({
            'x' : dat,
            'type' : 'histogram',
            'showlegend': True
        })
    return fig
