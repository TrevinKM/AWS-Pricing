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

* Then we can plot then use some data analysis methods to plot the future predictions

```python  
model_fit.plot_predict(dynamic=False)
plt.show()
```
![image](https://user-images.githubusercontent.com/64080171/176797362-e7044f98-dc46-45ab-837b-f1489ca1cd00.png)

