#!/usr/bin/env python
# coding: utf-8

# In[14]:


# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# In[96]:


# import dataset

traffic = pd.read_csv('traffic.csv', dtype = {7: 'string', 2: 'string', 4: 'string', 12: 'int'})
traffic = traffic.drop(columns=['Unnamed: 0'])


# In[97]:


# convert time column to format for graphing

time = traffic[['withdrawn', 'time']]
time2 = pd.crosstab(time.time, time.withdrawn)
time3 = time2
time3[2] = time2[1] / (time2[1] + time2[0])


# In[98]:


# plot time of day vs proportion of withdrawn notices

pl = time3[2].plot.line(figsize = (10,10), title = 'Time of Day and Proportion of Expiation Notices Withdrawn')

# label graph

pl.set_xlabel("Time")
pl.set_ylabel("Proportion of Notices Withdrawn");


# In[99]:


# define days

traffic['day'] = pd.to_datetime(traffic['incident_start_date'], errors = 'coerce').dt.dayofweek


# In[100]:


# monday

Monday = traffic[traffic['day'] == 0]
Monday = Monday[['withdrawn', 'time']]
Monday = pd.crosstab(Monday.time, Monday.withdrawn)
Monday[2] = Monday[1] / (Monday[0] + Monday[1])

# tuesday

Tuesday = traffic[traffic['day'] == 1]
Tuesday = Tuesday[['withdrawn', 'time']]
Tuesday = pd.crosstab(Tuesday.time, Tuesday.withdrawn)
Tuesday[2] = Tuesday[1] / (Tuesday[0] + Tuesday[1])

# wednesday

Wednesday = traffic[traffic['day'] == 2]
Wednesday = Wednesday[['withdrawn', 'time']]
Wednesday = pd.crosstab(Wednesday.time, Wednesday.withdrawn)
Wednesday[2] = Wednesday[1] / (Wednesday[0] + Wednesday[1])

# thursday

Thursday = traffic[traffic['day'] == 3]
Thursday = Thursday[['withdrawn', 'time']]
Thursday = pd.crosstab(Thursday.time, Thursday.withdrawn)
Thursday[2] = Thursday[1] / (Thursday[0] + Thursday[1])

# friday

Friday = traffic[traffic['day'] == 4]
Friday = Friday[['withdrawn', 'time']]
Friday = pd.crosstab(Friday.time, Friday.withdrawn)
Friday[2] = Friday[1] / (Friday[0] + Friday[1])

# saturday

Saturday = traffic[traffic['day'] == 5]
Saturday = Saturday[['withdrawn', 'time']]
Saturday = pd.crosstab(Saturday.time, Saturday.withdrawn)
Saturday[2] = Saturday[1] / (Saturday[0] + Saturday[1])

# sunday

Sunday = traffic[traffic['day'] == 6]
Sunday = Sunday[['withdrawn', 'time']]
Sunday = pd.crosstab(Sunday.time, Sunday.withdrawn)
Sunday[2] = Sunday[1] / (Sunday[0] + Sunday[1])


# In[101]:


# capture all days in one

allDays = Monday.drop([0,1,2], axis=1)
allDays['Monday'] = Monday[2]
allDays['Tuesday'] = Tuesday[2]
allDays['Wednesday'] = Wednesday[2]
allDays['Thursday'] = Thursday[2]
allDays['Friday'] = Friday[2]
allDays['Saturday'] = Saturday[2]
allDays['Sunday'] = Sunday[2]
allDays.columns.name = ""


# In[102]:


ax = allDays.plot.line(figsize = (10,10))
ax.set_xlabel("Time")
ax.set_ylabel("Proportion of Notices Withdrawn")
ax.set_title("Time and Proportion of Expiation Notices Withdrawn")

