#!/usr/bin/env python
# coding: utf-8

# In[1]:


import boto3
import pandas as pd
import datetime
import matplotlib.pylab as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.pylab import rcParams


# In[2]:


def obtainVals(instancesList, product_descList, regionName):
    m4_list = []
    client = boto3.client('ec2', region_name = regionName)
    for i in range(1,90):
        response = client.describe_spot_price_history(
            InstanceTypes=instancesList,
            ProductDescriptions=product_descList,
            StartTime=datetime.datetime.now() - datetime.timedelta(i),
            EndTime=datetime.datetime.now() - datetime.timedelta(i-1),
            MaxResults=10000
        )
        response = response['SpotPriceHistory']
        
        for j in range(0,len(response)):
            m4_list.append(response[j])

    df = pd.DataFrame(m4_list)
    df = df.drop_duplicates()
    df.reset_index(drop=True,inplace=True)
    return df


# In[3]:


df = obtainVals(['m4.2xlarge','g2.2xlarge','r3.2xlarge'],['Linux/UNIX (Amazon VPC)'], 'us-west-2')
df


# In[4]:


df.InstanceType.value_counts().plot(kind='bar')
plt.ylabel("Number of instances")
plt.xlabel("InstanceType")
plt.title("Instances in each type")


# In[5]:


df.AvailabilityZone.value_counts().plot(kind='bar')
plt.ylabel("Number of instances")
plt.xlabel("AvailabilityZone")
plt.title("Instances in each zone")


# In[6]:


us_wa = df.loc[df['AvailabilityZone'] == 'us-west-2a']
us_wa


# In[7]:


us_wb = df.loc[df['AvailabilityZone'] == 'us-west-2b']
us_wb 


# In[8]:


us_wc = df.loc[df['AvailabilityZone'] == 'us-west-2c']
us_wc


# In[9]:


us_wa_m4 = us_wa.loc[us_wa['InstanceType'] == 'm4.2xlarge']
us_wa_m4


# In[10]:


us_wb_m4 = us_wb.loc[us_wb['InstanceType'] == 'm4.2xlarge']
us_wb_m4


# In[11]:


us_wc_m4 = us_wc.loc[us_wc['InstanceType'] == 'm4.2xlarge']
us_wc_m4


# In[12]:


us_wa_m4.set_index('Timestamp',inplace=True)
us_wb_m4.set_index('Timestamp',inplace=True)
us_wc_m4.set_index('Timestamp',inplace=True)

for col in ['InstanceType', 'AvailabilityZone', 'ProductDescription']:
    us_wa_m4 = us_wa_m4.drop(col, axis=1)
    us_wb_m4 = us_wb_m4.drop(col, axis=1)
    us_wc_m4 = us_wc_m4.drop(col, axis=1)

us_wa_m4['SpotPrice'] = us_wa_m4['SpotPrice'].apply(pd.to_numeric)
us_wb_m4['SpotPrice'] = us_wb_m4['SpotPrice'].apply(pd.to_numeric)
us_wc_m4['SpotPrice'] = us_wc_m4['SpotPrice'].apply(pd.to_numeric)

us_wa_day = us_wa_m4.resample('D').mean()
us_wb_day = us_wb_m4.resample('D').mean()
us_wc_day = us_wc_m4.resample('D').mean()

us_wa_hour = us_wa_m4.resample('H').mean()
us_wb_hour = us_wb_m4.resample('H').mean()
us_wc_hour = us_wc_m4.resample('H').mean()

us_wb_hour


# In[13]:


us_wa_hour.fillna(method='ffill',inplace=True)
us_wb_hour.fillna(method='ffill',inplace=True)
us_wb_hour.fillna(method='ffill',inplace=True)


# In[14]:


rcParams['figure.figsize'] = 15, 6

## plotting for the day frequency; remember we did not fill the values for day frequency
plt.plot(us_wa_day,label='Zone A')
plt.plot(us_wb_day,label='Zone B')
plt.plot(us_wc_day,label='Zone C')
plt.legend(loc='best')
plt.ylabel("Spot Price")
plt.xlabel("Date")
plt.title("Daily spot price per zone")


# In[15]:


plt.plot(us_wb_hour)


# In[16]:


rolmean = us_wa_day.rolling(window = 7).mean()


## plot the results
orig = plt.plot(us_wa_day,label='Prices')
mean = plt.plot(rolmean, label='Rolling Mean')
plt.legend(loc='best')
plt.title('Rolling Mean at Zone A')


# In[17]:


rolmean = us_wb_day.rolling(window = 7).mean()

## plot the results
orig = plt.plot(us_wa_day,label='Prices')
mean = plt.plot(rolmean, label='Rolling Mean')
plt.legend(loc='best')
plt.title('Rolling Mean at Zone B')


# In[18]:


rolmean = us_wc_day.rolling(window = 7).mean()

## plot the results
orig = plt.plot(us_wa_day,label='Prices')
mean = plt.plot(rolmean, label='Rolling Mean')
plt.legend(loc='best')
plt.title('Rolling Mean at Zone C')


# In[19]:


from statsmodels.tsa.stattools import adfuller

x = us_wa_day.SpotPrice
result = adfuller(x)


# ---------Important-----------------------
# Utilise the REPL nature of the software for 
# instantiating the following parameters for models 
# use iteratively with the dfoutput function to create 
# DH tests

# In[20]:


x = us_wb_day.SpotPrice
result = adfuller(x)


# In[21]:


x = us_wc_day.SpotPrice
result = adfuller(x)


# In[22]:


dfoutput = pd.Series(result[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
for key,value in result[4].items():
    dfoutput['Critical Value (%s)'%key] = value
print(dfoutput)


# In[23]:


from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
import statsmodels as sm


# In[24]:


plot_acf(x,lags=44)
plt.show
plot_pacf(x,lags=44)
plt.show


# In[25]:


from statsmodels.tsa.arima_model import ARIMA
model=ARIMA(x,order=(1,1,1))
model_fit=model.fit()
model_fit.summary()


# In[26]:


model_fit.plot_predict(dynamic=False)
plt.show()


# In[ ]:




