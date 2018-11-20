import matplotlib
matplotlib.use('Agg')
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import pandas as pd
import re
import json

from dash.dependencies import Input, Output

os.nice(15)

app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True

# with open("./index.json") as fopen:
#     file_names = json.load(fopen)

# hdf_file = '/rscratch/vatj2/public_html/Polyominoes/data/gpmap/V8/experiment/Processed_GenomeMetrics.h5'

from apps import app_interactive_genomes

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div(dt.DataTable(data=pd.DataFrame().to_dict("rows"), row_selectable="multi",), style={'display': 'none'}),
    html.Div(
    [html.P(dcc.Link('Go to Interactive Genomes', href='/apps/app_interactive_genomes'))],
    style={'align': 'center'})
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app_interactive_genomes':
        return app_interactive_genomes.layout
    else:
        return '404'

app.css.append_css({"external_url": "http://files.tcm.phy.cam.ac.uk/~vatj2/assets/css/main.css"})
