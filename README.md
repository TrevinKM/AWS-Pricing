# AWS-Pricing
## Python data analysis

* First there was a funciton made to scrape the data from the AWS API and analyse it
```python 
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
```
![image](https://user-images.githubusercontent.com/64080171/176796260-de479f16-ac8d-4043-a97f-cdd358341029.png)
* Then we are able to analyse the instances in the data given using the dataframes
```python
df.InstanceType.value_counts().plot(kind='bar')
plt.ylabel("Number of instances")
plt.xlabel("InstanceType")
plt.title("Instances in each type")
```
![image](https://user-images.githubusercontent.com/64080171/176796449-f2ad56d6-9da0-4e03-8c80-1673713dc912.png)
* Using `fillna` we are able to normalise the data
```python
us_wa_hour.fillna(method='ffill',inplace=True)
us_wb_hour.fillna(method='ffill',inplace=True)
us_wb_hour.fillna(method='ffill',inplace=True)
```
* Using the matplotlib functions we can represent the data too

```python
orig = plt.plot(us_wa_day,label='Prices')
mean = plt.plot(rolmean, label='Rolling Mean')
plt.legend(loc='best')
plt.title('Rolling Mean at Zone A')
```

* We can further break down the parameters of the search results 

```python
us_wc_m4 = us_wc.loc[us_wc['InstanceType'] == 'm4.2xlarge']
us_wc_m4
```
* From the results obtained we can find the sections of the data whether by days or hours

```python
us_wa_m4.set_index('Timestamp',inplace=True)

for col in ['InstanceType', 'AvailabilityZone', 'ProductDescription']:
    us_wa_m4 = us_wa_m4.drop(col, axis=1)

us_wa_m4['SpotPrice'] = us_wa_m4['SpotPrice'].apply(pd.to_numeric)
us_wa_day = us_wa_m4.resample('D').mean()
us_wa_hour = us_wa_m4.resample('H').mean()

us_wb_hour   
```
* Using dickey fuller we can also test the data if it is stationary

Test Statistic                 | 0.454991
--- | --- 
p-value                        | 0.983439
#Lags Used                     | 7.000000
Number of Observations Used   | 82.000000
Critical Value (1%)           | -3.512738
Critical Value (5%)           | -2.897490
Critical Value (10%)          | -2.585949
dtype: float64
* One of the things we can do is find the pcf and acf of the data

![image](https://user-images.githubusercontent.com/64080171/176798505-5b597b55-6387-444e-be9f-141324c6fc1e.png)

* Then we can plot then use some data analysis methods to plot the future predictions, this is using the ARIMA model

```python  
model_fit.plot_predict(dynamic=False)
plt.show()
```
![image](https://user-images.githubusercontent.com/64080171/176797362-e7044f98-dc46-45ab-837b-f1489ca1cd00.png)

