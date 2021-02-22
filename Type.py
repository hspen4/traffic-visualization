#!/usr/bin/env python
# coding: utf-8

# In[248]:


# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# In[249]:


# import dataset

traffic = pd.read_csv('traffic.csv', dtype = {7: 'string', 2: 'string', 4: 'string', 12: 'int'})
traffic = traffic.drop(columns=['Unnamed: 0'])


# In[287]:


# get offence column

offence = traffic[['withdrawn', 'offence']]


# In[288]:


# graphable format

offence2 = pd.crosstab(offence.offence, offence.withdrawn)
offence3 = offence2
offence3[2] = offence2[1] / (offence2[1] + offence2[0])


# In[289]:


# sort descending

offence3 = offence3.sort_values(by = [2], ascending = False)


# In[351]:


# plot without removal

ax = offence3.head(5).plot.bar(y = 2, figsize = (10,10))
ax.get_legend().remove()
ax.set_title("Category of Offense and Proportion of Withdrawn Expiation Notices")
ax.set_xlabel("Offence")
ax.set_ylabel("Withdrawal Rate");


# In[302]:


# remove offences with not enough data

trimmed = offence3[(offence3[0] + offence3[1]) > 5000]


# In[348]:


# plot with removal

ax = trimmed.head(5).plot.bar(y = 2, figsize = (10,10))
ax.get_legend().remove()
ax.set_title("Category of Offense and Proportion of Withdrawn Expiation Notices")
ax.set_xlabel("Offence")
ax.set_ylabel("Withdrawal Rate")


# In[315]:


# combine similar categories with excel

trimmed.to_csv('names.csv')


# In[322]:


# read back in

combined = pd.read_csv('names_updated.csv', usecols=['offence','not_withdrawn','withdrawn'], nrows=8)


# In[329]:


# get overturn ratio

combined['ratio'] = combined['withdrawn'] / (combined['not_withdrawn'] + combined['withdrawn'])


# In[346]:


ax = combined.sort_values(by = ['ratio'], ascending = False).plot.bar(y = 'ratio', x = 'offence', figsize = (10,10))
ax.set_xlabel("Offence")
ax.set_ylabel("Withdrawal Rate")
ax.get_legend().remove()
ax.set_title("Category of Offense and Proportion of Withdrawn Expiation Notices")

