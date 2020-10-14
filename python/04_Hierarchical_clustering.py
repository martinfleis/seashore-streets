#!/usr/bin/env python
# coding: utf-8

# # Hierarchical agglomerative clustering of cases
# 
# Computational notebook 04 for Climate adaptation plans in the context of coastal settlements: the case of Portugal.
# 
# Date: 27/06/2020
# 
# ---
# 
# This notebooks standardize contextual characters and generates hierarchical clustering using Ward's method.
# 
# The only input required is `summative_data.csv` generated by `03_Calculate_contextual_characters.ipynb`.

# In[3]:


import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
from sklearn import preprocessing
import scipy as sp
from scipy.cluster import hierarchy


# In[19]:


sklearn.__version__, sp.__version__, pd.__version__, matplotlib.__version__


# In[5]:


path = 'data/summative_data.csv'
data = pd.read_csv(path, index_col=0)


# In[14]:


data


# ## Standardize

# In[15]:


x = data.values
scaler = preprocessing.StandardScaler()
cols = list(data.columns)
data[cols] = scaler.fit_transform(data[cols])
data


# In[16]:


data.to_csv('data/summative_data_norm.csv')


# ## Clustering

# In[17]:


Z = hierarchy.linkage(data, 'ward')


# In[18]:


plt.figure(figsize=(10, 25))
dn = hierarchy.dendrogram(Z, labels=data.index, orientation='right',
                          color_threshold=18)
#plt.savefig('dendrogram_right.svg')


# ## Assing to places

# In[ ]:


folder = 'data/'
parts = ['atlantic', 'preatl', 'premed', 'med']

c_parts = []
geoms = []
for part in parts:
    path = folder + part + '.gpkg'
    layers = [x[:-4] for x in fiona.listlayers(path) if 'blg' in x]
    for l in layers:
        buildings = gpd.read_file(path, layer=l + '_blg')
        
        if 'part' in buildings.columns:
            for bpart in set(buildings.part):
                subset = buildings.loc[buildings.part == bpart]
                geoms.append(subset.geometry.unary_union.centroid)
                c_parts.append(part)
        else:
            geoms.append(buildings.geometry.unary_union.centroid)
            c_parts.append(part)


# In[ ]:


gdf = gpd.GeoDataFrame(data, geometry=geoms)
gdf['part'] = c_parts


# In[ ]:


gdf['cl'] = hierarchy.fcluster(Z, 18, criterion='distance')
gdf['cl'] = gdf.cl.replace(8, 7)
gdf['cl'] = gdf.cl.replace(2, 3)


# In[ ]:


gdf.reset_index().to_file('data/points.gpkg', driver='GPKG', layer='ward')

