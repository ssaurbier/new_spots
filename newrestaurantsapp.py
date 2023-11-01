import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static



# data setup


# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM mytable;', ttl="10m")

# Filter out data older than 60 days
today = datetime.today()
cutoff_date = today - timedelta(days=60)
df = df[pd.to_datetime(df['date']) > cutoff_date]

# Handle NaNs
df = df.dropna(subset=['latitude', 'longitude'])

# Create map
m = folium.Map(location=[39, -96.5], zoom_start=4)  

for _, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name']
    ).add_to(m)







# displays





st.title("New Spots on Resy")

# container and placeholders for the map and table. This only works if you can't read this code.
st.markdown("""
<div class="container">
    <div class="map-container" class="folium-map leaflet-container leaflet-touch leaflet-retina leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom"></div>
    <div class="table-container" class="dvn-scroller glideDataEditor"></div>
</div>
""", unsafe_allow_html=True)

# placeholders for the map and table.
map_placeholder = st.empty()
table_placeholder = st.empty()

# display map.
map_placeholder.write(folium_static(m, use_container_width=True))

# display table.
if 'id' in df.columns:
    df = df.drop(columns=['id'])
table_placeholder.write(df)
