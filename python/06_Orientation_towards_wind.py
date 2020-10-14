#!/usr/bin/env python
# coding: utf-8

# # Measure orientation of seashore streets in relation to SW wind
# 
# Computational notebook 06 for Climate adaptation plans in the context of coastal settlements: the case of Portugal.
# 
# Date: 27/06/2020
# 
# ---
# 
# This notebook computes deviation of seashore street orientation from SW wind direction (45 degrees). 
# 
# Requires attribute `case` in `name_str` capturing which LineStrings form the seashore street itself. (1 - True) (already used in `03_Calculate_contextual_characters.ipynb`.
# 
# Structure of GeoPackages:
# 
# ```
# ./data/
#     atlantic.gpkg
#         name_blg    - Polygon layers
#         name_str    - LineString layers
#         name_case   - Polygon layers
#         name_tess   - Polygon layers
#         name_blocks - Polygon layers
#         ...
#      preatl.gpkg
#         name_blg
#         name_str
#         name_case
#         ...
#      premed.gpkg
#         name_blg
#         name_str
#         name_case
#         ...
#      med.gpkg
#         name_blg
#         name_str
#         name_case
#         ...
# ```
# 
# CRS of the original data is EPSG:3763.
# 
# ```
# <Projected CRS: EPSG:3763>
# Name: ETRS89 / Portugal TM06
# Axis Info [cartesian]:
# - X[east]: Easting (metre)
# - Y[north]: Northing (metre)
# Area of Use:
# - name: Portugal - mainland - onshore
# - bounds: (-9.56, 36.95, -6.19, 42.16)
# Coordinate Operation:
# - name: Portugual TM06
# - method: Transverse Mercator
# Datum: European Terrestrial Reference System 1989
# - Ellipsoid: GRS 1980
# - Prime Meridian: Greenwich
# ```

# In[1]:


import fiona
import geopandas as gpd
import shapely
import numpy as np
import pandas as pd


# In[2]:


fiona.__version__, gpd.__version__, shapely.__version__, np.__version__, pd.__version__


# In[ ]:


from shapely.ops import linemerge

def wind_issue(line, wind_angle=45):
    coords = line.coords
    angle = np.arctan2(coords[-1][0] - coords[0][0], coords[-1][1] - coords[0][1])
    az = np.degrees(angle)
    
    if az < wind_angle:
        az += 180
    az -= wind_angle
    if az < 0:
        az = az * -1
    if 90 < az <= 180:
        diff = az - 90
        az = az - 2 * diff
    return az / 90


wind = pd.DataFrame(columns=['place', 'winddev'])
ix = 0

parts = ['atlantic', 'preatl', 'premed', 'med']

for part in parts:
    path = folder + part + '.gpkg'
    layers = [x[:-4] for x in fiona.listlayers(path) if 'blg' in x]
    for l in layers:
        streets = gpd.read_file(path, layer=l + '_str')
        seashore = streets[streets.case == 1].geometry.to_list()
        merged = linemerge(seashore)
        if merged.type != 'LineString':
            dims = {}
            for i, seg in enumerate(merged):
                dims[i] = seg.length
            key = max(dims, key=dims.get)
            wind.loc[ix] = [l, wind_issue(merged[key])]
            ix += 1
        else:
            wind.loc[ix] = [l, wind_issue(merged)]
            ix += 1


# In[ ]:


wind.to_csv(folder + 'wind_relation.csv')

