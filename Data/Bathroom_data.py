import pandas as pd
import numpy as np
import requests as rq
import io
import warnings


url = 'https://data.cityofnewyork.us/resource/i7jb-7jku.csv'

def fetch_all_data_csv(base_url, limit=500, total_rows=10000):
    all_data = pd.DataFrame()  # Empty DataFrame to store all data
    for offset in range(0, total_rows, limit):
        # Request data with limit and offset parameters
        response = rq.get(f"{base_url}?$limit={limit}&$offset={offset}")
        
        if response.status_code == 200:
            # Parse the CSV data
            chunk = pd.read_csv(io.StringIO(response.text))
            with warnings.catch_warnings():
                warnings.simplefilter("ignore",category=FutureWarning)
                all_data = pd.concat([all_data, chunk], ignore_index=True)  # Append to main DataFrame
        else:
            # print(f"Error: Received status code {response.status_code}")
            break  # Stop if there's an error in the request
    return all_data

# Use the function to get data and save it to a CSV
data = fetch_all_data_csv("https://data.cityofnewyork.us/resource/i7jb-7jku.csv")

data['changing_stations'] = data['changing_stations'].fillna('No')
data['changing_stations'] = data['changing_stations'].replace('^\s*$',' ',regex = True)
data['changing_stations'] = data['changing_stations'].map({'':0,' ':0,'No':0,'Yes':1})
data['status'] = data['status'].replace('^\s*$','Not Operational',regex = True)
data['status'] = data['status'].fillna('Not Operational')
data['status'] = data['status'].map({'':0,' ':0,'Not Operational':0,'Operational':1})
data['open'] = data['open'].replace('^\s*$','',regex = True)
Seasonal_index = data[data['open']=='Seasonal'].index
Future_index =  data[data['open']=='Future'].index
Empty_index =  data[data['open']==''].index
Empty2_index = data[data['open']==' '].index
data.drop(Seasonal_index,inplace=True)
data.drop(Future_index,inplace=True)
data.drop(Empty_index,inplace=True)
data.drop(Empty2_index,inplace=True)


data.to_csv("Data/Parsed_CSV.csv",index=False)
# print(data.value_counts())

print(data.head)