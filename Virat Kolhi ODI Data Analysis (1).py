#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_column',None)
pd.set_option('display.max_rows',None)
pd.set_option('display.max_seq_items',None)
pd.set_option('display.max_colwidth', 500)
pd.set_option('expand_frame_repr', True)


# In[2]:


#Loading dataset
df=pd.read_csv(r'C:\Users\hindu\Downloads\archive (3)\Virat_Kohli_ODI.csv')


# In[3]:


df.head()


# In[4]:


df.tail()


# In[5]:


des=pd.read_csv(r'C:\Users\hindu\Downloads\archive (3)\DataDictionary-Cricket.csv')


# In[6]:


des.info


# # Data Pre-Processing

# In[7]:


df.info


# In[9]:


# Checking missing values for 'Mins'
df[df['Mins']=="-"]


# In[24]:


# Filter out non-integer values and handle missing values
temp_df = df[df['Mins'].astype(str).str.isnumeric()]

# Replace non-integer values in 'Mins' with NaN
temp_df['Mins'] = pd.to_numeric(temp_df['Mins'], errors='coerce')

# Calculate average minutes per ball
avg_min_per_ball = temp_df['Mins'].mean()


# In[27]:


# Calculating average minutes per ball to use it for filling missing values in 'Mins' column

temp_arr = temp_df.agg({'Mins':'sum', 'BF':'sum'}).values
avg_min_per_ball = temp_arr[1]/temp_arr[0]


# In[30]:


# Impute missing values in 'Mins' columns by 'BF'*avg_min_per_ball
df['Mins'] = df.apply(lambda x: int(x['BF'] * avg_min_per_ball) if not np.isnan(x['Mins']) else np.nan, axis=1)


# In[32]:


# Create a new boolean column 'Not Out'
df['Not Out'] = df['Runs'].apply(lambda x: 'Yes' if '*' in x else 'No')


# In[33]:


# Convert datatype of 'Runs' column to integer
df['Runs'] = df['Runs'].apply(lambda x: int(x[:-1]) if '*' in x else int(x))


# In[34]:


# Convert datatype of 'Start Date' to datetime
df['Start Date'] = pd.to_datetime(df['Start Date'])
# Create a new column 'Quarter' from 'Start Date'
df['Quarter'] =df['Start Date'].dt.quarter
# Create a new column 'Year' from 'Start Date'
df['Year'] = df['Start Date'].dt.year


# In[37]:


# Checking for missing values in Strike Rate
df[df['SR']=="-"]


# In[39]:


# Imputing Strike Rate with 0 since for that match Virat got out at 0 and converting it to float type
df[df['SR']=="-"] = 0
df['SR'] = df['SR'].astype(float)


# In[40]:


# Removing row with all Null values
df[df['Year']==0]


# In[41]:


df = df[df['Year']!=0]


# # Assignment Question

# 1. Using the data set, find out the country against which Virat Kohli has the maximum batting average. Here, the batting average is given by (total number of runs Virat scored)/(the total number of matches he played) and not the average runs Virat Kohli scored before getting out.

# In[42]:


df.groupby('Opposition').agg({'Runs' : 'sum', 'Opposition':'count'}).head()


# In[43]:


dict1 = {}
for i in df.index:   
    runs =df.loc[i].Runs
    country = df.loc[i].Opposition
    if country not in dict1:
        dict1[country] = [runs, 1]
    else:
        dict1[country] = [dict1[country][0]+runs, dict1[country][1]+1]    
dict1


# In[44]:


max = 0
team = ''
for k,v in dict1.items():
    avg = v[0]/v[1]
    if avg> max:
        max = avg
        team = k
max,team


# Note:Virat Kohli has the maximum batting average against Bangladesh

# 2. Plot a histogram to see where Virat Kohli has scored the most number of times.

# In[47]:


runs= df['Runs']
plt.figure(figsize = (20,10))
plt.hist(runs, bins = 16)
plt.show()


# 3. Whenever Virat Kohli has scored 90-100 runs (exclude 100), what has been the average strike rate?

# In[48]:


avg_list = []
for i in df.index:
    row = df.loc[i]
    runs = row['Runs']
    if runs >= 90 and runs <100:
        avg_list.append(float(row['SR']))       
avg_sr = sum(avg_list)/ len(avg_list)
avg_sr


# 4. Using the previous histogram, find the run interval where Virat has scored the maximum number of sixes. Also, mention the number of fours he hit in the same bracket.

# In[50]:


runs= df['Runs']
group_bin = [i//10 for i in runs]
df['Group_Size'] = group_bin
df1 = df.groupby('Group_Size').sum().reset_index()
df1.head()
max_six = 0
for i in df1.index:
    row = (df1.iloc[i])
    six_run = row['6s']
    if max_six<six_run:
        max_six = six_run
        max_four = row['4s']
        group_int = row['Group_Size']
max_six, max_four, group_int


# NOTE:In Group 10 i.e; 100,110 runs Kohli hit 14 Sixes and 90 Fours

# 5. Plot a pie chart to find out the approximate percentage of the times Virat Kohli has been out by LBW in all his innings. Take into account all his innings, including the ones in which he remained not out.

# In[52]:


df2= df[['Dismissal','Runs']].groupby('Dismissal').count()
lbw_count = df2.loc['lbw'].values[0]
total = df2.Runs.sum()
lbw_count, total


# In[54]:


plt.figure(figsize = (10,10))
plt.pie(x = [lbw_count,total],labels= ['LBW','Total Innings'] ,autopct='%.1f')
plt.show()


# 6. Let’s say you want to visualize the consistency of the runs scored by Virat against various teams, i.e. you want to compare the spread of the runs scored by Virat against various teams. Which of the following plots will be the most appropriate for visualizing this?

# In[56]:


plt.figure(figsize = (10,10))
sns.boxplot(x= 'Opposition', y = 'Runs', data = df)
plt.xticks(rotation = 90)
plt.show()


# 7. In which years have Kohli’s runs kept improving in the Q2-Q4 period given that he played at least one match in that period?

# In[57]:


temp_df = df[df['Quarter'].isin([1,2,3,4])].groupby(['Year','Quarter']).agg({'Runs':'sum', 'Inns':'sum'}).apply(lambda x: x[0]/x[1], axis=1).reindex()


# In[58]:


temp_df.plot(kind='bar', figsize = (20,10))
plt.show()


# In[59]:


df3 =df[['Start Date','Inns','Runs']]
df3.index = df3['Start Date']
df4  = df3.resample('Q', convention='end').agg('sum')
plt.figure(figsize = (20,10))
df4['Inns'].plot( kind = 'line')
df4['Runs'].plot( kind = 'line')
plt.show()


# 8. Against which country has Virat scored the maximum aggregate runs in matches where the mode of dismissal was “caught”?

# In[60]:


df[df['Dismissal']=='caught'].groupby('Opposition').agg({'Runs':'sum', 'Inns':'sum'}).apply(lambda x: x[0]/x[1], axis=1).idxmax()


# Virat scored the maximum aggregate runs in matches against West Indies where the mode of dismissal was “caught”

# 9. What is the batting position at which Virat has the best average against England?
# 

# In[61]:


# Calculating average 
df[df['Opposition']=='v England'].groupby('Pos').agg({'Runs':'sum', 'Inns':'sum'}).apply(lambda x: x[0]/x[1], axis=1)


# In[62]:


# Finding batting position
df[df['Opposition']=='v England'].groupby('Pos').agg({'Runs':'sum', 'Inns':'sum'}).apply(lambda x: x[0]/x[1], axis=1).idxmax()


# Virat has best average against England at 4th Batting position

# In[ ]:




