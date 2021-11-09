import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
#from app import app
#from tabs.racial import create_racial_tab
#from tabs.socioeconomic import create_socioeconomic_tab

def register_socioeconomic_callbacks(app, df):

    @app.callback(
        Output(component_id='edu-pie', component_property='figure'),
        Input(component_id='choro-map', component_property='clickData')
    )
    def update_education_pie(slct_data):
        
        df_edu = df[['GeoName', 'EA_LTHSGrE', 'EA_BchDHE']]

        edu_index = {
            'EA_LTHSGrE': 'Less than high school graduate',
            'EA_BchDHE': 'Bachelor degree or higher'
        }

        if slct_data is None:

            df_pie = pd.melt(df_edu, id_vars=['GeoName']).groupby('variable').sum().reset_index()

            # could add the dictionary mapping for the variable names
            df_pie['variable'] = df_pie.variable.map(edu_index)

            fig = px.pie(df_pie, values='value', names='variable', color='variable', title='Education Level for Citywide')

        else:

            nta_slct = slct_data['points'][0]['customdata'][2]

            df_melt = pd.melt(df_edu, id_vars=['GeoName'])

            df_pie = df_melt.loc[df_melt.GeoName == nta_slct] 

            # could add the dictionary mapping for the variable names
            df_pie['variable'] = df_pie.variable.map(edu_index)

            fig = px.pie(df_pie, values='value', names='variable', color='variable', title='Education Level for NTA ' + nta_slct)
        
        return fig 

    @app.callback(
        Output(component_id='income-pie', component_property='figure'),
        Input(component_id='choro-map', component_property='clickData')
    )
    def update_income_pie(slct_data):
        
        df_income = df[['GeoName','HHIU10E' , 'HHI10t14E', 'HHI15t24E', 'HHI25t34E',
       'HHI35t49E', 'HHI50t74E', 'HHI75t99E', 'HI100t149E', 'HI150t199E',
       'HHI200plE',]]

        color_map = {
            'HHIU10E':'royal blue',
            'HHI15t24E':'purple',
            'HHI10t14E':'orange',
            'HHI25t34E':'turquoise',
            'HHI35t49E': 'red',
            'HHI50t74E': 'green',
            'HHI75t99E' : 'yellow',
            'HI100t149E': 'pink',
            'HI150t199E': ''
        }

        income_index = {
            'HHIU10E' : 'Less Than $10,000', 
            'HHI10t14E': '$10,000 to $14,999', 
            'HHI15t24E': '$15,000 to $24,999', 
            'HHI25t34E': '$25,000 to $34,999',
            'HHI35t49E': '$35,000 to $49,999', 
            'HHI50t74E': '$50,000 to $74,999', 
            'HHI75t99E': '$75,000 to $99,999', 
            'HI100t149E': '$100,000 to $149,999', 
            'HI150t199E': '$150,000 to $199,999',
            'HHI200plE': '$200,000 to more'
        }

        if slct_data is None:
            
            df_pie = pd.melt(df_income, id_vars=['GeoName']).groupby('variable').sum().reset_index()

            # could add the dictionary mapping for the variable names e.g. df['variable'] = df.variable.map(income_level_dict)
            df_pie['variable'] = df_pie.variable.map(income_index)

            fig = px.pie(df_pie, values='value', names='variable', color='variable', title='Income Groups Citywide')

        else:
            nta_slct = slct_data['points'][0]['customdata'][2]

            df_melt = pd.melt(df_income, id_vars=['GeoName'])

            df_pie = df_melt.loc[df_melt.GeoName == nta_slct]
            
            # could add the dictionary mapping for the variable names
            df_pie['variable'] = df_pie.variable.map(income_index)

            #print(df.variable)

            fig = px.pie(df_pie, values='value', names='variable', color='variable', title='Income Level for NTA ' + nta_slct)

        return fig 

            
    
def register_racial_callbacks(app, df, nta):
        
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
            [0, "rgb(215,48,39)"], 
            [.02, "rgb(244,109,67)"], 
            [.06, "rgb(253,174,97)"],
            [.1, "rgb(166,206,227)"],
            [.2000, "rgb(31,120,180)"],
            [.3000, "rgb(178,223,138)"],
            [.5000, "rgb(51,160,44)"],
            [.7000, "rgb(251,154,153)"],
            [.9000, "rgb(227,26,28)"],
            [1, "green"]
        ]

        fig = px.choropleth_mapbox(df, geojson=nta, color=df[option_slctd],
                            locations=df["GeoID"], featureidkey="properties.NTA2020",
                            center={"lat": 40.7128, "lon": -74.0060},#-74.1052443755828, 40.5731022653906
                            mapbox_style="carto-positron", zoom=9, 
                            hover_data=[option_slctd, 'GeoID', 'Name'],
                            #custom_data=[]
                            #color_continuous_scale='Bluered_r'
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

def register_sources_callbacks(app):

    @app.callback(
        Output(component_id='', component_property='figure'),
        Input()
    )
    def choropleth_by_source():

        fig = px.choropleth_mapbox(tfed, geojson=nta, color=phasing,
                        locations="NTA2020", featureidkey="properties.NTA2020",
                        center={"lat": 40.7128, "lon": -74.0060},#-74.1052443755828, 40.5731022653906
                        mapbox_style="carto-positron", zoom=9,
                        hover_data=[phasing, 'NTA2020', 'NTAName'])

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig


