#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# In[2]:


# import dataset

traffic = pd.read_csv('traffic.csv', dtype = {7: 'string', 2: 'string', 4: 'string', 12: 'int'})
traffic = traffic.drop(columns=['Unnamed: 0'])


# In[18]:


# get area column

area = traffic[['withdrawn', 'area']]


# In[19]:


# put area in graphing format

area = pd.crosstab(area.area, area.withdrawn)
area[2] = area[1] / (area[0] + area[1])


# In[20]:


# regular format

area.index = area.index.str.title()
area.index = area.index.str.strip(' Lsa')
area = area.rename(index = {'Baro' : 'Barossa', 'imestone Coast' : 'Limestone Coast'})
area = area.drop("Unknown")


# In[21]:


area


# In[22]:


# sort descending

area = area.sort_values(by = 2, ascending = False)


# In[23]:


# plot the areas

ax = area.plot.bar(y = 2, figsize = (10,10))
ax.set_xlabel("Area")
ax.set_ylabel("Proportion of Notices Withdrawn")
ax.set_title("Police District and Proportion of Notices Withdrawn")
ax.get_legend().remove()

