import streamlit as st
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static



# data setup


df = pd.read_csv('restaurants.csv')
df_table = df[['name,' 'city', 'cuisine', 'neighborhood', 'description', 'link', 'address', 'date']]

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




# title
st.title("New Spots on Resy")

# display table.
if 'id' in df_table.columns:
    df_table = df_table.drop(columns=['id'])
    st.write(df_table)

# display map
folium_static(m)


