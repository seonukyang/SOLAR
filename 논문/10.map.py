import  geopandas as gpd
import pandas as pd
import folium 
from folium import plugins
from folium.plugins import MarkerCluster
import numpy as np
import branca
import requests
import json
import matplotlib.pyplot as plt

df = pd.read_csv('SOM_group2_coordinate.csv', encoding = 'cp949')
print(df)

lat = df['latitude']
lon = df['longitude']

plt.figure(figsize=(10, 10))
plt.scatter(lat, lon)

plt.show()