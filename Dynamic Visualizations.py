#!/usr/bin/env python
# coding: utf-8

# **Analysis of Traffic Camera Use in South Australia**
# 
# Below is the code used to process datasets provided by the South Australian Police on the Data SA website into pandas dataframes to be graphed. The process is split into sections for each of the four visualizations, which are displayed at the bottom, along with instructions.

# In[1]:


# import libraries, set options

import pandas as pd
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
import plotly.express as px
import plotly.io as pio
import numpy as np
pd.set_option("display.max_rows", False, "display.max_columns", False)
pd.options.mode.chained_assignment = None


# In[2]:


# import dataset

traffic = pd.read_csv('traffic.csv', dtype = {7: 'string', 2: 'string', 4: 'string', 12: 'string', 13: 'int'})


# In[3]:


# rename columns

traffic = traffic.drop(columns=['Unnamed: 0'])
traffic['year'] = traffic['incident_start_date'].str[:4]
traffic['month'] = traffic['incident_start_date'].astype(str).str[:7]
traffic['incident_start_date'] = pd.to_datetime(traffic['incident_start_date'])
traffic.month = pd.to_datetime(traffic.month)
traffic.incident_start_date = pd.to_datetime(traffic.incident_start_date)
cameras = traffic[traffic.camera != 'OTHER']
humans = traffic[traffic.camera == 'OTHER']


# In[4]:


# grouping by mean

def getMeans(df, col):
    return df.groupby(col).mean()

speedTrafficDay = getMeans(cameras, 'incident_start_date')
speedTrafficMonth = getMeans(cameras, 'month')
speedTrafficYear = getMeans(cameras, 'year')

humanTrafficDay = getMeans(humans, 'incident_start_date')
humanTrafficMonth = getMeans(humans, 'month')
humanTrafficYear = getMeans(humans, 'year')


# In[5]:


# get mean penalty

penalty = getMeans(traffic, ['camera','year'])
penalty = penalty.rename(index={'OTHER' : 'Human', 'FIXED CAMERA' : 'Fixed Camera', 'MOBILE CAMERA' : 'Mobile Camera'})
penalty = penalty.reset_index(level=[0,1])
penalty = penalty.rename(columns = {'camera' : 'Policing Type', 'year' : 'Year', 'penalty' : 'Fine'})


# In[6]:


# create bar chart

bar = px.bar(penalty, x="Policing Type", y="Fine", color="Policing Type",
animation_frame="Year", animation_group="Policing Type", range_y=[0, 600], 
title = "Average Cost of Fine Issued by Different Policing Types")
bar = bar.update(layout=dict(title=dict(text = "Average Cost of Fine Issued by Different Policing Types",
xanchor = 'center', x = 0.465)))


# In[7]:


# counting functions

def getCounts(df, col):
    return df[col].value_counts().sort_index()

camCountDay = getCounts(cameras, 'incident_start_date')
camCountMonth = getCounts(cameras, 'month')
camCountYear = getCounts(cameras, 'year')

humanCountDay = getCounts(humans, 'incident_start_date')
humanCountMonth = getCounts(humans, 'month')
humanCountYear = getCounts(humans, 'year')


# In[8]:


# create line plot

fig1 = go.Scatter(x = camCountDay.index, y = camCountDay, mode = 'lines', line_color = '#345060', name = 'Camera-issued Fines', visible = True)

fig2 = go.Scatter(x = humanCountDay.index, y = humanCountDay, mode = 'lines', line_color = '#D0EF78', name = 'Human-issued Fines', visible = True)

data = [fig1, fig2]
line = go.Figure(data=data, layout = dict(title = dict(text = 'Number of Fines Issued by Traffic Cameras vs Humans', xanchor = 'center', yanchor = 'top', x=0.43, y = 0.93)))

line = line.update_layout (
    updatemenus = [
        
        dict (
            
            buttons = list ([
                
                dict(args = [{"x": [camCountDay.index, humanCountDay.index], "y" : [camCountDay, humanCountDay]}], label = 'Day', method = 'restyle'),
                dict(args = [{"x": [camCountMonth.index, humanCountMonth.index], "y" : [camCountMonth, humanCountMonth]}], label = 'Month', method = 'restyle'),
                dict(args = [{"x": [camCountYear.index, humanCountYear.index], "y" : [camCountYear, humanCountYear]}], label = 'Year', method = 'restyle')
                
            ]), 
            
            xanchor = 'left', 
            
            yanchor = 'top', 
            
            x = 1.15,
            
            y = 0.72415            
        ),
        
        dict (
        
            buttons = list ([
                
                dict (
                    
                    args = [{"visible": ["legendonly", True]}, {"title" : "Number of Fines Issued by Humans", "title.x" : 0.45}],
                    label = "           Humans         ",
                    method = "update"
                    
                ),
                dict (
                    
                    args = [{"visible": [True, "legendonly"]}, {"title" : "Number of Fines Issued by Traffic Cameras", "title.x" : 0.45}],
                    label = "           Cameras       ",
                    method = "update"
                    
                ),
                dict (
                    
                    args = [{"visible": [True, True]}, {"title" : "Number of Fines Issued by Traffic Cameras vs Humans", "title.x" : 0.43}],
                    label = "             Both             ",
                    method = "update"
                    
                )

            ]),
            
            type = "buttons",
            
            showactive = True,
            
            x = 1.273,
            y = -0.01,
            
            active = 2
                    
        )
        
    ],
    
    xaxis_title = "Date",
    
    yaxis_title = "Number of Fines",
    
    legend = dict(font = dict(size = 13)),
    
    #plot_bgcolor = 'white',
    
    xaxis=dict(rangeslider=dict(visible=True), rangeselector=dict(
        buttons = list ([
            dict(label = "Month", step = "month", stepmode = "backward"),
            dict(label = "Year", step = "year", stepmode = "backward"),
            dict(label = "Decade", step = "all", stepmode = "backward"),
        ])))

    
)

line = line.add_annotation (

    dict (text = "Fines per", yref = 'paper', xref = 'paper', y = 0.7, x = 1.14, showarrow = False, font = dict(size=13))
    
)

line = line.add_annotation (

    dict (text = "Show", yref = 'paper', xref = 'paper', y = 0.025, x = 1.19, showarrow = False, font = dict(size=13))
    
)

line = line.add_annotation (

    dict (text = "View past:", yref = 'paper', xref = 'paper', y = 1.10455, x = -0.104, showarrow = False, font = dict(size=12))
    
)

line = line.add_shape (

    dict (type = 'line', yref = 'paper', xref = 'paper', x0 = 1.02, x1 = 1.3, y0 = 0.77, y1 = 0.77)

)

line = line.add_shape (

    dict (type = 'line', yref = 'paper', xref = 'paper', x0 = 1.02, x1 = 1.3, y0 = 0.14, y1 = 0.14)

)


# In[9]:


# import camera datasets

fixed = pd.read_excel('fixed-cameras.xlsx')
mobile = pd.read_csv('mobile-cameras.csv')


# In[10]:


# rename fixed dataset

fixed[['Road', 'Suburb']] = fixed.Location.str.split(',',expand=True)
fixed.Suburb = fixed.Suburb.str.title()


# In[11]:


# rename mobile dataset

mobile = mobile.rename(columns = {'CAMERA_LOCATION_CODE' : 'Code', 'SUBURB_NAME' : 'Suburb'})
mobile.ROAD_NAME = mobile.ROAD_NAME.replace(np.nan, '', regex=True)
mobile.ROAD_TYPE = mobile.ROAD_TYPE.replace(np.nan, '', regex=True)
mobile['Road'] = mobile['ROAD_NAME'] + ' ' + mobile['ROAD_TYPE']
mobile.Road = mobile.Road.str.title()
mobile.Suburb = mobile.Suburb.str.title()
mobile = mobile.drop(axis=1, labels = {"ROAD_NAME", "ROAD_TYPE"})
mobile = mobile.dropna(axis = 0)


# In[12]:


# fixed camera dataset processing

fix0 = traffic[traffic.camera == 'FIXED CAMERA']
fix = fix0[['withdrawn', 'fixed', 'year']]
fix2 = fix.groupby(['year', 'fixed']).withdrawn.value_counts()
fix3 = fix2
e = fix3.to_frame()
e = e.reset_index(level=[0,1])
e['status'] = e.index
e = e.reset_index(drop = True)
e['one'] = 'NaN'
e['zero'] = 'NaN'
for i in range(len(e)):
    if e.iloc[i]['status'] == 0:
        if (i < (len(e) - 1)) and (e.iloc[i + 1]['status'] == 1):
            e.loc[i, 'one'] = e.iloc[i + 1].withdrawn + e.iloc[i].withdrawn
            e.loc[i, 'zero'] = e.iloc[i + 1].withdrawn
        else:
            e.loc[i, 'one'] = e.iloc[i].withdrawn
            e.loc[i, 'zero'] = 0
fix3 = e[e.status == 0]
fix3 = fix3.set_index("fixed")
fix3 = fix3.drop(["withdrawn", "status"], axis = 1)
fix3['two'] = fix3['zero'] / fix3['one']
fix3 = fix3.rename(columns = {'one' : 1, "zero" : 0, "two" : 2})


# In[13]:


# mobile camera dataset processing

mobil0 = traffic[traffic.camera == 'MOBILE CAMERA']
mobil = mobil0[['withdrawn', 'mobile', 'year']]
mobil2 = mobil.groupby(['year', 'mobile']).withdrawn.value_counts()
mobil3 = mobil2
e = mobil3.to_frame()
e = e.reset_index(level=[0,1])
e['status'] = e.index
e = e.reset_index(drop = True)
e['one'] = 'NaN'
e['zero'] = 'NaN'
for i in range(len(e)):
    if e.iloc[i]['status'] == 0:
        if (i < (len(e) - 1)) and (e.iloc[i + 1]['status'] == 1):
            e.loc[i, 'one'] = e.iloc[i + 1].withdrawn + e.iloc[i].withdrawn
            e.loc[i, 'zero'] = e.iloc[i + 1].withdrawn
        else:
            e.loc[i, 'one'] = e.iloc[i].withdrawn
            e.loc[i, 'zero'] = 0
mobil3 = e[e.status == 0]
mobil3 = mobil3.set_index("mobile")
mobil3 = mobil3.drop(["withdrawn", "status"], axis = 1)
mobil3['two'] = mobil3['zero'] / mobil3['one']
mobil3 = mobil3.rename(columns = {'one' : 1, "zero" : 0, "two" : 2})


# In[14]:


# concatenate fixed and mobile datasets along with camera density

fixed.Suburb = fixed.Suburb.str.lstrip()
fixed.Road = fixed.Road.str.lstrip()
mobile.Suburb = mobile.Suburb.str.lstrip()
mobile.Road = mobile.Road.str.lstrip()

d = fixed.append(mobile)
b = d.Road.value_counts()
c = d.Suburb.value_counts()

fixed['Density'] = 'NaN'
fix3['density'] = 'NaN'
for i in range(len(fixed)):
    fixed['Density'][i] = b[fixed.iloc[i].Road]
for i in range(len(fix3)):
    if int(fix3.iloc[i].name) in fixed.Code.values:
        fix3.loc[int(fix3.iloc[i].name),'density'] = ((fixed.set_index("Code")).loc[int(fix3.iloc[i].name)]).Density
fix3=fix3[fix3.density != 'NaN']
fix3.density = fix3.density.astype('int')

fixed['Suburb_Density'] = 'NaN'
fix3['suburb_density'] = 'NaN'
for i in range(len(fixed)):
    fixed['Suburb_Density'][i] = c[fixed.iloc[i].Suburb]
for i in range(len(fix3)):
    if int(fix3.iloc[i].name) in fixed.Code.values:
        fix3.loc[int(fix3.iloc[i].name),'suburb_density'] = ((fixed.set_index("Code")).loc[int(fix3.iloc[i].name)]).Suburb_Density
fix3=fix3[fix3.suburb_density != 'NaN']
fix3.suburb_density = fix3.suburb_density.astype('int')

fix3['road'] = 'NaN'
fix3['type'] = 'NaN'
for i in range(len(fix3)):
    fix3.loc[int(fix3.iloc[i].name),'road'] = ((fixed.set_index("Code")).loc[int(fix3.iloc[i].name)]).Road
    fix3.loc[int(fix3.iloc[i].name),'suburb'] = ((fixed.set_index("Code")).loc[int(fix3.iloc[i].name)]).Suburb
    fix3.loc[int(fix3.iloc[i].name),'type'] = ((fixed.set_index("Code")).loc[int(fix3.iloc[i].name)]).Type
foxed = fixed
fix4 = fix3

fixed = mobile
fixed = fixed.reset_index()
fix3 = mobil3
b = fixed.Road.value_counts()
fixed['Density'] = 'NaN'
fix3['density'] = 'NaN'
for i in range(len(fixed)):
    fixed['Density'][i] = b[fixed.iloc[i].Road]
for i in range(len(fix3)):
    if int(fix3.iloc[i].name) in fixed.Code.values:
        fix3.loc[int(fix3.iloc[i].name),'density'] = ((fixed.set_index("Code")).loc[int(fix3.iloc[i].name)]).Density
fix3=fix3[fix3.density != 'NaN']
fix3.density = fix3.density.astype('int')

fixed['Suburb_Density'] = 'NaN'
fix3['suburb_density'] = 'NaN'
for i in range(len(fixed)):
    fixed['Suburb_Density'][i] = c[fixed.iloc[i].Suburb]
for i in range(len(fix3)):
    if int(fix3.iloc[i].name) in fixed.Code.values:
        fix3.loc[int(fix3.iloc[i].name),'suburb_density'] = ((fixed.set_index("Code")).loc[int(fix3.iloc[i].name)]).Suburb_Density
fix3=fix3[fix3.suburb_density != 'NaN']
fix3.suburb_density = fix3.suburb_density.astype('int')

fix3['road'] = 'NaN'
fix3['type'] = 'Mobile'
for i in range(len(fix3)):
    fix3.loc[int(fix3.iloc[i].name),'road'] = ((fixed.set_index("Code")).loc[int(fix3.iloc[i].name)]).Road
    fix3.loc[int(fix3.iloc[i].name),'suburb'] = ((fixed.set_index("Code")).loc[int(fix3.iloc[i].name)]).Suburb
mobil3 = fix3
mobile = fixed

fix3['code'] = fix3.index
fix4['code'] = fix4.index
fix3 = fix3.reset_index()
fix4 = fix4.reset_index()
cams = pd.concat([fix3, fix4], axis = 0, ignore_index = True)


# In[15]:


# rename camera types

cams = cams.rename(columns = {2 : 'Proportion of Fines Overturned', 1 : 'Total Fines', 'type' : 'Camera Type', 'road' : 'Road', 'code' : 'Camera Code', 0 : 'Total Overturned Fines', 'density' : 'Total Cameras on Road', 'year' : 'Year', 'suburb' : 'Suburb', 'suburb_density' : 'Total Cameras in Suburb'})
cams['Camera Type'] = cams['Camera Type'].str.replace('PAC', 'Pedestrian-activated Crossing')
cams['Camera Type'] = cams['Camera Type'].str.replace('I/section', 'Intersection')
cams['Camera Type'] = cams['Camera Type'].str.replace('I/Section', 'Intersection')
cams['Camera Type'] = cams['Camera Type'].str.replace('Rail', 'Rail Crossing')
cams['Camera Type'] = cams['Camera Type'].str.replace('P2P', 'Point to Point')     


# In[16]:


# create bubble chart

dt = cams[cams['Total Fines'] > 50]
bubble = px.scatter(data_frame = dt, size = 'Total Cameras in Suburb', y = 'Total Overturned Fines', x = 'Total Fines', hover_name = 'Road', hover_data = ['Proportion of Fines Overturned', 'Total Overturned Fines', 'Camera Type', 'Camera Code', 'Total Cameras on Road', 'Total Cameras in Suburb', 'Suburb'], animation_frame = 'Year', animation_group = 'Suburb', color = 'Camera Type', title = 'Overturned Fines as a Proportion of Total Fines for Traffic Cameras in South Australia')


# In[17]:


# sort by day of the week

weekdays = ["Sunday", "Saturday", "Friday", "Thursday", "Wednesday", "Tuesday", "Monday"]
traffic['day'] = traffic.incident_start_date.dt.day_name()
data = traffic[traffic.camera != 'OTHER'].groupby(['time', 'day']).count()
data2 = traffic[traffic.camera != 'OTHER'].groupby(['time', 'day']).sum()
data = data.filter(['month', 'year'])
data.year = data2.withdrawn
data['full_date'] = data.index
data = data.reset_index(level=[0,1])
data = data.rename(columns = {'month' : 'Total', 'year' : 'Overturned', 'day' : 'Day', 'time' : 'Time'})
data['Proportion'] = data['Overturned'] / data['Total']
data.Day = pd.Categorical(data.Day,categories=weekdays)
data = data.sort_values(["Time", "Day"])
data['Time'] = pd.to_datetime(data.Time, format="%H:%M")
data.Time = data['Time'].dt.strftime("%I %p")


# In[18]:


# sort by day of the week only for human offenses

datahum = traffic[traffic.camera == 'OTHER'].groupby(['time', 'day']).count()
data2 = traffic[traffic.camera == 'OTHER'].groupby(['time', 'day']).sum()
datahum = datahum.filter(['month', 'year'])
datahum.year = data2.withdrawn
datahum['full_date'] = datahum.index
datahum = datahum.reset_index(level=[0,1])
datahum = datahum.rename(columns = {'month' : 'Total', 'year' : 'Overturned', 'day' : 'Day', 'time' : 'Time'})
datahum['Proportion'] = datahum['Overturned'] / datahum['Total']
datahum.Day = pd.Categorical(datahum.Day,categories=weekdays)
datahum = datahum.sort_values(["Time", "Day"])
datahum['Time'] = pd.to_datetime(datahum.Time, format="%H:%M")
datahum.Time = datahum['Time'].dt.strftime("%I %p")


# In[19]:


# create heatmap

dt = go.Heatmap(x = data.Time, y = data.Day, z = data.Proportion, zmin = 0.006, zmax = 0.016, colorbar = dict(y = 0.4))

hm = go.Figure(data=dt, layout = dict(title = dict(text = 'Proportion of Traffic Offenses Misidentified by Cameras at Different Times', xanchor = 'center', x=0.43, y = 0.9)))

hm = hm.update_layout (
    updatemenus = [
        
        dict (
        
            buttons = list ([
                
                dict (
                    
                    args = [{"x": [data.Time], "y" : [data.Day], "z" : [data.Proportion]}, {"title" : "Proportion of Traffic Offenses Misidentified by Cameras at Different Times"}],
                    label = "Cameras",
                    method = "update"
                    
                ),
                dict (
                    
                    args = [{"x": [datahum.Time], "y" : [datahum.Day], "z" : [datahum.Proportion]}, {"title" : "Proportion of Traffic Offenses Misidentified by Humans at Different Times"}],
                    label = "Humans",
                    method = "update"
                    
                )

            ]),
            
            y = 0.8,
            x = 1.325
        ),
        
        dict (
        
            buttons = list ([
                
                dict (
                    
                    args = [{"zmin" : 0.008, "zmax" : 0.018}],
                    label = "High",
                    method = "update"
                    
                ),
                dict (
                    
                    args = [{"zmin" : 0.006, "zmax" : 0.016}],
                    label = "Medium",
                    method = "update"
                    
                ),
                dict (
                    
                    args = [{"zmin" : 0.004, "zmax" : 0.014}],
                    label = "Low",
                    method = "update"
                    
                )


            ]),
            
            y = 0.29,
            x = 1.32,
            active = 1
        )
        
    ],
    
    xaxis_title = "Time",
    
    yaxis_title = "Day"
    
)

hm = hm.add_shape (

    dict (type = 'line', yref = 'paper', xref = 'paper', x0 = 1.16, x1 = 1.16, y0 = -0.1, y1 = 0.9, line = dict(color = "rgb(198,66,125)"))

)

hm = hm.add_shape (

    dict (type = 'line', yref = 'paper', xref = 'paper', x0 = 1.16, x1 = 1.34, y0 = 0.43, y1 = 0.43, line = dict(color = "rgb(198,66,125)"))

)


hm = hm.add_annotation (

    dict (text = "Issued by", yref = 'paper', xref = 'paper', y = 0.9, x = 1.3043, showarrow = False, font = dict(size=13))
    
)

hm = hm.add_annotation (

    dict (text = "Scale", yref = 'paper', xref = 'paper', y = 0.36, x = 1.278, showarrow = False, font = dict(size=13))
    
)

hm = hm.add_annotation (

    dict (text = "Proportion", yref = 'paper', xref = 'paper', y = 1, x = 1.143, showarrow = False, font = dict(size=13))
    
)


# **Visualizations - How Effective are Traffic Cameras in South Australia?**

# *Number of Fines Issued by Traffic Cameras Versus Humans*
# 
# Below is a line plot demonstrating the differences between the number of fines issued by traffic cameras and human police in South Australia over time. The buttons in the top left of the graph can be used to select the distribution recently over the past month, or over a longer period like the past decade. More specific periods of time can be selected using the range slider at the bottom. The dropdown menu on the left of the graph allows for the number of fines to be grouped per day, month, or year. Note that 2011 and 2020 have less fines on the yearly view due to the data not covering these entire years. The buttons below the menu can be used to hide either the camera-issued or human-issued fines, or show both.

# In[24]:


line.show()


# *Overturned Fines as a Proportion of Total Fines for Traffic Cameras in South Australia*
# 
# The below bubble chart compares the number of total fines for each traffic camera used in South Australia, with the number of fines overturned in court. The size of each data point represents the density of cameras in the same suburb as that camera. Hovering over each point shows additional information about each camera, including the street name, suburb name, and camera code used by police. Specific segments of the data, such as cameras with a low number of fines, can be selected by clicking and dragging with the cursor. The slider at the bottom of the graph allows for it to be animated, using the play button to show how use of specific cameras has changed over time. Specific years can also be selected manually using the slider next to the button.

# In[25]:


bubble.show()


# *Proportion of Traffic Offenses Misidentified by Cameras at Different Times*
# 
# The below heatmap demonstrates how the proportion of traffic offenses that are misidentified changes relative to the day of the week and time of day. Blocks are shaded brighter if there is a higher proportion of wrongly issued fines, and darker if the proportion is lower. Each block can be hovered over to see the exact value of the proportion of overturned fines. The menus on the side of the graph allow it to be manipulated. The first dropdown allows for choosing whether the graph shows fines issued by traffic cameras, or by human police. The other allows the scale that determines the shading of the time and day blocks to be increased or decreased.

# In[26]:


hm.show()


# *Average Cost of Fine Issued by Different Policing Types*
# 
# Below is a bar chart demonstrating how fines issued by different policing types in South Australia have changed over time. The play and pause buttons can be used to display an animation of these changes throughout the last decade. The range slider can also be used to manually select a particular year.

# In[27]:


bar.show()

