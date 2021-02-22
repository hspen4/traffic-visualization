#!/usr/bin/env python
# coding: utf-8

# In[7]:


# import libraries

import pandas as pd
import matplotlib as plt


# In[8]:


# import datasets

twenty = pd.read_csv("2019-2020.csv", dtype = {1:'string', 4:'string', 8:'string', 9:'string', 13:'string', 20:'string', 21:'string', 26:'string'})
nineteen = pd.read_csv("2018-2019.csv", dtype = {1:'string', 4:'string', 8:'string', 9:'string', 13:'string', 20:'string', 21:'string', 26:'string'})
eighteen = pd.read_csv("2017-2018.csv", dtype = {1:'string', 4:'string', 8:'string', 9:'string', 13:'string', 20:'string', 21:'string', 26:'string'})
seventeen = pd.read_csv("2016-2017.csv", dtype = {1:'string', 4:'string', 8:'string', 9:'string', 13:'string', 20:'string', 21:'string', 26:'string'})
sixteen = pd.read_csv("2015-2016.csv", dtype = {1:'string', 4:'string', 8:'string', 9:'string', 13:'string', 20:'string', 21:'string', 26:'string'})
fifteen = pd.read_csv("2014-2015.csv", dtype = {1:'string', 4:'string', 8:'string', 9:'string', 13:'string', 20:'string', 21:'string', 26:'string'})
fourteen = pd.read_csv("2013-2014.csv", dtype = {1:'string', 4:'string', 8:'string', 9:'string', 13:'string', 20:'string', 21:'string', 26:'string'})
thirteen = pd.read_csv("2012-2013.csv", dtype = {1:'string', 4:'string', 8:'string', 9:'string', 13:'string', 20:'string', 21:'string', 26:'string'})
twelve = pd.read_csv("2011-2012.csv", dtype = {1:'string', 4:'string', 8:'string', 9:'string', 13:'string', 20:'string', 21:'string', 26:'string'})


# In[9]:


# combine datasets

combine = [twenty, nineteen, eighteen, seventeen, sixteen, fifteen, fourteen, thirteen, twelve]

orig = pd.concat(combine)


# In[10]:


# make columns readable

orig.columns = [col.replace(' ', '_').lower() for col in orig.columns]

# rename some columns

orig = orig.rename(columns = {'withdrawn_reason_desc' : 'withdrawn', 'notice_status_desc' : 'status', 'drivers_license_state_desc_-_expiation_subject' : 'license_state', 'reg_state_desc_-_expiation_vehicle' : 'vehicle_state', 'local_service_area_desc' : 'area', 'incident_state_date' : 'date', 'time_24_hour_-_incident_start' : 'time', 'expiation_offence_long_description' : 'offence', 'penalty_writtten_on_notice_amount' : 'penalty', 'vehicle_speed' : 'speed', 'expiation_zone_speed_limit' : 'speed_limit', 'speed_camera_category' : 'camera', 'notice_type_desc' : 'issued'})


# In[11]:


# remove unneeded columns

trim = orig.drop(columns = ['photo_rejected_reason_code', 'photo_rejected_reason_desc', 'photo_rejected_reason_desc', 'enforcement_warning_notice_fee_amount', 'fixed_camera_locn_code', 'blood_alcohol_content_-_exp', 'corporate_fee_amount', 'offence_levy_amt', 'offence_penalty_amt', 'location_code_-_mobile_speed_camera', 'expiation_offence_code', 'offence_status', 'offence_status_description', 'issue_date', 'expiation_vehicle_description_-_expiation_vehicle'])


# In[12]:


# remove instances where notices weren't issued

trim = trim[(trim.issued != 'CAUTION ONLY') & (trim.issued != 'LICENSE DISQUALIFICATION')]
trim = trim.drop(columns = ['issued'])


# In[13]:


# sort by whether or not notice was withdrawn

trim.withdrawn[trim.withdrawn == 'WITHDRAWN FOR PROSECUTION(ELECT TO CHALLENGE OFF.)'] = '1'


# In[14]:


# fill rows that were not withdrawn with zeros

trim.withdrawn = trim.withdrawn.fillna('0')
trim.withdrawn[trim.withdrawn != '1'] = '0'


# In[15]:


# export as csv

trim.to_csv('traffic.csv')

