#!/usr/bin/env python
# coding: utf-8

# In[103]:


import pandas as pd
import json
import requests

response = requests.get("https://services.surfline.com/taxonomy?type=taxonomy&id=58f7ed51dadb30820bb3879c&maxDepth=0")
json_data = response.json()
json_contains = json_data['contains']
states = []
state_ids = []
state_urls = []
for x in json_contains:
    states.append(x['name'])
    state_ids.append(x['_id'])

for state_id in state_ids:
    state_urls.append("https://services.surfline.com/taxonomy?type=taxonomy&id=" + state_id + "&maxDepth=0")
    
state_data = []
for state_url in state_urls:
    state_response = requests.get(state_url)
    state_data.append(state_response.json())
    
county_ids = []    
for state in state_data:
    state_contains = state['contains']
    for y in state_contains:
        county_ids.append(y['_id'])
        
county_urls = []
for county_id in county_ids:
    county_urls.append("https://services.surfline.com/taxonomy?type=taxonomy&id=" + county_id + "&maxDepth=0")

county_data = []
for county_url in county_urls:
    county_response = requests.get(county_url)
    county_data.append(county_response.json())
    
region_ids = []
region_names = []
for county in county_data:
    county_contains = county['contains']
    for z in county_contains:
        region_ids.append(z['_id'])
        region_names.append(z['name'])
        
region_urls = []
for region_id in region_ids:
    region_urls.append("https://services.surfline.com/taxonomy?type=taxonomy&id=" + region_id + "&maxDepth=0")

region_data = []
for region_url in region_urls:
    region_response = requests.get(region_url)
    region_data.append(region_response.json())
    
        
spot_ids = []
spot_names = []
spot_lon = []
spot_lat = []
spot_urls = []
for region in region_data:
    region_contains = region['contains']
    if len(region_contains) == 0:
        spot_ids.append(region['_id'])
        spot_names.append(region['name'])
        region_associated = region['associated']
        region_links = region_associated['links']
        region_location = region['location']
        region_coordinates = region_location['coordinates']
        spot_lon.append(region_coordinates[0])
        spot_lat.append(region_coordinates[1])
        for i in region_links:
            if i['key'] == "www":
                spot_urls.append(i['href'])
        
# print(spot_ids)
# print(spot_names)
# print(spot_lon)
# print(spot_lat)
# print(spot_urls)

df = pd.DataFrame({"ids": spot_ids, "names": spot_names, "lon": spot_lon, "lat": spot_lat, "urls": spot_urls})
df.to_csv('spot_list.csv')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




