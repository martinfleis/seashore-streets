#!/usr/bin/env python
# coding: utf-8

# # Flood risk modelling based on DTM
# 
# Computational notebook 05 for Climate adaptation plans in the context of coastal settlements: the case of Portugal.
# 
# Date: 27/06/2020
# 
# ---
# 
# This notebooks models floor risk under "what if" +5 m scenario based on digital terrain model on Portuguese coast provided by Direção-Geral do Território (DGT) - `Modelo Digital do Terreno das Zonas Costeiras de Portugal Continental com resolução de 1 m (400 m em terra) - LiDAR, 2011-12-07`. Unfortunately, we do not hold rights to share the data within this repository.
# 
# DTM data are stored in separate ASC files based on the grid defined in `MDT1m_LiDAR2011_secciona.shp`.
# 
# 
# `name_tess` layers require additional attribute `main` to be set to 1 for cells in the first row. Note that this information was not used in the final manuscript.
# 
# Structure of data:
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
# ./MDT/
#     MDT1m_LiDAR2011_secciona.shp
#     002_1_55-top_orto.asc
#     002_2_53-top_orto.asc
#     ...
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


import geopandas as gpd
import rasterio as rio
from rasterio.merge import merge
import rasterstats
import pandas as pd
import numpy as np
import fiona


# In[2]:


fiona.__version__, gpd.__version__, rio.__version__, rasterstats.__version__, np.__version__, pd.__version__


# In[174]:


grid = gpd.read_file('MDT/MDT1m_LiDAR2011_secciona.shp')


# In[197]:


folder = '/Users/martin/Dropbox/Academia/Data/Geo/Portugal/'


# In[201]:


parts = ['atlantic', 'preatl', 'premed', 'med']
for part in parts:
    path = folder + part + '.gpkg'
    layers = [x[:-4] for x in fiona.listlayers(path) if 'blg' in x]
    for l in layers:
        blg = gpd.read_file(path, layer=l + '_blg')
        case = gpd.read_file(path, layer=l + '_case')
        
        rparts = grid[grid.intersects(case.unary_union)].Id_Unidade
        rasters = []
        for rpart in rparts:
            rpath = 'MDT/' + rpart + '-top_orto.asc'
            rasters.append(rio.open(rpath))
        if len(rasters) > 1:
            array, affine = merge(rasters)
            stats = rasterstats.zonal_stats(blg, array[0], affine=affine, stats=['min', 'max', 'median', 'mean', 'count'])
        else:
            stats = rasterstats.zonal_stats(blg, rasters[0].read(1), affine=rasters[0].transform, stats=['min', 'max', 'median', 'mean', 'count'])
        if 'min' in blg.columns:
            blg = blg.drop(columns=['min', 'max', 'median', 'mean', 'count'])
        blg = blg.join(pd.DataFrame(stats))
        blg.to_file(path, layer=l + '_blg', driver='GPKG')
        print(part, l, 'done')


# In[210]:


parts = ['atlantic', 'preatl', 'premed', 'med']
for part in parts:
    path = folder + part + '.gpkg'
    layers = [x[:-4] for x in fiona.listlayers(path) if 'blg' in x]
    for l in layers:
        blg = gpd.read_file(path, layer=l + '_blg')
        blg = blg.replace(-999, np.nan)
        print(part, l, '- NaN in min:', blg['min'].isna().sum(), '/', len(blg))


# In[213]:


parts = ['atlantic', 'preatl', 'premed', 'med']
for part in parts:
    path = folder + part + '.gpkg'
    layers = [x[:-4] for x in fiona.listlayers(path) if 'blg' in x]
    for l in layers:
        blg = gpd.read_file(path, layer=l + '_blg')
        blg = blg.replace(-999, np.nan)
        print(part, l, (blg['min']< 5).sum(), (blg['min']< 5).sum() / len(blg))


# In[249]:


waterrelation = pd.DataFrame()


# In[251]:


parts = ['atlantic', 'preatl', 'premed', 'med']
for part in parts:
    path = folder + part + '.gpkg'
    layers = [x[:-4] for x in fiona.listlayers(path) if 'blg' in x]
    for l in layers:
        buildings = gpd.read_file(path, layer=l + '_blg')
        tessellation = gpd.read_file(path, layer=l + '_tess')
        
        buildings = buildings.merge(tessellation[['uID', 'main']], on='uID', how='left')
        if 'main' not in buildings.columns:
            import warnings
            warnings.warn(l)
        main = buildings[buildings['main'] == 1]
        
        if 'part' in main.columns:
            for part in set(main.part):
                subset = main.loc[main.part == part]
                mainset = buildings.loc[buildings.part == part]
                
                waterrelation.loc[l + str(part), 'min' + '_min'] = subset['min'].min()
                waterrelation.loc[l + str(part), 'min' + '_med'] = subset['min'].median()   
                waterrelation.loc[l + str(part), 'flooded_perc'] = (mainset['min']< 5).sum() / len(mainset)
    
        else:
            waterrelation.loc[l, 'min' + '_min'] = main['min'].min()
            waterrelation.loc[l, 'min' + '_med'] = main['min'].median()  
            waterrelation.loc[l, 'flooded_perc'] = (buildings['min']< 5).sum() / len(buildings)


# In[253]:


waterrelation.to_csv('data/waterrelation_data.csv')

