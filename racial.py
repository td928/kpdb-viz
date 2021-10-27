import dash
from dash import Dash, dcc, html, Input, Output

import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from callback import register_racial_callbacks
#from app import app
#import callback


def create_racial_tab(app):

    df = pd.read_csv('C:/Users/T_Du/Workspace/KPDB/kpdb-viz/kpdb_w_pop.csv')

    with urlopen('https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Neighborhood_Tabulation_Areas_2020/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson') as response:
        nta = json.load(response)

    register_racial_callbacks(app, df, nta)

    tab = html.Div([

        #dbc.Alert("This is a primary alert", color="primary"),
        #html.H1("KPDB with Dash", style={'text-align': 'center'}),
        html.Div(
            [
                dcc.Graph(id='units-bar', figure={}),
                dcc.Dropdown(id="phasing",
                            options=[
                                {"label": "Housing Database 2010 - 2020", "value": 'hdb_2010_2020'},
                                {"label": "Within 5 Years", "value": 'within_5_years'},
                                {"label": "From 5 to 10 Years", "value": 'from_5_to_10_years'},
                                {"label": "After 10 Years", "value": 'after_10_years'}],
                            multi=False,
                            value='within_5_years',
                            style={'width': "40%", 'display': 'inline-block'}
                ),
                dcc.Dropdown(id='census-select',
                    options=[
                        {"label": "Show 2020 Census Results", "value": 2020},
                        {"label": "Show 2010 Census Results", "value": 2010}
                    ],
                    multi=False,
                    value=2020,
                    style={'width': '40%', 'display': 'inline-block'}
                ),
                #html.Div(id='output_container', children=[]),
                html.Br(),

                dcc.Graph(id='choro-map', figure={}, className='six columns'),
                dcc.Graph(id='pie-chart', figure={}, className='five columns'),
                html.Br()

            ]
        ),
        html.Br(),
        html.Div(
            [
                dcc.Graph(id='percent-change-chart', figure={}, className='seven columns'),
                dcc.Graph(id='change-bar', figure={}, className='five columns')
            ]
        )
    ])

    # ------------------------------------------------------------------------------
    # Connect the Plotly graphs with Dash Components
    return tab
