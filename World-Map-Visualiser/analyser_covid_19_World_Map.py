

# URL's for the dynamic data from the multiple sources combined together

confirmed_data_source = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
deaths_data_source    = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
recovered_data_source = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

# importing various libraries 

import folium        
import numpy as np    
import pandas as pd
from folium.plugins import MarkerCluster

# Reading whole data from csv files

daily_confirmed_data = pd.read_csv(confirmed_data_source)
daily_death_data     = pd.read_csv(deaths_data_source)
daily_recovered_data = pd.read_csv(recovered_data_source)

# Extracting required data i.e. current or latest data

def get_latest_data(df):
  return df.iloc[:, [0, 1, 2, 3, -1]]

# Main function that makes the map

def get_map(df):
  df = get_latest_data(df)
  # Function that gives the colour to on the basis of severity of situations

  def color_change(c):
    if(c > 50):
        return('red')
    elif(25 <= c <= 49):
        return('orange')
    elif(10 <= c <= 25):
        return('green')
    else:
        return('yellow')

  # Helper function
  
  def get_province(name):
    if name is np.nan:
      return ''
    else:
      return '(' + name + ')' 
    
  # Create base map
  
  London = [51.506949, -0.122876]
  map = folium.Map(location = London,
                  zoom_start = 2, 
                  tiles = "CartoDB dark_matter")
  
  # Making clusters for better visuals on map

  marker_cluster = MarkerCluster().add_to(map)

  # Adding markers on various locations


  for index, row in df.iterrows(): 
      folium.CircleMarker(location = [row['Lat'], row['Long']],
                          radius = 9, 
                          popup = row['Country/Region'] + get_province(row['Province/State']) + ' ' + str(row[-1]), 
                          fill_color = color_change(row[-1]), 
                          color = "gray", 
                          fill_opacity = 0.9).add_to(marker_cluster)
  return map


# For getting map for confirmed cases of CoViD 19 in various countries and provinces
get_map(daily_confirmed_data)

