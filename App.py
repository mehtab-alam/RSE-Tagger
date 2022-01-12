#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 22:11:50 2021

@author: syed
"""

import folium

import streamlit as st
from streamlit_folium import folium_static
import json
import os


print("streamlit=="+st.__version__)
print("folium=="+folium.__version__)

list_country = os.listdir('geojson')
try:
    list_country.remove('.DS_Store')
except:
    print('Error')
list_country.sort()
option_country = st.selectbox("Select Country",(tuple(list_country)))
if option_country is not None:
    list_city = os.listdir('geojson'+os.path.sep+option_country+os.path.sep+'cities')
    try:    
        list_city.remove('.DS_Store')
    except:
        print('Error')
    list_city.sort()    
    option_city = st.selectbox("Select City",list_city)
    if option_city is not None:
        list_cardinals_with_extensions = os.listdir('geojson'+os.path.sep+option_country.lower()+os.path.sep+'cities'+os.path.sep+option_city.lower())
        list_cardinals = [x.split('.')[0] for x in list_cardinals_with_extensions]
        list_cardinals.sort()
        option_relative = st.selectbox("Select Relative position",list_cardinals)

if st.button('Draw Location'):

    path = 'geojson/'+option_country.lower()+'/cities/'+option_city.lower()+'/'+option_relative.lower()+'.geojson'
    #path1 = 'geojson/'+option_country.lower()+'/cities/'+option_city.lower()+'/south.geojson'
    #path2 = 'geojson/'+option_country.lower()+'/cities/'+option_city.lower()+'/south-east.geojson'
    #path3 = 'geojson/'+option_country.lower()+'/cities/'+option_city.lower()+'/south-west.geojson'
   
    #path = 'geojson/'+option_country.lower()+'/'+option_relative.lower()+'.geojson'
    #path = 'geojson/'+option_country.lower()+'/'+'centeral'+'.geojson'
    
    with open(path) as f:
        gj = json.load(f)
        centroid = gj['features'][0]['properties']['centroid']
    
        centroid = (centroid[0],centroid[1])
        my_map = folium.Map(location=[centroid[1], centroid[0]],
                                        zoom_start = 11)
        folium.GeoJson(
            path,
            style_function = lambda x: {
                'fillColor': 'green',
                'color': 'black',
                'weight': 2.5,
                'fillOpacity': 0.3
            },
        name= option_city.lower()).add_to(my_map)
        
       
        
        folium_static(my_map)

