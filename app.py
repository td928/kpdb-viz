import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
#from dash import dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import dash
from dash import Dash, dcc, html, Input, Output
from urllib.request import urlopen
import json

#import dash_bootstrap_components as dbc
#import dash_html_components as html
from racial import create_racial_tab
from socioeconomic import create_socioeconomic_tab

#from callback import register_callbacks

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
#app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
# df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Dash_Introduction/intro_bees.csv")
df = pd.read_csv('kpdb_w_pop.csv')

with urlopen('https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Neighborhood_Tabulation_Areas_2020/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson') as response:
    nta = json.load(response)

#df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
#df.reset_index(inplace=True)
#print(df[:5])
#register_callbacks(app)
######################
# Call the Tabs Functions to create tabs
########################
racial_tab = create_racial_tab(app)

socioeconomic_tab = create_socioeconomic_tab(app)


#################### 
# dcc tabs 
####################

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    html.H1('KPDB Dashboard'),
    #headers,
    dcc.Tabs(id="tab-selection", value='tab-racial', children=[
        dcc.Tab(label='Racial Characteristics', value='tab-racial', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Socioeconomic Characteristics', value='tab-socioeconomic', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tab-content')
])

@app.callback(Output('tab-content', 'children'), [Input('tab-selection', 'value')])
def render_content(tab):
    if tab == 'tab-racial':
        return racial_tab
    elif tab == 'tab-socioeconomic':
        return socioeconomic_tab

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

