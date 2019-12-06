
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

headers = ["Map phase", "Shuffle phase", "Reduce phase", "Finalize", "Total"]
file1 = pd.read_csv('./metrics_10_2_1.csv', engine='c', sep=',', skiprows=1,  names = headers)
file2 = pd.read_csv('./metrics_10_2_2.csv', engine='c', sep=',' ,skiprows=1,  names = headers)
file3 = pd.read_csv('./metrics_10_2_3.csv', engine='c', sep=',' , skiprows=1, names = headers)


# In[6]:


print(file1)


# In[7]:


print(file1.values[:,4:5])


# In[8]:


print(file1[file1.columns[4:]].mean())


# In[13]:


colors = ['yellow', 'lightblue', 'lightgreen']
tot_time = [file1.values[:,4:5],file2.values[:,4:5],file3.values[:,4:5]]
plt.bar(tot_time)
plt.xticks([1, 2, 3], ['10_2_1', '10_2_2', '10_2_3'])
#for patch, colors in zip(bplots['boxes'], colors):
#    patch.set_facecolor(colors)
plt.show()

