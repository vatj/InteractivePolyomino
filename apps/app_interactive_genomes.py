import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import json
import numpy as np
import plotly
from dash.dependencies import Input, Output, State
import itertools
import seaborn as sns
import plotly.graph_objs as go
from copy import deepcopy
import subprocess


import pandas as pd
import re

from app import app
from myscripts import neighbourhood_reshape, generate_config

temp_cfg = '/rscratch/vatj2/cloud/PolyominoDash/InteractivePolyomino/configuration.cfg'
# temp_genomes = '/rscratch/vatj2/public_html/Polyominoes/data/gpmap/V8/test/SampledGenotypes_N2_C7_T25_B40.txt'

# filepath = 'http://files.tcm.phy.cam.ac.uk/~vatj2/Polyominoes/data/gpmap/V8/test/'
filepath = '/rscratch/vatj2/public_html/Polyominoes/data/gpmap/V8/test/'

display_names = ['genome', 'srobustness', 'irobustness', 'evolvability',  'robust_evolvability', 'complex_evolvability', 'rare', 'unbound', 'complex_diversity', 'diversity', 'pIDs']

df = pd.read_csv(filepath + 'GenomeMetrics_N2_C7_T25_B40_Cx9_J3.txt', sep=' ')

dfn = pd.read_csv(filepath + 'Neighbourhood_N2_C7_T25_B40_Cx9_J3.txt', sep=' ', names=['genome', 'pIDs'], index_col=False)

ndf = neighbourhood_reshape.neighbourhood_reshape(df, dfn, 2, 9)

layout = html.Div([
     ##Control Panel
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
        value=9, multi=False, placeholder='ex : 9')],
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
        id='box-threshold', min=1, max=100, step=1, value=25,
        type='number', placeholder='ex : 0.25', style={'width' :  '70px'})],
    style={'marginTop': -5, 'display' : 'inline-block'})],
    style={'width': '400px'}),

    html.Div(
        html.Button('Update Configuration', id='button-update-configuration'),
        style={'horizontalAlign' : 'middle'}),
    html.Div(
        id='custom-parameters',
        style={'display':'none'})],
    style={'verticalAlign' : 'top', 'display' : 'inline-block'}),

    # Genome Input

    html.Div([
        html.H3('Genome List : '),
        html.Div(
            dcc.Input(
                id='genome-list-input', type='text',
                value='', placeholder='(1,0,0,0,2,0,0,0)'),
            style={'width':'200px'}),
        html.Div(
            children='Enter a genome...',
            id='genome-list-text'),
        html.Div(
            children=json.dumps([]),
            id='genome-list-python',
            style={'display':'none'}),
        html.Div(
            html.Button('Submit Genome', id='button-submit-genome'),
        style={'horizontalAlign' : 'middle', 'verticalAlign' : 'bottom'})
        # html.Div(
        #     id='genome-list-file',
        #     style={'display':'none'}),
        # html.Div(
        #     html.Button('Write Genomes', id='button-write-genome'),
        # style={'horizontalAlign' : 'middle', 'verticalAlign' : 'bottom'})
        ], style={'verticalAlign' : 'top', 'display' : 'inline-block', 'width':'400px'}),
    html.Br(),

    # C++ binary run

    html.Div([
        html.Div(
            id='genome-analysis-hidden',
            style={'display':'none'}),
        html.Div(
            html.Button('Run Genome Analysis', id='button-analyse-genome'),
        style={'horizontalAlign' : 'right', 'verticalAlign' : 'middle'}),
        html.Div(
            html.Button('Reload Table', id='button-analyse-genome'),
        style={'horizontalAlign' : 'right', 'verticalAlign' : 'middle'})
        ], style={'verticalAlign' : 'top', 'display' : 'inline-block', 'width':'800px', 'rightMargin' : '300px'}),

    html.Br(),

    # Interactive Data Table

    dt.DataTable(
        id='datatable-genome-metrics',
        columns=[
            {"name": i, "id": i, "deletable": True} for i in df.columns
        ],
        data=df.to_dict("rows"),
        editable=True,
        filtering=True,
        sorting=True,
        sorting_type="multi",
        row_selectable="multi",
        selected_rows=[],
    ),
    html.Div(id='datatable-interactivity-container')
])



# Interactive callback functions


@app.callback(
    Output('custom-parameters', 'children'),
    [Input('button-update-configuration', 'n_clicks')],
    [State('dropdown-ngenes', 'value'),
    State('dropdown-metric-colours', 'value'),
    State('box-threshold', 'value'),
    State('box-builds', 'value')])
def write_config_file(n_clicks, ngenes, metric_colours, threshold, builds):
    local_parameters = deepcopy(generate_config.parameters)

    local_parameters['main']['n_genes'] = ngenes
    local_parameters['main']['metric_colours'] = metric_colours
    local_parameters['main']['threshold'] = threshold
    local_parameters['main']['builds'] = builds

    generate_config.write_config(local_parameters, temp_cfg)

    return json.dumps(local_parameters)

@app.callback(
    Output('genome-list-python', 'children'),
    [Input('button-submit-genome', 'n_clicks')],
    [State('genome-list-input', 'value'),
    State('genome-list-python', 'children')])
def update_genome_list(n_clicks, new_genome, old_genomes):

    genomes = json.loads(old_genomes)
    genomes.append(new_genome)

    return json.dumps(genomes)

@app.callback(
    Output('genome-list-text', 'children'),
    [Input('genome-list-python', 'children')],
    [State('custom-parameters','children')])
def update_displayed_genome_list(old_genomes, parameters_json):

    if parameters_json is None:
        parameters = deepcopy(generate_config.parameters)
    else:
        parameters = json.loads(parameters_json)

    ending = 'N{n_genes}_C{generate_colours}_T{threshold}_B{builds}.txt'.format(**parameters['main'])
    file = '_'.join(['SampledGenotypes', ending])

    if old_genomes is None:
        return 'Enter a genome...'

    genomes = json.loads(old_genomes)

    with open(filepath+file, "w") as f:
        for genome in genomes:
            for label in eval(genome):
                f.write(str(label) + ' ')
            f.write('\n')

    return [html.Div(str(genome)) for genome in genomes]

# @app.callback(
#     Output('genome-list-file', 'children'),
#     [Input('button-write-genome', 'n_clicks')],
#     [State('genome-list-python', 'children')])
# def write_genome_file(n_clicks, old_genomes):
#     genomes = json.loads(old_genomes);
#
#     with open(temp_genomes, "w") as f:
#         for genome in genomes:
#             for label in eval(genome):
#                 f.write(str(label) + ' ')
#             f.write('\n')
#
#     return 'Hidden String...'

@app.callback(
    Output('genome-analysis-hidden', 'children'),
    [Input('button-analyse-genome', 'n_clicks')])
def run_analysis(n_clicks):
    subprocess.run(['/rscratch/vatj2/cloud/PolyominoDash/InteractivePolyomino/bin/Interactive'], shell=True)
    return 'Hidden String...'


@app.callback(
    Output('datatable-genome-metrics', "data"),
    [Input('genome-analysis-hidden', 'children')],
    [State('custom-parameters', 'children')])
def update_graph(string, parameters_json):

    if parameters_json is None:
        parameters = deepcopy(generate_config.parameters)
        dff = df
    else:
        parameters = json.loads(parameters_json)
        ending = 'N{n_genes}_C{generate_colours}_T{threshold}_B{builds}_Cx{metric_colours}_J{n_jiggle}.txt'.format(**parameters['main'])
        file = '_'.join(['GenomeMetrics', ending])
        dff = pd.read_csv(filepath + file, sep=' ')

    # print('here :')
    # print(dff.head())

    return dff.to_dict('records')


@app.callback(
    Output('datatable-interactivity-container', 'children'),
    [Input('datatable-genome-metrics', "derived_virtual_data"),
     Input('datatable-genome-metrics', "derived_virtual_selected_rows"),
     Input('genome-analysis-hidden', 'children')],
     [State('custom-parameters', 'children')])
def update_graph(rows, derived_virtual_selected_rows, string, parameters_json):

    if parameters_json is None:
        parameters = deepcopy(generate_config.parameters)
    else:
        parameters = json.loads(parameters_json)

    ending = 'N{n_genes}_C{generate_colours}_T{threshold}_B{builds}_Cx{metric_colours}_J{n_jiggle}.txt'.format(**parameters['main'])
    metric_file = '_'.join(['GenomeMetrics', ending])
    neighbour_file = '_'.join(['Neighbourhood', ending])


    dff = pd.read_csv(filepath + metric_file, sep=' ')
    dffn = pd.read_csv(filepath + neighbour_file, sep=' ', names=['genome', 'pIDs'], index_col=False)
    ndff = neighbourhood_reshape.neighbourhood_reshape(dff, dffn, parameters['main']['n_genes'], parameters['main']['metric_colours'])

    # if derived_virtual_selected_rows is None:
    #     derived_virtual_selected_rows = []

    return html.Div(
        [
            dcc.Graph(
                id=genome,
                figure={
                    "data": [
                        {
                            "x": ndff.loc[slice(None),(genome,'pIDs')].value_counts().index,
                            "y": ndff.loc[slice(None),(genome,'pIDs')].value_counts().values,
                            "type": "bar"
                        }
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 250,
                        "margin": {"t": 10, "l": 10, "r": 10},
                    },
                },
            )
            for genome in dff['genome']
        ]
    )
