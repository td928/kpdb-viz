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

    #def register_racial_callbacks(app, df, nta):   
    @app.callback(
        Output(component_id='choro-map', component_property='figure'),
        Input(component_id='phasing', component_property='value')
    )
    def update_choropleth(option_slctd):
        #print(option_slctd)
        #print(type(option_slctd))

        container = "The year chosen by user was: {}".format(option_slctd)

        #dff = df.copy()
        #dff = dff[dff["Year"] == option_slctd]
        #dff = dff[dff["Affected by"] == "Varroa_mites"]

        self_color_scale = [
            [0, "rgb(224,243,248)"],
            [0.01, "rgb(215,235,240)"],
            [0.02, "rgb(200,225,238)"],
            [0.04, "rgb(171,217,233)"],
            [0.1, "rgb(135,173,209)"],
            [0.2, "rgb(120,145,180)"],
            [1.0, "rgb(49,54,149)"]
        ]

        df_ = df.loc[df[option_slctd] != 0]

        fig = px.choropleth_mapbox(df_, geojson=nta, color=df_[option_slctd],
                            locations=df_["GeoID"], featureidkey="properties.NTA2020",
                            center={"lat": 40.7128, "lon": -74.0060},#-74.1052443755828, 40.5731022653906
                            mapbox_style="carto-positron", zoom=9, 
                            hover_data=[option_slctd, 'GeoID', 'Name'],
                            #custom_data=[]
                            color_continuous_scale=self_color_scale
                            )

        fig.update_layout(clickmode='event+select', margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    @app.callback(
        Output(component_id='units-bar', component_property='figure'),
        Input(component_id='choro-map', component_property='selectedData'),
    )
    def update_units_bar(slct_data):

        df_units = df[['Name', 'within_5_years', 'from_5_to_10_years', 'after_10_years', 'hdb_2010_2020']] 

        if slct_data is None:

            temp = df_units.sum(axis=0)

            df_bar = pd.DataFrame(data={'value': temp.array[1:], 'variable': temp.index[1:]}) # create the dataframe for multiple selection 

            fig = px.bar(df_bar, x='variable', y='value', color='variable', text='value', title='Total Units by Phasing Assumption Citywide')

        
        else:

            nta_slct = [x['customdata'][2] for x in slct_data['points']] 

            temp = df_units.loc[df_units.Name.isin(nta_slct)].sum(axis=0)

            df_bar = pd.DataFrame(data={'value': temp.array[1:], 'variable': temp.index[1:]}) # create the dataframe for multiple selection 

            fig = px.bar(df_bar, x='variable', y='value', color='variable', text='value', title='Total Units by Phasing Assumption in NTA ' + ' ,'.join(nta_slct))

        return fig

    @app.callback(
        Output(component_id='pie-chart', component_property='figure'),
        Input(component_id='choro-map', component_property='selectedData'), # for multiple selection
        #Input(component_id='choro-map', component_property='clickData'),
        Input(component_id='census-select', component_property='value')
    )
    def update_pie_chart(slct_data, option_slctd):
        
        if option_slctd == 2020:
            
            df_pop = df[['Name', 'Hsp_20', 'WNH_20', 'BNH_20',  'ANH_20', 'ONH_20', 'NH2pl_20', ]] 
            
            color_map = {'BNH_20':'royal blue',
                                    'Hsp_20':'purple',
                                    'WNH_20':'orange',
                                    'NH2pl_20':'turquoise',
                                    'ANH_20': 'red',
                                    'ONH_20': 'green'}        

        else:

            #df_pop = df[['Name', 'Hsp_20', 'WNH_20', 'BNH_20',  'ANH_20', 'ONH_20', 'NH2pl_20', ]] 
            df_pop = df[['Name', 'Hsp_10', 'WNH_10', 'BNH_10',  'ANH_10', 'ONH_10', 'NH2pl_10', ]] 

            color_map = {'BNH_10':'royal blue',
                                'Hsp_10':'purple',
                                'WNH_10':'orange',
                                'NH2pl_10':'turquoise',
                                'ANH_10': 'red',
                                'ONH_10': 'green'}



        if slct_data is None:

            #df_pop = df[['Name', 'WNH', 'BNH', 'ANH', 'ONH', 'TwoPlNH']]
            
            #print(df_pop.sum(axis=0))

            #print(pd.melt(df_pop, id_vars=['Name']).groupby('variable').sum())

            df_pie = pd.melt(df_pop, id_vars=['Name']).groupby('variable').sum().reset_index()

            fig = px.pie(df_pie, values='value', names='variable', color='variable', title='Racial Composition Citywide',
                    color_discrete_map=color_map)

        else:
            print(f'select data: {slct_data}')

            #nta_slct = slct_data['points'][0]['customdata'][2] # for sinlge click

            #df_melt = pd.melt(df_pop, id_vars=['Name']) # for single click

            #df_pie = df_melt.loc[df_melt.Name == nta_slct] # for single click

            nta_slct = [x['customdata'][2] for x in slct_data['points']] # for multiple selection

            temp = df_pop.loc[df_pop.Name.isin(nta_slct)].sum(axis=0) # this is an array for multiple selection

            df_pie = pd.DataFrame(data={'value': temp.array, 'variable': temp.index}) # create the dataframe for multiple selection 

            #print(f'the data is {df_s.array}')

            #print(f'the data is {df_s.index}')

            #print(df_s)

            #print(df_pie)

            fig = px.pie(df_pie, values='value', names='variable', color='variable', title='Racial Composition for NTA ' + ' ,'.join(nta_slct), #', '.join(nta_slct),
                    color_discrete_map=color_map)

        fig.update_traces(textposition='auto', textinfo='percent+label+value')
        return fig 

    @app.callback(
        Output(component_id='percent-change-chart', component_property='figure'),
        Input(component_id='phasing', component_property='value')
    )
    def update_percent_change_line_chart(option_slctd):

        #cols = [col for col in df.columns if '_Percent' in col] + ['Name']
        #cols = ['Name', 'Hsp1_Percent','WNH_Percent', 'BNH_Percent', 'ANH_Percent', 'ONH_Percent', 'TwoPlNH_Percent']

        cols = ['Name', 'Hsp_PCh',  'WNH_PCh', 'BNH_PCh', 'ANH_PCh', 'ONH_PCh', 'NH2pl_PCh']

        df_percent = df.sort_values(by=option_slctd, ascending=False)[cols] #+ [option_slctd]]
        
        fig = px.line(pd.melt(df_percent, id_vars=['Name']), x='Name', y='value', color='variable',
                color_discrete_map={'BNH_PCh':'royal blue',
                                            'Hsp_PCh':'purple',
                                            'WNH_PCh':'orange',
                                            'NH2pl_PCh':'turquoise',
                                            'ANH_PCh': 'red',
                                            'ONH_PCh': 'green'})

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    @app.callback(
        Output(component_id='change-bar', component_property='figure'),
        #Input(component_id='choro-map', component_property='clickData'),
        Input(component_id='choro-map', component_property='selectedData')
    )
    def update_change_bar_chart(slct_data):

        # only use the change columns 
        df_pop = df[['Name', 'Hsp_Ch',  'WNH_Ch', 'BNH_Ch', 'ANH_Ch', 'ONH_Ch', 'NH2pl_Ch']]
        
        color_map = {'BNH_Ch':'royal blue',
                                'Hsp_Ch':'purple',
                                'WNH_Ch':'orange',
                                'NH2pl_Ch':'turquoise',
                                'ANH_Ch': 'red',
                                'ONH_Ch': 'green'}
        if slct_data is None:

            #df_pop = df[['Name', 'WNH', 'BNH', 'ANH', 'ONH', 'TwoPlNH']]
            
            #print(df_pop.sum(axis=0))

            #print(pd.melt(df_pop, id_vars=['Name']).groupby('variable').sum())

            df_bar = pd.melt(df_pop, id_vars=['Name']).groupby('variable').sum().reset_index()

            #fig = px.pie(df_pie, values='value', names='variable', color='variable', title='Population Change by Racial Group Citywide',
            #        color_discrete_map=color_map)

            fig = px.bar(df_bar, x='variable', y='value', color='variable', text='value',title='Population Change by Racial Group Citywide', color_discrete_map=color_map)

        else:
            #print(f'select data: {slct_data}')

            #nta_slct = slct_data['points'][0]['customdata'][2] # for single click

            #df_melt = pd.melt(df_pop, id_vars=['Name']) # for single click

            #df_bar = df_melt.loc[df_melt.Name == nta_slct] # for single click

            nta_slct = [x['customdata'][2] for x in slct_data['points']]# for multiple selection

            temp = df_pop.loc[df_pop.Name.isin(nta_slct)].sum(axis=0) # this is an array for multiple selection

            df_bar = pd.DataFrame(data={'value': temp.array[1:], 'variable': temp.index[1:]}) # create the dataframe for multiple selection 

            #print(df_pie)

            # the pie chart has trouble representing the negative value in change
            #fig = px.pie(df_pie, values='value', names='variable', color='variable', title='Population Change by Racial Group for NTA ' + nta_slct,
            #        color_discrete_map=color_map)

            fig = px.bar(df_bar, x='variable', y='value', color='variable', text='value', title='Population Change by Racial Group for NTA ' + ' ,'.join(nta_slct), color_discrete_map=color_map)


            #pd.melt(df_nta[[]]
        fig.update_traces(textposition='outside',) #textinfo='label+value')

        return fig

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
