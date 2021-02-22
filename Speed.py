#!/usr/bin/env python
# coding: utf-8

# In[32]:


# import libraries

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# In[82]:


# import dataset

traffic = pd.read_csv('traffic.csv', dtype = {7: 'string', 2: 'string', 4: 'string', 12: 'int'})
traffic = traffic.drop(columns=['Unnamed: 0'])


# In[83]:


# get speed column

speed = traffic
speed = speed[['withdrawn', 'speed']]


# In[84]:


# split into speed segments

# speed1 = speed[(speed['speed'] > 0) & (speed['speed'] <= 20)]
# speed2 = speed[(speed['speed'] > 20) & (speed['speed'] <= 40)]
speed3 = speed[(speed['speed'] > 40) & (speed['speed'] <= 60)]
speed4 = speed[(speed['speed'] > 60) & (speed['speed'] <= 80)]
speed5 = speed[(speed['speed'] > 80) & (speed['speed'] <= 100)]
speed6 = speed[(speed['speed'] > 100) & (speed['speed'] <= 120)]
speed7 = speed[(speed['speed'] > 120) & (speed['speed'] <= 140)]
speed8 = speed[(speed['speed'] > 140) & (speed['speed'] <= 160)]


# In[85]:


# combine the arrays of each segment

speedComb = {'Speed': ['50', '70', '90', '110', '130', '150'], 'Withdrawn': [0,0,0,0,0,0]}
arrays = [speed3, speed4, speed5, speed6, speed7, speed8]

# get the overturn rate for each speed segment

for i in range(len(arrays)):
    speedComb['Withdrawn'][i] = arrays[i]['withdrawn'].sum() / len(arrays[i])


# In[86]:


# place into new dataframe

newSpeed = (pd.DataFrame(data = speedComb))


# In[87]:


# plot speed against overturn ratio

plt.figure(figsize = (10,10))
ax = plt.bar(x = newSpeed['Speed'], height = newSpeed['Withdrawn'], width = 1)
plt.xlabel('Car Speed (km/h)')
plt.ylabel('Proportion of Withdrawn Notices')
plt.ylim([0,0.035])
plt.title('Relation between Car Speed and Probability of a Withdrawn Notice, for All Fines');


# In[88]:


# get speed column for second plot

speed = traffic
speed = traffic[traffic['camera'] == 'OTHER']
speed = speed[['withdrawn', 'speed']]


# In[89]:


# split into speed segments

# speed1 = speed[(speed['speed'] > 0) & (speed['speed'] <= 20)]
# speed2 = speed[(speed['speed'] > 20) & (speed['speed'] <= 40)]
speed3 = speed[(speed['speed'] > 40) & (speed['speed'] <= 60)]
speed4 = speed[(speed['speed'] > 60) & (speed['speed'] <= 80)]
speed5 = speed[(speed['speed'] > 80) & (speed['speed'] <= 100)]
speed6 = speed[(speed['speed'] > 100) & (speed['speed'] <= 120)]
speed7 = speed[(speed['speed'] > 120) & (speed['speed'] <= 140)]
speed8 = speed[(speed['speed'] > 140) & (speed['speed'] <= 160)]


# In[90]:


# combine the arrays of each segment

speedComb = {'Speed': ['50', '70', '90', '110', '130', '150'], 'Withdrawn': [0,0,0,0,0,0]}
arrays = [speed3, speed4, speed5, speed6, speed7, speed8]

# get the overturn rate for each speed segment

for i in range(len(arrays)):
    speedComb['Withdrawn'][i] = arrays[i]['withdrawn'].sum() / len(arrays[i])


# In[91]:


# place into new dataframe

newSpeed = (pd.DataFrame(data = speedComb))


# In[92]:


# plot speed against overturn ratio

plt.figure(figsize = (10,10))
ax = plt.bar(x = newSpeed['Speed'], height = newSpeed['Withdrawn'], width = 1)
plt.xlabel('Car Speed (km/h)')
plt.ylabel('Proportion of Withdrawn Notices')
plt.ylim([0,0.035])
plt.title('Relation between Car Speed and Probability of a Withdrawn Notice, for Human-Issued Fines');

