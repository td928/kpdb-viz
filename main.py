import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from urllib.request import urlopen
import json

def main():

##########################################
#Side Panel functionality
##########################################

    df = load_data()
    # let user select the aggregation date field and load the data bsed on selection
    st.sidebar.header("Horizontal Axis")

    phasing = st.sidebar.selectbox("Select the phasing option to filter",
        options=("Within 5 Years", "From 5 to 10 Years", "After 10 Years"), index=0)

    filtered = filter_phasing(phasing, df)

    sources = filtered.source.unique().tolist()

    sources_select = st.sidebar.multiselect('Select the sources you want to include in the map', 
        options=sources, default=sources)

    units_vs_projects = st.sidebar.radio(label='View of number of projects or units', 
        options=('Number of Units', 'Number of Projects'))

    tfed = transform(filtered, sources_select)


 #########################################################################
 #Main Panel content starts here
 ##########################################################################   

    st.title('Real Time Development Tracker')

    st.header('About the Tracker')
    st.info("""
    
    """)

    # create a accruate title for the graph based on the criteria selected (job type,)
    #st.subheader(graph_format[0])

    

    #start the executive summary section
    st.header('Excutive Summary for Week Beginning May 25')

    st.info("""
    ### Job Applications Filings
    """)

    st.dataframe(filtered)

    st.dataframe(tfed)

    st.plotly_chart(visualize(tfed, phasing), use_contrainer_width=True)

    #st.bar_chart(tfed)

@st.cache
def load_data():

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
        "NTA2020"

        FROM 
        export a
        JOIN nta b
        ON ST_WITHIN(a.geom, b.geometry) 

        GROUP BY
        "NTA2020",
        a.source
        '''
    , con=conn)

    return df

@st.cache
def filter_phasing(phasing, df):

    phase_dict = {
                    'Within 5 Years': 'within_5_years',
                    'From 5 to 10 Years': 'from_5_to_10_years',
                    'After 10 Years': 'after_10_years'
                }


    filtered = df.loc[(df[phase_dict[phasing]] != 0)]

    #if phasing == 'Within 5 Years':

    #    filtered = df.loc[(df.within_5_years != 0)]
    
    #elif phasing == 'From 5 to 10 Years':

    #    filtered = df.loc[(df.from_5_to_10_years != 0)]

    #else:

    #    filtered = df.loc[(df.after_10_years != 0)]

    return filtered

@st.cache
def transform(f, ss):

  tfed = f.loc[f.source.isin(ss)].groupby('NTA2020').sum().reset_index()

  return tfed

@st.cache
def load_nta():
    with urlopen('https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Neighborhood_Tabulation_Areas_2020/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson') as response:
        nta = json.load(response)

def visualize(tfed, phasing):

    nta = load_nta()

    phase_dict = {
        'Within 5 Years': 'within_5_years',
        'From 5 to 10 Years': 'from_5_to_10_years',
        'After 10 Years': 'after_10_years'
    }

    fig = px.choropleth_mapbox(tfed, geojson=nta, color=phase_dict[phasing],
                        locations=tfed["NTA2020"], featureidkey="properties.NTA2020",
                        center={"lat": 40.5731022653906, "lon": -74.1052443755828},#-74.1052443755828, 40.5731022653906
                        mapbox_style="carto-positron", zoom=9)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

if __name__ == "__main__":

    main()

