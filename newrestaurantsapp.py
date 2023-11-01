import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static



# data setup


def fetch_data():
    conn = psycopg2.connect(
        database=st.secrets["database"]["database"], 
        user=st.secrets["database"]["user"], 
        password=st.secrets["database"]["password"], 
        host=st.secrets["database"]["host"], 
        port=st.secrets["database"]["port"]
    )

    query = "SELECT * FROM restaurants;"
    df = pd.read_sql(query, conn)

    cols = ['name', 'city', 'cuisine', 'neighborhood', 'description', 'link', 'address', 'date', 'latitude', 'longitude']
    df = df[cols]

    conn.close()
    return df

# get data
data = fetch_data()

# Filter out data older than 60 days
today = datetime.today()
cutoff_date = today - timedelta(days=60)
data = data[pd.to_datetime(data['date']) > cutoff_date]

# nans
data = data.dropna(subset=['latitude', 'longitude'])


# create map
m = folium.Map(location=[39, -96.5], zoom_start=4)  

for _, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name']
    ).add_to(m)








# displays






st.title("New Spots on Resy")

# container and placeholders for the map and table. This only working if you can't read this code
st.markdown("""
<div class="container">
    <div class="map-container" class="folium-map leaflet-container leaflet-touch leaflet-retina leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom"></div>
    <div class="table-container" class="dvn-scroller glideDataEditor"></div>
</div>
""", unsafe_allow_html=True)

# placeholders for the map and table
map_placeholder = st.empty()
table_placeholder = st.empty()

# display map 
folium_static(m)

# display table 
if 'id' in data.columns:
    data = data.drop(columns=['id'])
table_placeholder.write(data)
