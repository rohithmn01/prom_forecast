#!/usr/bin/env python3

import requests
import copy 
import pandas as pd
URL = "http://34.70.250.100:30000/api/v1/query?query=node_memory_MemFree_bytes{instance=\"10.56.0.4:9100\",job=\"node-exporter\"}[1d]"
  
r = requests.get(url = URL) 

data = r.json()

data_dict={}
metric_list = []
# print(data['data']['result']['values'])
# exit()
for i in data['data']['result']:
    #print(i)
    counter=0
    for j in i['values']:
        data_dict = copy.deepcopy(i['metric'])
        #if counter == 2:
        #    break
        data_dict['time'] = j[0]
        data_dict['value'] = j[1]
        metric_list.append(data_dict)
        #counter += 1 
        
  
#print(metric_list)
df_metric = pd.DataFrame(metric_list)

df1 = df_metric[['time', 'value']]
df1['time'] = pd.to_datetime(df1['time'],unit='s')
df1 = df1.set_index('time')
df1["value"] = df1.values.astype(float)

print(df1)
print(df1.dtypes)

print(df1.resample('15min').mean())
print(type(df1))
df1 = pd.DataFrame(df1.value.str.split(' ',1).tolist(),
                                 columns = ['date','value'])
# df1 = df1.iloc[1: , :]
print(df1)
