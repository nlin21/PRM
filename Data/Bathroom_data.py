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
data.to_csv("Data/Raw_CSV.csv",index=False)
data = data.drop(columns=['location_type',"operator"])


data['status'] = data['status'].fillna('Not Operational')
data['status'] = data['status'].map({'Closed':0,'Closed for Construction':0,'Not Operational':0,'Operational':1})
data = data[data['status'] != 0]
data = data[data['open'] == 'Year Round']
data['accessibility'] = data['accessibility'].fillna("NA")
data['restroom_type'] = data['restroom_type'].fillna("NA")
data['changing_stations'] = data['changing_stations'].fillna("NA")




data.to_csv("Data/Parsed_CSV.csv",index=False)
# print(data.value_counts())

print(data.head)