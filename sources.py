import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd
from callback import register_sources_callbacks


def create_sources_tab(app):

    #conn = create_engine(os.environ.get('ENGINE'))
    conn = create_engine('postgresql://doadmin:l321n3ihac032kya@hed-apr-20-backup-do-user-1939427-0.a.db.ondigitalocean.com:25060/kpdb')

    df = pd.read_sql(
        '''
        SELECT
        COUNT(a.record_id) as project_count,
        SUM(a.within_5_years) as within_5_years,
        SUM(a.from_5_to_10_years) as from_5_to_10_years,
        SUM(a.after_10_years) as after_10_years, 
        a.source as source,
        "NTA2020",
        "NTAName"

        FROM 
        kpdb a
        JOIN nta b
        ON ST_WITHIN(a.geom, b.geometry) 

        ---WHERE 
        ---a.source = 'Neighborhood Study Projected Development Sites'

        GROUP BY
        "NTA2020",
        "NTAName",
        a.source
        '''
    , con=conn)

    @app.callback(
        Output(component_id='sources-choro', component_property='figure'),
        Input(component_id='', component_property='option_select')
    )
    def update_nta_choropleth_sources():

        fig = px.choropleth_mapbox(tfed, geojson=nta, color=phasing,
                            locations="NTA2020", featureidkey="properties.NTA2020",
                            center={"lat": 40.7128, "lon": -74.0060},#-74.1052443755828, 40.5731022653906
                            mapbox_style="carto-positron", zoom=9,
                            hover_data=[phasing, 'NTA2020', 'NTAName'])

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        return fig

    @app.callback(
        Output(component_id='sources-boro-bar', component_property='figure'),
        Input(component_id='', component_property='option_select')
    )
    def update_sources_boro_bar():

        # create bar chart which breaks down the units by their source
        bar_chart = px.bar(f_2, x='NTAName', y=phase_dict[phasing], color='source', category_orders=order, color_discrete_map=color_map)

        bar_chart.update_layout(xaxis=dict(tickmode='linear'))

        st.plotly_chart(bar_chart, use_contrainer_width=True)

        return fig

    @app.callback(
        Output(component_id='sources-nta-bar', component_property='figure'),
        Input(component_id='', component_property='option_select')
    )
    def update_sources_nta_bar():

        # create bar chart which breaks down the units by their source
        bar_chart = px.bar(f_2, x='NTAName', y=phase_dict[phasing], color='source', category_orders=order, color_discrete_map=color_map)

        bar_chart.update_layout(xaxis=dict(tickmode='linear'))

        st.plotly_chart(bar_chart, use_contrainer_width=True)

        return fig
