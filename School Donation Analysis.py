#!/usr/bin/env python
# coding: utf-8

# In[76]:


# libarries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import chart_studio.plotly as pl
import plotly.offline as of
import cufflinks as cf
import datetime as dt
import plotly as po
# plotly.offline.init_notebook_mode()
from plotly.offline import iplot
import plotly.offline as of
import plotly.io as pio
pio.renderers.default='notebook'


# In[77]:


of.init_notebook_mode(connected=True)
cf.go_offline()


# In[2]:


# school dataset
school = pd.read_csv('Schools.csv')


# In[3]:


# donation dataset
donation = pd.read_csv('Donations.csv')


# In[4]:


# donars dataset
donars = pd.read_csv('Donors.csv')


# In[5]:


# project dataset
projects = pd.read_csv('Projects.csv')


# In[6]:


# resources dataset
resources = pd.read_csv('Resources.csv')


# In[7]:


# teachers dataset
teachers = pd.read_csv('Teachers.csv')


# In[8]:


school.head()


# In[9]:


donation.head()


# In[10]:


donars.head()


# In[11]:


resources.head()


# In[12]:


teachers.head()


# In[13]:


projects.head()


# In[14]:


projects.shape


# In[15]:


teachers.head()


# In[17]:


# shape of all the dataset imported

print(f'The shape of school date is: {school.shape} million')
print(f'The shape of Resource date is: {resources.shape} million')
print(f'The shape of donation date is: {donation.shape} million')
print(f'The shape of donars date is: {donars.shape} million')
print(f'The shape of project date is: {projects.shape} million')
print(f'The shape of teacher date is: {teachers.shape} million')


# In[18]:


donars.describe()


# In[19]:


donation.describe()


# In[20]:


school.describe()


# In[21]:


teachers.describe()


# In[22]:


resources.describe()


# In[23]:


projects.describe()


# In[24]:


# merging the whole data

data_1 = pd.merge(donation, projects, how='inner', on='Project ID')


# In[25]:


data_1.head()


# In[26]:


data_2 = pd.merge(data_1, donars, how='inner', on='Donor ID')


# In[27]:


data_2.head()


# In[28]:


data_3 = pd.merge(data_2, school, how='inner', on='School ID')


# In[29]:


data_3.head()


# In[30]:


data_4 = pd.merge(data_3, teachers, how='inner', on='Teacher ID')


# In[32]:


data_4


# In[33]:


a = data_4.columns.values.tolist()


# In[42]:


z = data_4.columns.value_counts()


# In[43]:


z


# In[44]:


a


# ---------------let's calculate the 10 most number of states having schools opened for a project to collect donations.

# In[79]:


s = data_4['School State'].value_counts().sort_values(ascending=False).head(10)


# In[80]:


s.head()


# In[81]:


# draw a bar plot to analyse this

s.iplot(kind='bar',
        xTitle='states',
        yTitle='number of schools',
        title='Max number of schools on a particular state')


# In[82]:


# let's plot the top 10 states with the highest average

h = data_4.groupby('School State')['Donation Amount'].mean().sort_values(ascending=False).head(10)
h


# In[87]:


h.iplot(kind='bar',
       xTitle='STATES',
       yTitle='AMOUNT',
       title='STATES AND MAXIMUM NUMBER OF DONATIONS',colorscale='paired')


# -----------------calculate min, max,mean,precentile,median 25% and 75% of donations

# In[88]:


# Basic mathematical analysis

# calculate min, max,mean,precentile,median 25 and 75% of donations

data_4.describe()


# In[95]:


mean = data_4['Donation Amount'].mean()


# In[96]:


mean


# In[98]:


median = data_4['Donation Amount'].median()


# In[99]:


median


# In[102]:


perctentile = np.percentile(data_4['Donation Amount'].dropna(), [25,75])


# In[103]:


perctentile


# In[104]:


minimum = data_4['Donation Amount'].min()


# In[105]:


minimum


# In[106]:


maximum = data_4['Donation Amount'].max()


# In[107]:


maximum


# In[109]:


print(f'The mean amount is: {round(mean,2)}')
print(f'The median amount is: {median}')
print(f'The maximum is: {maximum}')
print(f'The minimum is: {minimum}')
print(f'The percentile of 25 and 75 are: {perctentile}')


# ----------- let's calculate in which state's donation has been made greater by the donors

# In[119]:


donor = data_4.groupby('Donor State')['Donor ID'].count().sort_values(ascending=False).head(10)
donor


# In[120]:


# let's plot this
donor.iplot(kind = 'bar',
           xTitle='STATES',
           yTitle='AMOUNT',
           title='DONOR STATE AND AMOUNT',
           colorscale='paired')


# In[157]:


s2 = school['School State'].value_counts()
s3 = data_4.groupby('Donor State')['Donation ID'].count()
df = pd.concat([s2, s3], axis=1,keys=['Projects','Donations'])


# In[158]:


df.head()


# In[159]:


df = df.dropna()


# In[164]:


df.iplot(kind='scatter',
        xTitle='Projects',
        yTitle='Donations',
         title='DONATIONS VS PROJECTS',
        colorscale='paired',
        symbol='x',
        mode='markers')


# In[165]:


# let's plot a linear model to check below average and above average rates

df.Projects


# In[166]:


df.Donations


# In[168]:


slope, intercept = np.polyfit(df.Projects, df.Donations, 1)
x = np.array([df.Projects.min(), df.Projects.max()])
y = slope*x + intercept
plt.plot(x,y)


# In[174]:


df.plot.scatter(x = 'Projects', y='Donations')
slope, intercept = np.polyfit(df.Projects, df.Donations, 1)
x = np.array([df.Projects.min(), df.Projects.max()])
y = slope*x + intercept
plt.plot(x,y)
plt.title('PROJECTS VS DONATIONS', fontweight='bold')
plt.tight_layout()
plt.margins(0.05)


# The projects that exist below the above regression line represents below average projects with the donation.

# ----------Project type and total donations

# In[175]:


s5 = data_4['Project Type'].value_counts()
s5


# In[180]:


s6 = data_4.groupby('Project Type')['Donation Amount'].sum().astype(int)


# In[181]:


s6


# In[198]:


# let's draw pie chart 
plt.figure(figsize=(10,8))
plt.pie(s5, startangle=90)
plt.legend(data_4['Project Type'], loc='center')

plt.title('PROJECT TYPE', fontweight='bold')

plt.tight_layout()
plt.margins(0.05)


# In[199]:


# let's plot the type of project subcategory tree which attracts the most donation amount

s7 = data_4['Project Subject Category Tree'].value_counts()


# In[201]:


s7.nunique()


# In[202]:


s8 = data_4.groupby('Project Subject Category Tree')['Donation Amount'].sum().astype(int).sort_values(ascending=False).head(15)


# In[203]:


s8


# In[204]:


s9 = s8/1000000
s9


# In[206]:


s9.iplot(kind='bar',
        xTitle='Project subject category tree',
        yTitle='Donation amount in millions',
        title='PROJECT SUBJECT CATEGORY TREE ATTRACTED POTENTIAL DONATION AMOUNT IN MILLIONS',
        )


# In[207]:


# let's move to time column now

a


# In[208]:


data_4[['Project Posted Date','Project Fully Funded Date']].head()


# In[209]:


data_4[['Project Posted Date','Project Fully Funded Date']].isnull().sum()


# In[210]:


data_4['Project Posted Date'] = pd.to_datetime(data_4['Project Posted Date'])


# In[211]:


data_4['Project Fully Funded Date'] = pd.to_datetime(data_4['Project Fully Funded Date'])


# In[212]:


data_4['Funding time'] = data_4['Project Fully Funded Date'] - data_4['Project Posted Date']


# In[213]:


data_4[['Project Posted Date','Project Fully Funded Date','Funding time']]


# In[215]:


data5 = data_4[pd.notnull(data_4['Funding time'])]


# In[220]:


data5[['Project Posted Date','Project Fully Funded Date','Funding time']].isnull().sum()


# In[222]:


data5[['Project Posted Date','Project Fully Funded Date','Funding time']].head()


# In[224]:


# let's remove days from funding time

import datetime as dt

# remove day from funding column
data5['Funding time'] = data5['Funding time'].dt.days


# In[225]:


data5[['Project Posted Date','Project Fully Funded Date','Funding time']]


# In[226]:


# average time taken to fund the project on ruf basis
ruf_mean_time = data5['Funding time'].mean()
ruf_mean_time


# In[227]:


# average time taken to fund all the projects with project id consideration
overall_mean_time = data5.groupby('Project ID')['Funding time'].mean()
output = overall_mean_time.mean()
output


# In[230]:


# Average funding time for each state

average_funding_time_for_state = data5.groupby(['School State','Project ID'])['Funding time'].mean()


# In[231]:


average_funding_time_for_state


# In[237]:


average_time_funding = averaeg_funding_time_for_state.groupby('School State').mean().round(0)
average_time_funding.head()


# In[251]:


# let's calculate which state is fast and which state is slow in terms of funding

# Fast funding states
fast = average_time_funding
fast[fast<32].sort_values(ascending=False).head()


# In[254]:


fast_funding = fast[fast<32].sort_values(ascending=True).head(10)


# In[265]:


fast_funding.iplot(kind='bar',
                  xTitle='States',
                  yTitle='Funding Time(days)',
                  title='Advanced Funding States',
                  )


# In[258]:


# states which are slow funding

slow_funding = average_time_funding.head(10)


# In[262]:


slow_funding[slow_funding>32].sort_values().head(10)


# In[267]:


slow_funding = slow_funding[slow_funding>32].sort_values().head(10)
slow_funding.iplot(kind='bar',
                  xTitle='States',
                  yTitle='Funding Time(days)',
                  title='SLOW FUNDING STATES',
                  colorscale='paired')


# # -------------------------------THANK YOU------------------------------------

# In[ ]:




