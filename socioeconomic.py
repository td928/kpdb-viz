import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd
from callback import register_socioeconomic_callbacks

def create_socioeconomic_tab(app):

    #df = pd.read_csv('C:/Users/T_Du/Workspace/KPDB/kpdb-viz/socioeconomic.csv')

    df = pd.read_csv('socioeconomic.csv')

    register_socioeconomic_callbacks(app, df)

    tab = html.Div(
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
            dcc.Graph(id='choro-map', figure={}, className='six columns'),
            dcc.Graph(id='edu-pie', figure={}, className='four columns'),
            dcc.Graph(id='income-pie', figure={}, className='four columns'),
        ]
    )

    return tab